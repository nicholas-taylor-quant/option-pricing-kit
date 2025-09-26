import math
from scipy.stats import norm
from optionkit.core.model import Model
from optionkit.core.math_utils import d1_d2, discount
from optionkit.core.factory import register_model

@register_model("BlackScholes")
class BlackScholesModel(Model):
    """Black-Scholes-Merton closed-form pricing with Greeks."""

    def __init__(self, spot: float, rate: float, vol: float):
        self.spot = spot
        self.rate = rate
        self.vol = vol

    def price(self, option):
        S, K, T, r, sigma = self.spot, option.strike, option.maturity, self.rate, self.vol
        d1, d2 = d1_d2(S, K, T, r, sigma)
        if option.is_call:
            return S * norm.cdf(d1) - K * discount(r, T) * norm.cdf(d2)
        else:
            return K * discount(r, T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    # override Greeks for closed form
    def delta(self, option):
        d1, _ = d1_d2(self.spot, option.strike, option.maturity, self.rate, self.vol)
        return norm.cdf(d1) if option.is_call else norm.cdf(d1) - 1


