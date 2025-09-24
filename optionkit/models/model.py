from abc import ABC, abstractmethod
from typing import Dict, Type
from optionkit.core.option import Option

class Model(ABC):
    """
    Abstract base class for all pricing models.
    Provides registry functionality and default finite-difference Greeks.
    """

    # Registry of all subclasses
    registry: Dict[str, Type["Model"]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Model.registry[cls.__name__] = cls

    @abstractmethod
    def price(self, option: Option) -> float:
        """
        Price the given option under this model.
        Must be implemented by subclasses.
        """
        pass

    # ============================
    # Greeks via finite differences
    # ============================
    def delta(self, option: Option, h: float = 1e-4) -> float:
        """Numerical Delta = dPrice/dSpot"""
        S0 = self.spot
        self.spot = S0 + h
        p_up = self.price(option)
        self.spot = S0 - h
        p_dn = self.price(option)
        self.spot = S0
        return (p_up - p_dn) / (2*h)

    def gamma(self, option: Option, h: float = 1e-4) -> float:
        """Numerical Gamma = d²Price/dSpot²"""
        S0 = self.spot
        self.spot = S0 + h
        p_up = self.price(option)
        self.spot = S0
        p0 = self.price(option)
        self.spot = S0 - h
        p_dn = self.price(option)
        self.spot = S0
        return (p_up - 2*p0 + p_dn) / (h**2)

    def vega(self, option: Option, h: float = 1e-4) -> float:
        """Numerical Vega = dPrice/dVol"""
        vol0 = self.vol
        self.vol = vol0 + h
        p_up = self.price(option)
        self.vol = vol0 - h
        p_dn = self.price(option)
        self.vol = vol0
        return (p_up - p_dn) / (2*h)

    def theta(self, option: Option, h: float = 1e-4) -> float:
        """Numerical Theta = -dPrice/dT"""
        T0 = option.maturity
        option.maturity = max(T0 - h, 1e-6)  # avoid negative
        p_shorter = self.price(option)
        option.maturity = T0
        p0 = self.price(option)
        return (p_shorter - p0) / h

    def rho(self, option: Option, h: float = 1e-4) -> float:
        """Numerical Rho = dPrice/dr"""
        r0 = self.rate
        self.rate = r0 + h
        p_up = self.price(option)
        self.rate = r0 - h
        p_dn = self.price(option)
        self.rate = r0
        return (p_up - p_dn) / (2*h)

    # ================
    # Utility methods
    # ================
    def describe(self) -> str:
        return f"{self.__class__.__name__} pricing model"

    def __repr__(self) -> str:
        return self.describe()

    @classmethod
    def list_registered(cls):
        return list(cls.registry.keys())

    @classmethod
    def get(cls, name: str):
        return cls.registry.get(name)
