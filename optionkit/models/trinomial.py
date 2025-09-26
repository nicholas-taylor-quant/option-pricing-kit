# optionkit/models/trinomial.py
import math
from optionkit.core.tree_model import TreeModel
from optionkit.core.factory import register_model

@register_model("TrinomialTree")
class TrinomialTreeModel(TreeModel):
    """Trinomial tree option pricing model (Jarrow–Rudd)."""

    def __init__(self, spot: float, rate: float, vol: float, steps: int = 100):
        super().__init__(steps)
        self.spot = spot
        self.rate = rate
        self.vol = vol

    def _build_tree(self, option):
        dt = option.maturity / self.steps
        v = self.vol
        r = self.rate

        # Boyle (1986) symmetric trinomial
        u = math.exp(v * math.sqrt(2 * dt))
        d = 1 / u
        m = 1.0

        pu = 1.0 / 6.0
        pm = 2.0 / 3.0
        pd = 1.0 / 6.0

        self.u, self.d, self.m = u, d, m
        self.pu, self.pm, self.pd = pu, pm, pd
        self.dt = dt

        # Recombining trinomial tree: 2t+1 nodes at time t
        tree = [[0.0 for _ in range(2 * i + 1)] for i in range(self.steps + 1)]
        tree[0][0] = self.spot

        for t in range(1, self.steps + 1):
            for j in range(2 * t + 1):
                k = j - t
                tree[t][j] = self.spot * (u ** max(0, k)) * (d ** max(0, -k))

        return tree


    def _step(self, i, t, payoffs, option):
        """Backward induction with trinomial probabilities."""
        disc = math.exp(-self.rate * self.dt)

        down = payoffs[i] if i == 0 else payoffs[i - 1]
        mid = payoffs[i]
        up = payoffs[i + 1] if i + 1 < len(payoffs) else payoffs[i]

        return disc * (self.pu * up + self.pm * mid + self.pd * down)



