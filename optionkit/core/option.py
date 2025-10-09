# optionkit/core/option.py
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(slots=True, repr=True, eq=True)
class Option(ABC):
    """
    Abstract base class for option contracts.
    Contains only common fields and UX helpers.
    Registry duties are handled by optionkit.core.factory.
    """
    strike: float
    maturity: float
    is_call: bool = True

    @abstractmethod
    def payoff(self, x, /) -> float:
        """
        Compute payoff given terminal input.

        Conventions:
        - Spot-based options (European, American, Digital) implement payoff(spot: float) -> float
        - Path-based options (Asian) implement payoff(path: Sequence[float]) -> float
        """
        raise NotImplementedError

    def describe(self) -> str:
        kind = "Call" if self.is_call else "Put"
        return f"{kind} Option: strike={self.strike}, maturity={self.maturity}"

    def __repr__(self) -> str:  # optional override for a friendlier string
        return self.describe()

