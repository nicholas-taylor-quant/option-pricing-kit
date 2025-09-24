from optionkit.core.option import Option

class EuropeanOption(Option):
    """
    Standard European option.
    """

    def payoff(self, spot: float) -> float:
        return max(spot - self.strike, 0) if self.is_call else max(self.strike - spot, 0)
