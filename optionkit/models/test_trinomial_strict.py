import pytest
from optionkit.payoffs.european import EuropeanOption
from optionkit.models.trinomial import TrinomialTreeModel
from optionkit.models.black_scholes import BlackScholesModel


@pytest.mark.parametrize("scheme", ["boyle", "jr", "tian", "kr"])
def test_trinomial_strict(scheme):
    """
    Strict mode (adaptive=False).
    Tests each scheme at N=500 and documents expected quirks.
    """
    option = EuropeanOption(strike=100, maturity=1, is_call=True)
    bs_model = BlackScholesModel(spot=100, rate=0.05, vol=0.2)
    bs_price = bs_model.price(option)

    if scheme == "kr":
        model = TrinomialTreeModel(spot=100, rate=0.05, vol=0.2,
                                   steps=500, method=scheme, adaptive=False)
        tri_price = model.price(option)
        assert abs(tri_price - bs_price) < 0.2  # KR is robust
    elif scheme == "boyle":
        model = TrinomialTreeModel(spot=100, rate=0.05, vol=0.2,
                                   steps=500, method=scheme, adaptive=False)
        tri_price = model.price(option)
        assert tri_price < bs_price  # Boyle underprices
    elif scheme in {"jr", "tian"}:
        model = TrinomialTreeModel(spot=100, rate=0.05, vol=0.2,
                                   steps=500, method=scheme, adaptive=False)
        with pytest.raises(ValueError):
            _ = model.price(option)  # expected to fail with invalid probs
