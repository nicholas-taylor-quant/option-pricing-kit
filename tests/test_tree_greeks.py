from optionkit.payoffs.european import EuropeanOption
from optionkit.models.binomial import BinomialTreeModel
from optionkit.models.trinomial import TrinomialTreeModel

def test_binomial_greeks():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = BinomialTreeModel(spot=100, rate=0.05, vol=0.2, steps=200)
    delta = model.delta(option)
    gamma = model.gamma(option)
    assert -1 <= delta <= 1
    assert gamma > 0

def test_trinomial_greeks():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = TrinomialTreeModel(spot=100, rate=0.05, vol=0.2, steps=200)
    delta = model.delta(option)
    gamma = model.gamma(option)
    assert -1 <= delta <= 1
    assert gamma > 0
