from optionkit.payoffs.european import EuropeanOption
from optionkit.models.black_scholes import BlackScholesModel
from optionkit.core.option import Option
from optionkit.core.model import Model

def test_registries_work():
    assert "EuropeanOption" in Option.list_registered()
    assert "BlackScholesModel" in Model.list_registered()
    assert Option.get("EuropeanOption") is EuropeanOption
    assert Model.get("BlackScholesModel") is BlackScholesModel
