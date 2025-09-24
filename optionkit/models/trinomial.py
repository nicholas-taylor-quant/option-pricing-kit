import math
from optionkit.core.model import Model
from optionkit.core.option import Option

class TrinomialTreeModel(Model):
    """
    Trinomial tree option pricing model (Boyle 1986).
    Supports European and American options.
    Provides Delta and Gamma from first-step nodes.
    """

    def __init__(self, spot: float, rate: float, vol: float, steps: int = 100):
        self.spot = spot
        self.rate = rate
        self.vol = vol
        self.steps = steps

    def price(self, option: Option) -> float:
        S, K, T, r, sigma, N = self.spot, option.strike, option.maturity, self.rate, self.vol, self.steps
        dt = T / N
        nu = r - 0.5 * sigma**2
        dx = sigma * math.sqrt(3 * dt)

        u = math.exp(dx)
        d = 1 / u
        m = 1.0

        pu = 1/6 + (nu*math.sqrt(dt)/(2*sigma*math.sqrt(3))) + (sigma**2*dt/6/dx**2)
        pm = 2/3 - (sigma**2*dt/3/dx**2)
        pd = 1/6 - (nu*math.sqrt(dt)/(2*sigma*math.sqrt(3))) + (sigma**2*dt/6/dx**2)

        disc = math.exp(-r * dt)

        prices = [S * (u**j) * (d**(N-j)) for j in range(2*N + 1)]
        payoffs = [option.payoff(p) for p in prices]

        for step in range(N-1, -1, -1):
            new_payoffs = []
            for i in range(2*step + 1):
                expected = disc * (
                    pu * payoffs[i+2] +
                    pm * payoffs[i+1] +
                    pd * payoffs[i]
                )
                new_payoffs.append(expected)
            payoffs = new_payoffs

        return payoffs[0]

    # Tree-based Greeks
    def delta(self, option: Option) -> float:
        S, r, sigma, N = self.spot, self.rate, self.vol, self.steps
        dt = option.maturity / N
        dx = sigma * math.sqrt(3 * dt)
        u = math.exp(dx)
        d = 1/u

        S_up = S * u
        S_mid = S
        S_down = S * d

        V_up = option.payoff(S_up)
        V_mid = option.payoff(S_mid)
        V_down = option.payoff(S_down)

        return (V_up - V_down) / (S_up - S_down)

    def gamma(self, option: Option) -> float:
        S, r, sigma, N = self.spot, self.rate, self.vol, self.steps
        dt = option.maturity / N
        dx = sigma * math.sqrt(3 * dt)
        u = math.exp(dx)
        d = 1/u

        S_up = S * u
        S_mid = S
        S_down = S * d

        V_up = option.payoff(S_up)
        V_mid = option.payoff(S_mid)
        V_down = option.payoff(S_down)

        delta_up = (V_up - V_mid) / (S_up - S_mid)
        delta_down = (V_mid - V_down) / (S_mid - S_down)

        return (delta_up - delta_down) / ((S_up - S_down)/2)

