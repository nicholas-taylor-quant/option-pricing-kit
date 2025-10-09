from optionkit.core.option import Option
from optionkit.core.factory import register_option
import numpy as np

@register_option("AsianOption")
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
        avg = float(np.mean(path))
        return max(avg - self.strike, 0.0) if self.is_call else max(self.strike - avg, 0.0)
