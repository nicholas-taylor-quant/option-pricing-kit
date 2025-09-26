import numpy as np
from optionkit.core.model import Model
from optionkit.core.option import Option
from optionkit.core.factory import register_model

@register_model("Heston")
class HestonModel(Model):
    """
    Heston stochastic volatility model.
    Priced via Monte Carlo simulation.
    """

    def __init__(self, spot: float, rate: float, v0: float, kappa: float, theta: float,
                 sigma_v: float, rho: float, steps: int = 200, paths: int = 100_000, seed: int = 42):
        self.spot = spot
        self.rate = rate
        self.v0 = v0          # initial variance
        self.kappa = kappa    # mean reversion speed
        self.theta = theta    # long-run variance
        self.sigma_v = sigma_v  # vol of vol
        self.rho = rho        # correlation between Brownian motions
        self.steps = steps
        self.paths = paths
        self.seed = seed

    def simulate_paths(self, T: float) -> np.ndarray:
        """
        Simulate asset price paths under Heston dynamics.
        Returns array of shape (steps+1, paths).
        """
        np.random.seed(self.seed)
        dt = T / self.steps

        S = np.zeros((self.steps + 1, self.paths))
        v = np.zeros((self.steps + 1, self.paths))
        S[0] = self.spot
        v[0] = self.v0

        # Correlated Brownian increments
        Z1 = np.random.normal(size=(self.steps, self.paths))
        Z2 = np.random.normal(size=(self.steps, self.paths))
        W1 = Z1
        W2 = self.rho * Z1 + np.sqrt(1 - self.rho**2) * Z2

        for t in range(1, self.steps + 1):
            v_prev = np.maximum(v[t-1], 0)  # ensure non-negativity
            v[t] = np.maximum(
                v_prev + self.kappa * (self.theta - v_prev) * dt + self.sigma_v * np.sqrt(v_prev * dt) * W2[t-1],
                0
            )
            S[t] = S[t-1] * np.exp((self.rate - 0.5 * v_prev) * dt + np.sqrt(v_prev * dt) * W1[t-1])

        return S

    def price(self, option: Option) -> float:
        """
        Monte Carlo pricing of a European-style option.
        """
        S_paths = self.simulate_paths(option.maturity)
        S_T = S_paths[-1, :]
        payoffs = [option.payoff(s) for s in S_T]
        return np.exp(-self.rate * option.maturity) * np.mean(payoffs)
