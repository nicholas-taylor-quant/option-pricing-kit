import numpy as np
from optionkit.core.model import Model
from optionkit.core.option import Option
from optionkit.core.factory import register_model

@register_model("Merton")
class MertonModel(Model):
    """
    Merton jump-diffusion model.
    Priced via Monte Carlo simulation.
    """

    def __init__(self, spot: float, rate: float, vol: float,
                 lam: float, mu_j: float, sigma_j: float,
                 steps: int = 200, paths: int = 100_000, seed: int = 42):
        """
        lam    : jump intensity (expected # jumps per year)
        mu_j   : mean jump size (lognormal mean)
        sigma_j: jump volatility
        """
        self.spot = spot
        self.rate = rate
        self.vol = vol
        self.lam = lam
        self.mu_j = mu_j
        self.sigma_j = sigma_j
        self.steps = steps
        self.paths = paths
        self.seed = seed

    def simulate_paths(self, T: float) -> np.ndarray:
        np.random.seed(self.seed)
        dt = T / self.steps

        S = np.zeros((self.steps + 1, self.paths))
        S[0] = self.spot

        for t in range(1, self.steps + 1):
            Z = np.random.normal(size=self.paths)
            N_jumps = np.random.poisson(self.lam * dt, size=self.paths)

            jump_sizes = np.exp(self.mu_j * N_jumps + self.sigma_j * np.sqrt(N_jumps) * np.random.normal(size=self.paths))

            drift = (self.rate - 0.5 * self.vol**2 - self.lam * (np.exp(self.mu_j + 0.5*self.sigma_j**2) - 1)) * dt
            diffusion = self.vol * np.sqrt(dt) * Z

            S[t] = S[t-1] * np.exp(drift + diffusion) * jump_sizes

        return S

    def price(self, option: Option) -> float:
        S_paths = self.simulate_paths(option.maturity)
        S_T = S_paths[-1, :]
        payoffs = [option.payoff(s) for s in S_T]
        return np.exp(-self.rate * option.maturity) * np.mean(payoffs)
