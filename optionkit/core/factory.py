# optionkit/core/factory.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Type

from .model import Model
from .option import Option

# === Registries ===
MODEL_REGISTRY: Dict[str, Type[Model]] = {}
OPTION_REGISTRY: Dict[str, Type[Option]] = {}

# Small record to trace creations (handy in tests/debug)
@dataclass(slots=True)
class CreationRecord:
    when: datetime
    kind: str          # "model" or "option"
    name: str
    kwargs: Dict[str, Any]

_CREATION_LOG: List[CreationRecord] = []

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
    try:
        cls = MODEL_REGISTRY[name]
    except KeyError:
        raise ValueError(
            f"Model '{name}' not found. Available: {list_models()}"
        )
    _CREATION_LOG.append(CreationRecord(datetime.now(), "model", name, dict(kwargs)))
    return cls(**kwargs)

def create_option(name: str, **kwargs) -> Option:
    """Factory to create an option payoff by name."""
    try:
        cls = OPTION_REGISTRY[name]
    except KeyError:
        raise ValueError(
            f"Option '{name}' not found. Available: {list_options()}"
        )
    _CREATION_LOG.append(CreationRecord(datetime.now(), "option", name, dict(kwargs)))
    return cls(**kwargs)

# === Introspection helpers (pretty + uniform) ===
def list_models() -> List[str]:
    """Return registered model names (sorted)."""
    return sorted(MODEL_REGISTRY.keys())

def list_options() -> List[str]:
    """Return registered option names (sorted)."""
    return sorted(OPTION_REGISTRY.keys())

def describe_registry() -> str:
    """Pretty string for both registries (for logs/CLI/tests)."""
    lines: List[str] = []
    lines.append("Models:")
    for name, cls in sorted(MODEL_REGISTRY.items()):
        lines.append(f"  - {name}: {cls.__module__}.{cls.__name__}")
    lines.append("Options:")
    for name, cls in sorted(OPTION_REGISTRY.items()):
        lines.append(f"  - {name}: {cls.__module__}.{cls.__name__}")
    return "\n".join(lines)

def recent_creations(n: int = 20) -> List[CreationRecord]:
    """Most recent creations (models and options) with kwargs."""
    return _CREATION_LOG[-n:]

