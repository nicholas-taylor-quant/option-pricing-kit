from optionkit.payoffs.european import EuropeanOption
from optionkit.models.trinomial import TrinomialTreeModel

def test_trinomial_converges():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = TrinomialTreeModel(spot=100, rate=0.05, vol=0.2, steps=200)
    price = model.price(option)
    # Should be close to Black–Scholes (~10.45)
    assert abs(price - 10.45) < 0.2
