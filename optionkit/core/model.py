from abc import ABC, abstractmethod
import copy

class Model(ABC):
    """Abstract base for all pricing models."""

    @abstractmethod
    def price(self, option):
        """Return option price."""
        pass

    # ===== Default Greeks (finite difference) =====
    def _fd(self, option, attr, h=1e-4, second=False):
        opt1 = copy.deepcopy(option)
        opt2 = copy.deepcopy(option)

        if second:
            setattr(opt1, attr, getattr(opt1, attr) + h)
            setattr(opt2, attr, getattr(opt2, attr) - h)
            return (self.price(opt1) - 2*self.price(option) + self.price(opt2)) / (h**2)

        setattr(opt1, attr, getattr(opt1, attr) + h)
        return (self.price(opt1) - self.price(option)) / h

    def delta(self, option): return self._fd(option, "spot")
    def gamma(self, option): return self._fd(option, "spot", second=True)
    def vega(self, option): return self._fd(option, "vol")
    def theta(self, option): return -self._fd(option, "maturity")
    def rho(self, option): return self._fd(option, "rate")

