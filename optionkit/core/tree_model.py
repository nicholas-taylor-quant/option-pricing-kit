from .model import Model

class TreeModel(Model):
    """Generic tree scaffold for binomial/trinomial-like models."""

    def __init__(self, steps=100):
        self.steps = steps

    def _build_tree(self, option):
        """Each subclass must return a 2D tree of stock prices."""
        raise NotImplementedError

    def _payoff(self, stock_price, option):
        return option.payoff(stock_price)

    def price(self, option):
        tree = self._build_tree(option)
        payoffs = [self._payoff(s, option) for s in tree[-1]]
        # backward induction
        for t in range(len(tree) - 2, -1, -1):
            payoffs = [self._step(i, t, payoffs, option) for i in range(len(tree[t]))]
        return payoffs[0]

    def _step(self, i, t, payoffs, option):
        """Discount expected payoff at node i,t."""
        raise NotImplementedError
