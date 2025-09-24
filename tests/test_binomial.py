from optionkit.payoffs.european import EuropeanOption
from optionkit.models.binomial import BinomialTreeModel

def test_binomial_converges_to_bsm():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = BinomialTreeModel(spot=100, rate=0.05, vol=0.2, steps=500)
    price = model.price(option)
    # Should converge close to BSM value (~10.45)
    assert abs(price - 10.45) < 0.1
