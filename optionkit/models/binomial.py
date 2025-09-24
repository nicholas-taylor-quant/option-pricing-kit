import math
from optionkit.core.model import Model
from optionkit.core.option import Option

class BinomialTreeModel(Model):
    """
    Cox-Ross-Rubinstein binomial tree model.
    Provides Delta and Gamma directly from the tree.
    """

    def __init__(self, spot: float, rate: float, vol: float, steps: int = 100):
        self.spot = spot
        self.rate = rate
        self.vol = vol
        self.steps = steps

    def price(self, option: Option) -> float:
        S, K, T, r, sigma, N = self.spot, option.strike, option.maturity, self.rate, self.vol, self.steps
        dt = T / N
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        q = (math.exp(r * dt) - d) / (u - d)

        # stock prices at maturity
        prices = [S * (u ** j) * (d ** (N - j)) for j in range(N + 1)]
        payoffs = [option.payoff(price) for price in prices]

        # backward induction
        for i in range(N - 1, -1, -1):
            payoffs = [math.exp(-r * dt) * (q * payoffs[j + 1] + (1 - q) * payoffs[j]) for j in range(i + 1)]

        return payoffs[0]

    # ======================
    # Tree-based Greeks
    # ======================
    def delta(self, option: Option) -> float:
        S, K, T, r, sigma, N = self.spot, option.strike, option.maturity, self.rate, self.vol, self.steps
        dt = T / N
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        q = (math.exp(r * dt) - d) / (u - d)

        # Terminal payoffs
        prices = [S * (u ** j) * (d ** (N - j)) for j in range(N + 1)]
        payoffs = [option.payoff(p) for p in prices]

        # Back one step
        V_up = math.exp(-r*dt) * (q*payoffs[-1] + (1-q)*payoffs[-2])
        V_down = math.exp(-r*dt) * (q*payoffs[1] + (1-q)*payoffs[0])

        # Approximate delta from first-step nodes
        S_up = S * u
        S_down = S * d
        return (V_up - V_down) / (S_up - S_down)

    def gamma(self, option: Option) -> float:
        S, K, T, r, sigma, N = self.spot, option.strike, option.maturity, self.rate, self.vol, self.steps
        dt = T / N
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        q = (math.exp(r * dt) - d) / (u - d)

        # Terminal payoffs
        prices = [S * (u ** j) * (d ** (N - j)) for j in range(N + 1)]
        payoffs = [option.payoff(p) for p in prices]

        # Back one step
        V_up = math.exp(-r*dt) * (q*payoffs[-1] + (1-q)*payoffs[-2])
        V_mid = math.exp(-r*dt) * (q*payoffs[-2] + (1-q)*payoffs[1])
        V_down = math.exp(-r*dt) * (q*payoffs[1] + (1-q)*payoffs[0])

        S_up = S * u
        S_mid = S
        S_down = S * d

        delta_up = (V_up - V_mid) / (S_up - S_mid)
        delta_down = (V_mid - V_down) / (S_mid - S_down)

        return (delta_up - delta_down) / ((S_up - S_down)/2)

