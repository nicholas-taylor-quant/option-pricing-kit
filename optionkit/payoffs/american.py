from optionkit.core.option import Option

class AmericanOption(Option):
    """
    American option — exercise allowed any time before maturity.
    Used with tree models (binomial/trinomial).
    """

    def payoff(self, spot: float) -> float:
        return max(spot - self.strike, 0) if self.is_call else max(self.strike - spot, 0)
