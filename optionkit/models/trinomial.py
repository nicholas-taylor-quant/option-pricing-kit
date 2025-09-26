# optionkit/models/trinomial.py
import math
from optionkit.core.tree_model import TreeModel
from optionkit.core.factory import register_model

@register_model("TrinomialTree")
class TrinomialTreeModel(TreeModel):
    """Trinomial tree option pricing model."""

    def __init__(self, spot: float, rate: float, vol: float, steps: int = 100):
        super().__init__(steps)
        self.spot = spot
        self.rate = rate
        self.vol = vol

    def _build_tree(self, option):
        """
        Build stock price tree.
        Each node has 3 branches: up, middle, down.
        """
        dt = option.maturity / self.steps
        dx = self.vol * math.sqrt(3 * dt)

        u = math.exp(dx)   # up
        d = math.exp(-dx)  # down
        m = 1.0            # middle

        pu = 1/6 + (self.rate - 0.5*self.vol**2) * math.sqrt(dt/(12*self.vol**2))
        pm = 2/3
        pd = 1 - pu - pm

        self.u, self.d, self.m = u, d, m
        self.pu, self.pm, self.pd = pu, pm, pd
        self.dt = dt

        # build tree structure
        tree = [[self.spot * (u**j) * (d**(i-j)) for j in range(i+1)] for i in range(self.steps+1)]
        return tree

    def _step(self, i, t, payoffs, option):
        """
        Backward induction step:
        discount expected payoff with trinomial probabilities.
        """
        # Trinomial: payoffs[i-1], payoffs[i], payoffs[i+1]
        # Need to guard array edges.
        pu, pm, pd = self.pu, self.pm, self.pd
        disc = math.exp(-self.rate * self.dt)

        down = payoffs[i] if i == 0 else payoffs[i-1]
        mid  = payoffs[i]
        up   = payoffs[i+1] if i+1 < len(payoffs) else payoffs[i]

        return disc * (pu*up + pm*mid + pd*down)


