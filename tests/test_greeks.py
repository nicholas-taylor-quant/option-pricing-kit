from optionkit.payoffs.european import EuropeanOption
from optionkit.models.black_scholes import BlackScholesModel

def test_bsm_greeks_sanity():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = BlackScholesModel(spot=100, rate=0.05, vol=0.2)

    delta = model.delta(option)
    gamma = model.gamma(option)
    vega = model.vega(option)
    theta = model.theta(option)
    rho = model.rho(option)

    # Sanity checks
    assert -1 <= delta <= 1
    assert gamma > 0
    assert vega > 0
    assert rho > 0
