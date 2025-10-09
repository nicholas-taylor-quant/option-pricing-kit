# optionkit/payoffs/digital.py
from dataclasses import dataclass
from optionkit.core.option import Option
from optionkit.core.factory import register_option

@register_option("DigitalOption")
@dataclass(slots=True, repr=False, eq=True)
class DigitalOption(Option):
    """Cash-or-nothing digital option."""
    payout: float = 1.0

    def payoff(self, spot: float) -> float:
        return self.payout if ((spot > self.strike) if self.is_call else (spot < self.strike)) else 0.0
