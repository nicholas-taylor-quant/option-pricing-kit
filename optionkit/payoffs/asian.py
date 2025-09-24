from optionkit.core.option import Option
import numpy as np

class AsianOption(Option):
    """
    Arithmetic average Asian option.
    Payoff depends on the average price of the underlying.
    """

    def payoff(self, path: np.ndarray) -> float:
        """
        path : np.ndarray
            Array of spot prices along the simulated path.
        """
        avg_price = np.mean(path)
        return max(avg_price - self.strike, 0) if self.is_call else max(self.strike - avg_price, 0)
