from optionkit.core.factory import create_option, create_model

def test_factory_creates_objects():
    opt = create_option("EuropeanOption", strike=100, maturity=1, is_call=True)
    model = create_model("BlackScholesModel", spot=100, rate=0.05, vol=0.2)
    assert opt.strike == 100
    assert "BlackScholesModel" in repr(model)
