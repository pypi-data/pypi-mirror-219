"""Defines utility functions for Diffusion models.

This module can be used to train a Gaussian diffusion model as follows.

.. code-block:: python

    # Instantiate the beta schedule and diffusion module.
    betas = get_diffusion_beta_schedule("linear", 1000)
    diff = GaussianDiffusion(betas)

    # Pseudo-training loop.
    for _ in range(1000):
        images = ds[index]  # Get some image from the dataset
        times = diff.sample_random_times(images)
        q_sample, noise = diff.q_sample(images, times)
        pred_noise = model(q_sample, times)
        loss = F.mse_loss(pred_noise, noise)
        loss.backward()
        optimizer.step()

    # Sample from the model.
    init_noise = torch.randn_like(images)
    generated = diff.p_sample_loop(model, init_noise)
    show_image(generated[-1])

Choices for the beta schedule are:

- ``"linear"``: Linearly increasing beta.
- ``"quad"``: Quadratically increasing beta.
- ``"warmup"``: Linearly increasing beta with a warmup period.
- ``"const"``: Constant beta.
- ``"jsd"``: Jensen-Shannon divergence schedule.
"""

from typing import Callable, Literal, get_args

import torch
from torch import Tensor, nn

DiffusionBetaSchedule = Literal["linear", "quad", "warmup", "const", "jsd"]


def _warmup_beta_schedule(
    beta_start: float,
    beta_end: float,
    num_timesteps: int,
    warmup: float,
    dtype: torch.dtype = torch.float64,
) -> Tensor:
    betas = beta_end * torch.ones(num_timesteps, dtype=dtype)
    warmup_time = int(num_timesteps * warmup)
    betas[:warmup_time] = torch.linspace(beta_start, beta_end, warmup_time, dtype=dtype)
    return betas


def get_diffusion_beta_schedule(
    schedule: DiffusionBetaSchedule,
    num_timesteps: int,
    *,
    beta_start: float = 0.0001,
    beta_end: float = 0.02,
    warmup: float = 0.1,
    dtype: torch.dtype = torch.float64,
) -> Tensor:
    """Returns a beta schedule for the given schedule type.

    Args:
        schedule: The schedule type.
        num_timesteps: The total number of timesteps.
        beta_start: The initial beta value.
        beta_end: The final beta value.
        warmup: The fraction of timesteps to use for warmup.
        dtype: The dtype of the returned tensor.

    Returns:
        The beta schedule, a tensor with shape ``(num_timesteps)``.
    """
    match schedule:
        case "linear":
            return torch.linspace(beta_start, beta_end, num_timesteps, dtype=dtype)
        case "quad":
            return torch.linspace(beta_start**0.5, beta_end**0.5, num_timesteps, dtype=dtype) ** 2
        case "warmup":
            return _warmup_beta_schedule(beta_start, beta_end, num_timesteps, warmup, dtype=dtype)
        case "const":
            return torch.full((num_timesteps,), beta_end, dtype=dtype)
        case "jsd":
            return torch.linspace(num_timesteps, 1, num_timesteps, dtype=dtype) ** -1.0
        case _:
            raise NotImplementedError(f"Unknown schedule type: {schedule}")


def _extract_mul(a: Tensor, t: Tensor, x: Tensor) -> Tensor:
    b, *_ = t.shape
    out = a.gather(-1, t)
    return out.view(b, *((1,) * (len(x.shape) - 1))) * x


class GaussianDiffusion(nn.Module):
    """Defines a module which provides utility functions for Gaussian diffusion.

    Parameters:
        betas: The beta values for each timestep, provided by the function
            :func:`get_diffusion_beta_schedule`.
    """

    __constants__ = ["num_timesteps"]

    def __init__(self, betas: Tensor, eps: float = 1e-9) -> None:
        super().__init__()

        assert betas.dim() == 1

        self.num_timesteps = betas.shape[0]

        alphas = 1.0 - betas
        alphas_cum = torch.cumprod(alphas, dim=0)
        alphas_cum_prev = torch.cat([torch.ones(1, dtype=betas.dtype), alphas_cum[:-1]])
        sqrt_alphas_cum = alphas_cum.sqrt()
        sqrt_one_minus_alphas_cum = (1.0 - alphas_cum).sqrt()
        log_one_minus_alpha_cum = alphas_cum.log()
        sqrt_recip_alphas_cum = (1.0 / alphas_cum).sqrt()
        sqrt_recip_alphas_cum_minus_one = (1.0 / alphas_cum - 1.0).sqrt()
        posterior_var_mul = (1.0 - alphas_cum_prev) / (1.0 - alphas_cum)
        posterior_var = betas * posterior_var_mul
        posterior_log_var_clipped = posterior_var.clamp_min(eps).log()
        posterior_mean_coef1 = betas * sqrt_alphas_cum / (1.0 - alphas_cum)
        posterior_mean_coef2 = alphas.sqrt() * posterior_var_mul

        self.register_buffer("betas", betas, persistent=False)
        self.register_buffer("alphas", alphas, persistent=False)
        self.register_buffer("alphas_cum", alphas_cum, persistent=False)
        self.register_buffer("alphas_cum_prev", alphas_cum_prev, persistent=False)
        self.register_buffer("sqrt_alphas_cum", sqrt_alphas_cum, persistent=False)
        self.register_buffer("sqrt_one_minus_alphas_cum", sqrt_one_minus_alphas_cum, persistent=False)
        self.register_buffer("log_one_minus_alpha_cum", log_one_minus_alpha_cum, persistent=False)
        self.register_buffer("sqrt_recip_alphas_cum", sqrt_recip_alphas_cum, persistent=False)
        self.register_buffer("sqrt_recip_alphas_cum_minus_one", sqrt_recip_alphas_cum_minus_one, persistent=False)
        self.register_buffer("posterior_var", posterior_var, persistent=False)
        self.register_buffer("posterior_log_var_clipped", posterior_log_var_clipped, persistent=False)
        self.register_buffer("posterior_mean_coef1", posterior_mean_coef1, persistent=False)
        self.register_buffer("posterior_mean_coef2", posterior_mean_coef2, persistent=False)

    betas: Tensor
    alphas: Tensor
    alphas_cum: Tensor
    alphas_cum_prev: Tensor
    sqrt_alphas_cum: Tensor
    sqrt_one_minus_alphas_cum: Tensor
    log_one_minus_alpha_cum: Tensor
    sqrt_recip_alphas_cum: Tensor
    sqrt_recip_alphas_cum_minus_one: Tensor
    posterior_var: Tensor
    posterior_log_var_clipped: Tensor
    posterior_mean_coef1: Tensor
    posterior_mean_coef2: Tensor

    def sample_random_times(self, bsz: int, *, weights: Tensor | None = None, device: torch.device) -> Tensor:
        """Samples random timesteps for each element in the batch.

        Args:
            bsz: The batch size.
            weights: The weights for each timestep, used for sampling.
                If ``None``, a uniform distribution is used. Otherwise, should
                be a tensor of shape ``(num_timesteps)``.
            device: The device to use.

        Returns:
            A tensor of shape ``(bsz)`` containing the sampled timesteps, as
            integer values in the range ``[0, num_timesteps)``.
        """
        if weights is None:
            return torch.randint(0, self.num_timesteps, (bsz,), device=device, dtype=torch.long)
        return torch.multinomial(weights, bsz, replacement=True)

    def _get_sampling_timesteps(self, bsz: int, *, device: torch.device) -> list[Tensor]:
        t = torch.arange(start=self.num_timesteps - 1, end=0, step=-1, device=device, dtype=torch.long)
        return list(t.unsqueeze(0).repeat_interleave(bsz, dim=0).unbind(dim=1))

    def _q_posterior(self, x_start: Tensor, x_t: Tensor, t: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        lhs = _extract_mul(self.posterior_mean_coef1, t, x_start)
        rhs = _extract_mul(self.posterior_mean_coef2, t, x_t)
        posterior_mean = lhs + rhs
        posterior_var = self.posterior_var.gather(-1, t)
        posterior_log_var_clipped = self.posterior_log_var_clipped.gather(-1, t)
        return posterior_mean, posterior_var, posterior_log_var_clipped

    def q_sample(self, x_start: Tensor, t: Tensor) -> tuple[Tensor, Tensor]:
        r"""Samples a noise tensor from the posterior :math:`q(x_t|x_0)`.

        Args:
            x_start: The starting point :math:`x_0`.
            t: The timestep :math:`t`.

        Returns:
            A tuple ``(x_t, noise)`` where ``x_t`` is the sampled point
            :math:`x_t` and ``noise`` is the sampled noise :math:`\\epsilon_t`.
        """
        noise = torch.randn_like(x_start)
        lhs = _extract_mul(self.sqrt_alphas_cum, t, x_start)
        rhs = _extract_mul(self.sqrt_one_minus_alphas_cum, t, noise)
        x_noisy = lhs + rhs
        return x_noisy, noise

    def _predict_start_from_noise(self, x_t: Tensor, t: Tensor, noise: Tensor) -> Tensor:
        lhs = _extract_mul(self.sqrt_recip_alphas_cum, t, x_t)
        rhs = _extract_mul(self.sqrt_recip_alphas_cum_minus_one, t, noise)
        return lhs - rhs

    @torch.no_grad()
    def _p_sample(self, mean: Tensor, log_var: Tensor, noise: Tensor, times: Tensor) -> Tensor:
        is_last_sampling_timestep = times == 0
        nonzero_mask = 1 - is_last_sampling_timestep.to(log_var)
        pred_var = nonzero_mask * (0.5 * log_var).exp()
        return mean + pred_var.view(-1, *([1] * (noise.dim() - 1))) * noise

    @torch.no_grad()
    def p_sample_loop(self, func: Callable[[Tensor, Tensor], Tensor], init_noise: Tensor) -> list[Tensor]:
        """Samples from the trained model in a loop.

        Args:
            func: The function to sample from, which takes the current frame
                and the time and returns the predicted noise
            init_noise: The initial noise, a Gaussian distribution with the
                same shape as the data

        Returns:
            A list of sampled data with decreasing noise levels, with the
            same shape as the initial noise.
        """
        timesteps = self._get_sampling_timesteps(bsz=init_noise.shape[0], device=init_noise.device)
        xs: list[Tensor] = []
        x = init_noise
        for times in timesteps:
            pred_noise = func(x, times)
            x_start = self._predict_start_from_noise(x, times, pred_noise)
            pred_mean, _, pred_log_var = self._q_posterior(x_start, x, times)
            new_noise = torch.randn_like(x)
            x = self._p_sample(pred_mean, pred_log_var, new_noise, times)
            xs.append(x)
        return xs


def plot_schedules(*, num_timesteps: int = 1000) -> None:
    """Plots all of the schedules together on one graph.

    Args:
        num_timesteps: The number of timesteps to plot
    """
    try:
        import matplotlib.pyplot as plt  # type: ignore[import]
    except ImportError as e:
        raise ImportError("Please install matplotlib to use this script: `pip install matplotlib`") from e

    plt.figure(figsize=(8, 8))
    time = torch.arange(num_timesteps)
    for schedule in get_args(DiffusionBetaSchedule):
        plt.plot(time, get_diffusion_beta_schedule(schedule, num_timesteps=num_timesteps), label=schedule)
    plt.yscale("log")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # python -m ml.utils.diffusion
    plot_schedules()
