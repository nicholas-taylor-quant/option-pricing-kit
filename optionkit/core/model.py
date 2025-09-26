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
        model1 = copy.deepcopy(self)
        model2 = copy.deepcopy(self)

        if second:
            setattr(model1, attr, getattr(model1, attr) + h)
            setattr(model2, attr, getattr(model2, attr) - h)
            return (model1.price(option) - 2*self.price(option) + model2.price(option)) / (h**2)

        setattr(model1, attr, getattr(model1, attr) + h)
        return (model1.price(option) - self.price(option)) / h

    def delta(self, option): return self._fd(option, "spot")
    def gamma(self, option): return self._fd(option, "spot", second=True)
    def vega(self, option): return self._fd(option, "vol")
    def theta(self, option):
        opt1 = copy.deepcopy(option)
        opt2 = copy.deepcopy(option)
        opt1.maturity += 1e-4
        opt2.maturity -= 1e-4
        return -(self.price(opt1) - self.price(opt2)) / (2e-4)
    def rho(self, option): return self._fd(option, "rate")

