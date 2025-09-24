from optionkit.core.option import Option
from optionkit.core.model import Model

def create_option(name: str, **kwargs) -> Option:
    """
    Factory to create an option by name.
    Example:
        opt = create_option("EuropeanOption", strike=100, maturity=1, is_call=True)
    """
    cls = Option.get(name)
    if cls is None:
        raise ValueError(f"Option '{name}' not found. Available: {Option.list_registered()}")
    return cls(**kwargs)

def create_model(name: str, **kwargs) -> Model:
    """
    Factory to create a pricing model by name.
    Example:
        model = create_model("BlackScholesModel", spot=100, rate=0.05, vol=0.2)
    """
    cls = Model.get(name)
    if cls is None:
        raise ValueError(f"Model '{name}' not found. Available: {Model.list_registered()}")
    return cls(**kwargs)
