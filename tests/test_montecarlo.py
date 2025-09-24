from optionkit.payoffs.european import EuropeanOption
from optionkit.models.montecarlo import MonteCarloModel

def test_mc_pricing_runs():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = MonteCarloModel(spot=100, rate=0.05, vol=0.2, paths=50_000, seed=123)
    price = model.price(option)
    assert price > 0  # sanity check
