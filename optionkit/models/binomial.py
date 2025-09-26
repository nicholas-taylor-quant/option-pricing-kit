# optionkit/models/binomial.py
import math
from optionkit.core.tree_model import TreeModel
from optionkit.core.factory import register_model

@register_model("BinomialTree")
class BinomialTreeModel(TreeModel):
    """Binomial tree option pricing model."""

    def __init__(self, spot: float, rate: float, vol: float, steps: int = 100):
        super().__init__(steps)
        self.spot = spot
        self.rate = rate
        self.vol = vol

    def _build_tree(self, option):
        dt = option.maturity / self.steps
        u = math.exp(self.vol * math.sqrt(dt))
        d = 1 / u
        q = (math.exp(self.rate * dt) - d) / (u - d)

        tree = [[0] * (i + 1) for i in range(self.steps + 1)]
        tree[0][0] = self.spot
        for i in range(1, self.steps + 1):
            for j in range(i + 1):
                tree[i][j] = self.spot * (u ** j) * (d ** (i - j))
        self.u, self.d, self.q, self.dt = u, d, q, dt
        return tree

    def _step(self, i, t, payoffs, option):
        # backward induction step
        return math.exp(-self.rate * self.dt) * (
            self.q * payoffs[i + 1] + (1 - self.q) * payoffs[i]
        )

