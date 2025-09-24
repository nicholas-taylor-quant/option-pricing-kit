from optionkit.core.option import Option

class DigitalOption(Option):
    """
    Cash-or-nothing digital option.
    """

    def __init__(self, strike: float, maturity: float, is_call: bool = True, payout: float = 1.0):
        super().__init__(strike, maturity, is_call)
        self.payout = payout

    def payoff(self, spot: float) -> float:
        if self.is_call:
            return self.payout if spot > self.strike else 0.0
        else:
            return self.payout if spot < self.strike else 0.0
