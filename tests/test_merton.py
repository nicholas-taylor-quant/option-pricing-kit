from optionkit.payoffs.european import EuropeanOption
from optionkit.models.merton import MertonModel

def test_merton_mc_runs():
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    model = MertonModel(
        spot=100, rate=0.05, vol=0.2,
        lam=0.75, mu_j=-0.5, sigma_j=0.2,
        steps=50, paths=5000, seed=123
    )
    price = model.price(option)
    assert price > 0  # sanity check
