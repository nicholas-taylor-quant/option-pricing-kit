from optionkit.payoffs.european import EuropeanOption
from optionkit.core.factory import OPTION_REGISTRY, MODEL_REGISTRY

def test_registries_work():
    assert "EuropeanOption" in OPTION_REGISTRY
    assert "BlackScholes" in MODEL_REGISTRY
    assert OPTION_REGISTRY["EuropeanOption"] is EuropeanOption

