import math
from optionkit.core.option import Option
from optionkit.models.black_scholes import BlackScholesModel

class EuropeanOption(Option):
    """
    Simple European option implementation for testing.
    """

    def payoff(self, spot: float) -> float:
        return max(spot - self.strike, 0) if self.is_call else max(self.strike - spot, 0)

def test_call_price():
    model = BlackScholesModel(spot=100, rate=0.05, vol=0.2)
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    price = model.price(option)
    # Reference value ~10.45 for S=100, K=100, r=5%, sigma=20%, T=1
    assert math.isclose(price, 10.45, rel_tol=1e-2)
