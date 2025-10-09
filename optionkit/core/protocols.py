# optionkit/core/protocols.py
from __future__ import annotations
from typing import Protocol, Sequence, runtime_checkable

@runtime_checkable
class SupportsSpotPayoff(Protocol):
    """
    Protocol for options whose payoff depends on a single terminal spot value.

    Engines that pass terminal spot values (e.g., closed-form Black–Scholes,
    binomial/trinomial trees) can type against this to ensure the option
    implements `payoff(spot: float) -> float`.
    """
    def payoff(self, spot: float) -> float: ...

@runtime_checkable
class SupportsPathPayoff(Protocol):
    """
    Protocol for options whose payoff depends on a price path (sequence of spots).

    Engines that simulate full paths (e.g., Monte Carlo for Asian options)
    can type against this to ensure the option implements
    `payoff(path: Sequence[float]) -> float`.
    """
    def payoff(self, path: Sequence[float]) -> float: ...
