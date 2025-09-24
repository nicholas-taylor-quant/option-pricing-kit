import numpy as np
from optionkit.core.model import Model
from optionkit.core.option import Option

class MonteCarloModel(Model):
    """
    Monte Carlo pricing under GBM dynamics.
    Includes pathwise Greeks estimators.
    """

    def __init__(self, spot: float, rate: float, vol: float, paths: int = 100_000, seed: int = 42):
        self.spot = spot
        self.rate = rate
        self.vol = vol
        self.paths = paths
        self.seed = seed

    def simulate_terminal(self, T: float) -> np.ndarray:
        np.random.seed(self.seed)
        Z = np.random.normal(size=self.paths)
        S0, r, sigma = self.spot, self.rate, self.vol
        ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
        return ST, Z

    def price(self, option: Option) -> float:
        ST, _ = self.simulate_terminal(option.maturity)
        payoffs = np.maximum(ST - option.strike, 0) if option.is_call else np.maximum(option.strike - ST, 0)
        return np.exp(-self.rate * option.maturity) * np.mean(payoffs)

    # ====================
    # Pathwise Greeks
    # ====================
    def delta(self, option: Option, **kwargs) -> float:
        ST, Z = self.simulate_terminal(option.maturity)
        payoff_indicator = (ST > option.strike).astype(float) if option.is_call else -(ST < option.strike).astype(float)
        delta_est = np.exp(-self.rate * option.maturity) * np.mean(payoff_indicator * ST / self.spot)
        return delta_est

    def vega(self, option: Option, **kwargs) -> float:
        ST, Z = self.simulate_terminal(option.maturity)
        payoff_indicator = (ST > option.strike).astype(float) if option.is_call else -(ST < option.strike).astype(float)
        vega_est = np.exp(-self.rate * option.maturity) * np.mean(
            payoff_indicator * ST * (Z * np.sqrt(option.maturity) - self.vol * option.maturity) / self.vol
        )
        return vega_est

    def rho(self, option: Option, **kwargs) -> float:
        ST, Z = self.simulate_terminal(option.maturity)
        payoff = np.maximum(ST - option.strike, 0) if option.is_call else np.maximum(option.strike - ST, 0)
        rho_est = option.maturity * np.exp(-self.rate * option.maturity) * np.mean(payoff)
        return rho_est

    def theta(self, option: Option, **kwargs) -> float:
        ST, Z = self.simulate_terminal(option.maturity)
        payoff = np.maximum(ST - option.strike, 0) if option.is_call else np.maximum(option.strike - ST, 0)
        discounted = np.exp(-self.rate * option.maturity) * np.mean(payoff)
        theta_est = (discounted - self.price(option)) / 1e-4  # crude FD around maturity
        return theta_est

