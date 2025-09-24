import math
from scipy.stats import norm
from optionkit.core.option import Option
from optionkit.core.model import Model

class BlackScholesModel(Model):
    """
    Black–Scholes–Merton pricing model with closed-form Greeks.
    """

    def __init__(self, spot: float, rate: float, vol: float):
        self.spot = spot
        self.rate = rate
        self.vol = vol

    def _d1_d2(self, option: Option):
        S, K, T, r, sigma = self.spot, option.strike, option.maturity, self.rate, self.vol
        d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
        d2 = d1 - sigma*math.sqrt(T)
        return d1, d2

    def price(self, option: Option) -> float:
        S, K, T, r, sigma = self.spot, option.strike, option.maturity, self.rate, self.vol
        d1, d2 = self._d1_d2(option)

        if option.is_call:
            return S * norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2)
        else:
            return K*math.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

    # Closed-form Greeks
    def delta(self, option: Option, **kwargs) -> float:
        d1, _ = self._d1_d2(option)
        return norm.cdf(d1) if option.is_call else norm.cdf(d1) - 1

    def gamma(self, option: Option, **kwargs) -> float:
        d1, _ = self._d1_d2(option)
        return norm.pdf(d1) / (self.spot * self.vol * math.sqrt(option.maturity))

    def vega(self, option: Option, **kwargs) -> float:
        d1, _ = self._d1_d2(option)
        return self.spot * norm.pdf(d1) * math.sqrt(option.maturity)

    def theta(self, option: Option, **kwargs) -> float:
        S, K, T, r, sigma = self.spot, option.strike, option.maturity, self.rate, self.vol
        d1, d2 = self._d1_d2(option)
        pdf_d1 = norm.pdf(d1)

        if option.is_call:
            return -(S * pdf_d1 * sigma) / (2*math.sqrt(T)) - r*K*math.exp(-r*T)*norm.cdf(d2)
        else:
            return -(S * pdf_d1 * sigma) / (2*math.sqrt(T)) + r*K*math.exp(-r*T)*norm.cdf(-d2)

    def rho(self, option: Option, **kwargs) -> float:
        K, T, r = option.strike, option.maturity, self.rate
        _, d2 = self._d1_d2(option)
        if option.is_call:
            return K*T*math.exp(-r*T)*norm.cdf(d2)
        else:
            return -K*T*math.exp(-r*T)*norm.cdf(-d2)

