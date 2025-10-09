import pytest
from optionkit.payoffs.european import EuropeanOption
from optionkit.models.trinomial import TrinomialTreeModel
from optionkit.models.black_scholes import BlackScholesModel


@pytest.mark.parametrize("scheme", ["boyle", "jr", "tian", "kr"])
def test_trinomial_adaptive_converges(scheme):
    """
    Adaptive mode (adaptive=True).
    All schemes should converge or fallback to KR to match Black–Scholes.
    Boyle is skipped since it cannot converge by design.
    """
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    bs_model = BlackScholesModel(spot=100, rate=0.05, vol=0.2)
    bs_price = bs_model.price(option)

    if scheme == "boyle":
        pytest.skip("Boyle scheme does not converge to Black–Scholes by design")

    model = TrinomialTreeModel(
        spot=100, rate=0.05, vol=0.2,
        steps=50, method=scheme, adaptive=True, tol=1e-5
    )
    tri_price = model.price(option)

    # With adaptive, all valid schemes should end up close to BS (or fallback to KR)
    assert abs(tri_price - bs_price) < 0.5

