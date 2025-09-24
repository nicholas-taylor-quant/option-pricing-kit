from optionkit.payoffs.european import EuropeanOption
from optionkit.payoffs.american import AmericanOption
from optionkit.models.binomial import BinomialTreeModel

def test_american_vs_european():
    euro = EuropeanOption(strike=100, maturity=1, is_call=False)  # Put
    amer = AmericanOption(strike=100, maturity=1, is_call=False)

    model = BinomialTreeModel(spot=100, rate=0.05, vol=0.2, steps=500)
    euro_price = model.price(euro)
    amer_price = model.price(amer)

    # American put should never be cheaper than European put
    assert amer_price >= euro_price
