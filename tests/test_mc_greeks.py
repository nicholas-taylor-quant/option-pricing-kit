from optionkit.payoffs.european import EuropeanOption
from optionkit.models.montecarlo import MonteCarloModel

def test_mc_greeks_run():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = MonteCarloModel(spot=100, rate=0.05, vol=0.2, paths=20000, seed=123)

    delta = model.delta(option)
    vega = model.vega(option)
    rho = model.rho(option)

    # Sanity checks
    assert -1 <= delta <= 1
    assert vega > 0
    assert rho > 0
