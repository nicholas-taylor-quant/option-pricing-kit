import math
from scipy.stats import norm

def d1_d2(S, K, T, r, sigma):
    """Return d1 and d2 for Black-Scholes/Merton-style models."""
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return d1, d2

def discount(r, T):
    return math.exp(-r * T)

def std_norm_cdf(x):
    return norm.cdf(x)
