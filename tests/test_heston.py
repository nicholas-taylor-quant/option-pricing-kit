from optionkit.payoffs.european import EuropeanOption
from optionkit.models.heston import HestonModel

def test_heston_mc_runs():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = HestonModel(
        spot=100, rate=0.05,
        v0=0.04, kappa=2.0, theta=0.04,
        sigma_v=0.2, rho=-0.7,
        steps=100, paths=5000, seed=42
    )
    price = model.price(option)
    assert price > 0  # sanity check
