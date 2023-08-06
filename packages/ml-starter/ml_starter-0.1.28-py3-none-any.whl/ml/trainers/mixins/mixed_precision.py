"""Defines a mixin for doing FP16 scaling.

FP16 scaling is a technique for training with FP16 precision while maintaining
FP32 precision for the model weights. This is done by scaling the loss by a
large factor (e.g. 2^16) and then scaling the gradients by the inverse of that
factor. So if the scale factor starts to decrease, it means that the loss is
overflowing and training is diverging.
"""

import logging
from dataclasses import dataclass
from typing import Any, Iterable, TypeVar, cast

import torch
from torch import Tensor, inf, nn
from torch.distributed.fsdp.fully_sharded_data_parallel import FullyShardedDataParallel as FSDP
from torch.optim import Optimizer
from torch.utils._foreach_utils import _group_tensors_by_device_and_dtype, _has_foreach_support

from ml.core.config import conf_field
from ml.trainers.base import BaseTrainer, BaseTrainerConfig, ModelT, TaskT

logger = logging.getLogger(__name__)

GradDict = dict[tuple[torch.device, torch.dtype], list[list[Tensor]]]


@torch.no_grad()
def clip_grad_norm_(
    parameters: Iterable[nn.Parameter],
    max_norm: float,
    norm_type: float = 2.0,
    foreach: bool | None = None,
) -> tuple[Tensor, bool]:
    """Clips gradient norm of an iterable of parameters.

    The norm is computed over all gradients together, as if they were
    concatenated into a single vector. Gradients are modified in-place.

    Args:
        parameters: An iterable of the model parameters.
        max_norm: The maximum norm of the gradients.
        norm_type: The type of the used p-norm.
        foreach: Use the faster foreach-based implementation. If ``None``, use
            the foreach implementation for CUDA and CPU native tensors and
            silently fall back to the slow implementation for other device
            types. If ``True`` or ``False``, use the foreach or non-foreach
            implementation, respectively, and raise an error if the chosen
            implementation is not available.

    Returns:
        The total norm of the parameters (viewed as a single vector) and
        whether the parameters were successfully clipped.
    """
    grads = [p.grad for p in parameters if p.grad is not None]
    max_norm = float(max_norm)
    norm_type = float(norm_type)
    if len(grads) == 0:
        return torch.tensor([0.0]), True

    first_device = grads[0].device
    grouped_grads = cast(GradDict, _group_tensors_by_device_and_dtype([[g.detach() for g in grads]]))

    if norm_type == inf:
        norms = [g.detach().abs().max().to(first_device) for g in grads]
        total_norm = norms[0] if len(norms) == 1 else torch.max(torch.stack(norms))
    else:
        norms = []
        for (device, _), [grads] in grouped_grads.items():
            if (foreach is None or foreach) and _has_foreach_support(grads, device=device):
                norms.extend(torch._foreach_norm(grads, norm_type))
            elif foreach:
                raise RuntimeError(f"foreach=True was passed, but can't use the foreach API on {device.type} tensors")
            else:
                norms.extend([torch.norm(g, norm_type) for g in grads])

        total_norm = torch.norm(torch.stack([norm.to(first_device) for norm in norms]), norm_type)

    if not torch.isfinite(total_norm):
        return total_norm, False

    clip_coef = max_norm / (total_norm + 1e-6)
    clip_coef_clamped = torch.clamp(clip_coef, max=1.0)
    for (device, _), [grads] in grouped_grads.items():
        if (foreach is None or foreach) and _has_foreach_support(grads, device=device):
            torch._foreach_mul_(grads, clip_coef_clamped.to(device))  # type: ignore[call-overload]
        elif foreach:
            raise RuntimeError(f"foreach=True was passed, but can't use the foreach API on {device.type} tensors")
        else:
            clip_coef_clamped_device = clip_coef_clamped.to(device)
            for g in grads:
                g.detach().mul_(clip_coef_clamped_device)

    return total_norm, True


@dataclass
class MixedPrecisionConfig:
    enabled: bool = conf_field(True, help="If set, should FP16 training be enabled")
    init_scale: float = conf_field(2.0**16, help="Initial scaling factor")
    growth_factor: float = conf_field(2.0, help="Factor by which the scale is multiplied if no gradient NaNs occur")
    backoff_factor: float = conf_field(0.5, help="Factor by which the scale is multiplied if gradient NaNs occur")
    growth_interval: int = conf_field(2000, help="How often to grow the scale")
    min_grad_scale: float = conf_field(1e-4, help="Minimum allowable gradient scale")


@dataclass
class MixedPrecisionTrainerConfig(BaseTrainerConfig):
    mixed_precision: MixedPrecisionConfig = conf_field(MixedPrecisionConfig(), help="Mixed precision configuration")
    clip_grad_norm: float = conf_field(10.0, help="What to clip the gradient norm to")
    clip_grad_norm_type: Any = conf_field(2, help="Type of norm to use")


MixedPrecisionConfigT = TypeVar("MixedPrecisionConfigT", bound=MixedPrecisionTrainerConfig)


class MixedPrecisionTrainerMixin(BaseTrainer[MixedPrecisionConfigT, ModelT, TaskT]):
    """Defines a trainer mixin for doing FP16 scaling."""

    def __init__(self, config: MixedPrecisionConfigT) -> None:
        super().__init__(config)

        self.grad_scaler: torch.cuda.amp.GradScaler | None
        if self._device.supports_grad_scaler() and self.config.mixed_precision.enabled:
            self.grad_scaler = torch.cuda.amp.GradScaler(
                init_scale=self.config.mixed_precision.init_scale,
                growth_factor=self.config.mixed_precision.growth_factor,
                backoff_factor=self.config.mixed_precision.backoff_factor,
                growth_interval=self.config.mixed_precision.growth_interval,
                enabled=True,
            )
        else:
            self.grad_scaler = None

        self.autocast_context = self._device.autocast_context(enabled=self.config.mixed_precision.enabled)

    def scale_mixed_precision(self, tensor: Tensor) -> Tensor:
        if self.grad_scaler is not None:
            return self.grad_scaler.scale(tensor)
        return tensor

    def backward_grads(self, loss: Tensor) -> None:
        if loss.numel() > 1:
            loss = loss.sum()
        if self.grad_scaler is not None:
            loss = self.grad_scaler.scale(loss)
        isnan = not bool(torch.isfinite(loss))
        if isnan:
            loss.backward(torch.zeros_like(loss))
        else:
            loss.backward()

        if isnan and self.grad_scaler is not None:
            with torch.no_grad():
                new_scale = self.grad_scaler.get_scale() * self.grad_scaler.get_backoff_factor()
                if new_scale < self.config.mixed_precision.min_grad_scale:
                    raise FloatingPointError("Minimum gradient scale reached; your loss is probably exploding")
                logger.warning("Loss NaNs detected; reducing scale to %.2g", new_scale)
                self.grad_scaler.update(new_scale)

    @torch.no_grad()
    def step_optimizer(self, model: nn.Module, optim: Optimizer) -> None:
        clip_norm = self.config.clip_grad_norm
        norm_type = self.config.clip_grad_norm_type

        # Unscale gradients.
        if self.grad_scaler is not None:
            self.grad_scaler.unscale_(optim)

        # Clips gradients.
        if isinstance(model, FSDP):
            total_norm = model.clip_grad_norm_(clip_norm, norm_type)
            was_clipped = bool(torch.isfinite(total_norm))
            self.logger.log_scalar("total_norm", total_norm.item(), namespace="optim")
        else:
            total_norm, was_clipped = clip_grad_norm_(
                model.parameters(),
                max_norm=clip_norm,
                norm_type=norm_type,
                foreach=True,
            )
            self.logger.log_scalar("total_norm", total_norm, namespace="optim")

        # Steps the optimizer.
        if self.grad_scaler is None:
            if was_clipped:
                optim.step()
        elif was_clipped:
            self.grad_scaler.step(optim)
            self.grad_scaler.update()
        else:
            new_scale = self.grad_scaler.get_scale() * self.grad_scaler.get_backoff_factor()
            if new_scale < self.config.mixed_precision.min_grad_scale:
                raise FloatingPointError("Minimum gradient scale reached; your loss is probably exploding")
            logger.warning("Gradient NaNs detected; reducing scale to %.2g", new_scale)
            self.grad_scaler.update(new_scale)

    def log_mp_scale(self) -> None:
        if (scaler := self.grad_scaler) is not None and scaler._enabled:
            self.logger.log_scalar("fp16_scale", scaler.get_scale)
            self.logger.log_scalar("fp16_growth", scaler._get_growth_tracker)

    def load_state_dict(self, ckpt: dict[str, Any]) -> None:
        if self.grad_scaler is not None:
            self.grad_scaler.load_state_dict(ckpt["grad_scaler"])

        super().load_state_dict(ckpt)

    def update_state_dict(self, ckpt: dict[str, Any]) -> None:
        if self.grad_scaler is not None:
            assert "grad_scaler" not in ckpt

            ckpt["grad_scaler"] = self.grad_scaler.state_dict()

        super().update_state_dict(ckpt)
