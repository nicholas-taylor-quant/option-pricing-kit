import pytest

from optionkit.core import (
    OPTION_REGISTRY,
    MODEL_REGISTRY,
    register_option,
    register_model,
    create_option,
    create_model,
    list_options,
    list_models,
    describe_registry,
    recent_creations,
)

# import concrete classes
from optionkit.payoffs import EuropeanOption
from optionkit.payoffs import AmericanOption
from optionkit.payoffs import AsianOption
from optionkit.payoffs import DigitalOption

from optionkit.models import BlackScholesModel
from optionkit.models import HestonModel
from optionkit.models import MertonModel
from optionkit.models import MonteCarloModel
from optionkit.models import BinomialTreeModel
from optionkit.models import TrinomialTreeModel


def test_registries_have_expected_entries():
    # Names present
    for name in ["EuropeanOption", "AmericanOption", "AsianOption", "DigitalOption"]:
        assert name in OPTION_REGISTRY

    for name in ["BlackScholes", "Heston", "Merton", "MonteCarlo", "BinomialTree", "TrinomialTree"]:
        assert name in MODEL_REGISTRY

    # Identity checks
    assert OPTION_REGISTRY["EuropeanOption"] is EuropeanOption
    assert OPTION_REGISTRY["AmericanOption"] is AmericanOption
    assert OPTION_REGISTRY["AsianOption"] is AsianOption
    assert OPTION_REGISTRY["DigitalOption"] is DigitalOption

    assert MODEL_REGISTRY["BlackScholes"] is BlackScholesModel
    assert MODEL_REGISTRY["Heston"] is HestonModel
    assert MODEL_REGISTRY["Merton"] is MertonModel
    assert MODEL_REGISTRY["MonteCarlo"] is MonteCarloModel
    assert MODEL_REGISTRY["BinomialTree"] is BinomialTreeModel
    assert MODEL_REGISTRY["TrinomialTree"] is TrinomialTreeModel


def test_list_and_describe_helpers_are_sane():
    opts = list_options()
    mods = list_models()
    assert "EuropeanOption" in opts and "DigitalOption" in opts
    assert "BlackScholes" in mods and "TrinomialTree" in mods

    txt = describe_registry()
    # Basic shape check
    assert "Models:" in txt and "Options:" in txt
    assert "BlackScholes" in txt and "EuropeanOption" in txt


def test_factory_creates_objects_and_traces():
    # Create via factory
    opt = create_option("EuropeanOption", strike=100, maturity=1.0, is_call=True)
    mdl = create_model("BlackScholes", spot=100, rate=0.05, vol=0.2)

    # Object sanity
    assert isinstance(opt, EuropeanOption)
    assert opt.strike == 100 and opt.is_call is True

    # repr should include class name and some params (Model.__repr__ helper)
    r = repr(mdl)
    assert "BlackScholes" in r
    assert ("spot" in r) or ("rate" in r) or ("vol" in r)

    # creation log recorded both
    log = recent_creations(5)
    kinds = [rec.kind for rec in log[-2:]]
    assert set(kinds) == {"option", "model"}


def test_factory_error_messages_are_helpful():
    with pytest.raises(ValueError) as e1:
        create_option("NopeOption", strike=100, maturity=1.0)
    assert "Available:" in str(e1.value)

    with pytest.raises(ValueError) as e2:
        create_model("NopeModel")
    assert "Available:" in str(e2.value)


def test_digital_option_dataclass_behaviour():
    a = DigitalOption(strike=100, maturity=1.0, is_call=True, payout=5.0)
    b = DigitalOption(strike=100, maturity=1.0, is_call=True, payout=5.0)
    c = DigitalOption(strike=100, maturity=1.0, is_call=False, payout=5.0)

    # eq=True from dataclass → structural equality on fields
    assert a == b
    assert a != c

    # repr from Option override should be friendly
    assert "Option: strike=100" in repr(a)


# --- Protocol checks (static + optional runtime) ---
def test_protocol_runtime_guards_optional():
    from optionkit.core.protocols import SupportsSpotPayoff, SupportsPathPayoff
    from optionkit.payoffs.european import EuropeanOption
    from optionkit.payoffs.asian import AsianOption

    e = EuropeanOption(strike=100, maturity=1.0, is_call=True)
    a = AsianOption(strike=100, maturity=1.0, is_call=True)

    assert isinstance(e, SupportsSpotPayoff)
    assert isinstance(a, SupportsPathPayoff)

def test_example_payoffs_behave_reasonably():
    e_call = EuropeanOption(strike=100, maturity=1.0, is_call=True)
    e_put = EuropeanOption(strike=100, maturity=1.0, is_call=False)

    assert e_call.payoff(spot=120) == 20.0
    assert e_call.payoff(spot=80) == 0.0
    assert e_put.payoff(spot=80) == 20.0
    assert e_put.payoff(spot=120) == 0.0

    d = DigitalOption(strike=100, maturity=1.0, is_call=True, payout=7.5)
    assert d.payoff(spot=101) == 7.5
    assert d.payoff(spot=99) == 0.0

    a = AsianOption(strike=100, maturity=1.0, is_call=True)
    assert a.payoff([100, 100, 100]) == 0.0
    assert a.payoff([90, 110, 120]) > 0.0
