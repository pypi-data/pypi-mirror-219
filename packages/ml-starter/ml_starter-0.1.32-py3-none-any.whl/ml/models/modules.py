"""Miscellaneous shared modules which can be used in various models."""

from torch import Tensor
from torch.autograd.function import Function, FunctionCtx


class _InvertGrad(Function):
    @staticmethod
    def forward(ctx: FunctionCtx, input: Tensor) -> Tensor:  # type: ignore[override]
        return input

    @staticmethod
    def backward(ctx: FunctionCtx, grad_output: Tensor) -> Tensor:  # type: ignore[override]
        return -grad_output


def invert_grad(input: Tensor) -> Tensor:
    """Inverts the gradient of the input.

    Args:
        input: Input tensor.

    Returns:
        The identity of the input tensor in the forward pass, and the negative
        of the gradient in the backward pass.
    """
    return _InvertGrad.apply(input)
