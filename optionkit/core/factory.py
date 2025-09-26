# optionkit/core/factory.py
from typing import Type
from optionkit.core.model import Model
from optionkit.core.option import Option

# === Registries ===
MODEL_REGISTRY = {}
OPTION_REGISTRY = {}

# === Decorators ===
def register_model(name: str):
    """Decorator to register a pricing model class."""
    def decorator(cls: Type[Model]):
        MODEL_REGISTRY[name] = cls
        return cls
    return decorator

def register_option(name: str):
    """Decorator to register an option payoff class."""
    def decorator(cls: Type[Option]):
        OPTION_REGISTRY[name] = cls
        return cls
    return decorator

# === Factory functions ===
def create_model(name: str, **kwargs) -> Model:
    """Factory to create a pricing model by name."""
    if name not in MODEL_REGISTRY:
        raise ValueError(
            f"Model '{name}' not found. Available: {list(MODEL_REGISTRY.keys())}"
        )
    return MODEL_REGISTRY[name](**kwargs)

def create_option(name: str, **kwargs) -> Option:
    """Factory to create an option payoff by name."""
    if name not in OPTION_REGISTRY:
        raise ValueError(
            f"Option '{name}' not found. Available: {list(OPTION_REGISTRY.keys())}"
        )
    return OPTION_REGISTRY[name](**kwargs)
