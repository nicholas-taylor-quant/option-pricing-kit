 # optionkit/core/__init__.py
from .model import Model
from .tree_model import TreeModel
from .option import Option
from .protocols import SupportsSpotPayoff, SupportsPathPayoff

from .factory import (
    MODEL_REGISTRY, OPTION_REGISTRY,
    register_model, register_option,
    create_model, create_option,
    list_models, list_options,
    describe_registry, recent_creations,
)

__all__ = [
    "Model", "TreeModel", "Option",
    "SupportsSpotPayoff", "SupportsPathPayoff",
    "MODEL_REGISTRY", "OPTION_REGISTRY",
    "register_model", "register_option",
    "create_model", "create_option",
    "list_models", "list_options",
    "describe_registry", "recent_creations",
]
