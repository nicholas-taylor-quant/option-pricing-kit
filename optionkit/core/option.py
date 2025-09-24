from abc import ABC, abstractmethod
from typing import Dict, Type

class Option(ABC):
    """
    Abstract base class for option contracts.
    Provides registry functionality for all subclasses.
    """

    # Class-level registry for all options
    registry: Dict[str, Type["Option"]] = {}

    def __init_subclass__(cls, **kwargs):
        """Automatically register subclasses by class name."""
        super().__init_subclass__(**kwargs)
        Option.registry[cls.__name__] = cls

    def __init__(self, strike: float, maturity: float, is_call: bool = True):
        self.strike = strike
        self.maturity = maturity
        self.is_call = is_call

    @abstractmethod
    def payoff(self, spot: float) -> float:
        """
        Compute payoff at maturity given spot price.
        Must be implemented by subclasses.
        """
        pass

    def describe(self) -> str:
        """Human-readable description of the contract."""
        kind = "Call" if self.is_call else "Put"
        return f"{kind} Option: strike={self.strike}, maturity={self.maturity}"

    def __repr__(self) -> str:
        return self.describe()

    # --- Class methods for registry usage ---
    @classmethod
    def list_registered(cls):
        """List all registered option types."""
        return list(cls.registry.keys())

    @classmethod
    def get(cls, name: str):
        """Fetch an option class by name."""
        return cls.registry.get(name)

