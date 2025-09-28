import math
import warnings
from optionkit.core.tree_model import TreeModel
from optionkit.core.factory import register_model
from optionkit.models.trinomial_schemes import TrinomialSchemes

@register_model("TrinomialTree")
class TrinomialTreeModel(TreeModel):
    """
    Trinomial tree option pricing model.

    Implements a recombining trinomial tree for pricing European-style options
    under the risk-neutral measure. Several parameterization schemes are
    available to match different moments of the underlying asset distribution.

    Parameters
    ----------
    spot : float
        Current spot price of the underlying asset.
    rate : float
        Risk-free continuously compounded interest rate.
    vol : float
        Annualized volatility of the underlying asset.
    steps : int, optional
        Number of time steps in the trinomial tree. Default is 100.
    method : {"boyle", "jr", "tian", "kr"}, optional
        Choice of trinomial parameterization scheme:

        - "boyle" : Boyle (1986) symmetric tree.
          Simple and always stable, but convergence to Black–Scholes is slow.
        - "jr" : Jarrow–Rudd (1983).
          Matches mean and variance, may yield negative probabilities for coarse trees.
        - "tian" : Tian (1993).
          Matches central moments (mean, variance, skewness) for faster convergence.
        - "kr" : Kamrad–Ritchken (1991).
          Generalized scheme; robust, widely used in practice, and the default.

    adaptive : bool, optional
        If True, automatically increase steps until probabilities are valid
        and/or prices converge. Default is False.
    tol : float, optional
        Convergence tolerance for adaptive refinement. Default is 1e-6.
    max_steps : int, optional
        Maximum number of steps to try in adaptive mode. Default is 5000.

    Attributes
    ----------
    u, d, m : float
        Up, down, and middle movement multipliers for stock prices.
    pu, pm, pd : float
        Risk-neutral probabilities of up, middle, and down moves.
    dt : float
        Size of a single time step.

    Notes
    -----
    - The model supports only European-style options via backward induction.
    - For large `steps`, the tree price converges to the Black–Scholes price.
    - Default scheme is `"kr"` since it balances robustness and accuracy.
    """

    def __init__(self, spot: float, rate: float, vol: float,
                 steps: int = 100, method: str = "kr",
                 adaptive: bool = False, tol: float = 1e-6,
                 max_steps: int = 5000):
        super().__init__(steps)
        self.spot = spot
        self.rate = rate
        self.vol = vol
        self.method = method.lower()
        self.adaptive = adaptive
        self.tol = tol
        self.max_steps = max_steps

    # ------------------------------------------------------------------

    def _compute_params(self, dt):
        schemes = {
            "boyle": TrinomialSchemes.boyle,
            "jr": TrinomialSchemes.jarrow_rudd,
            "tian": TrinomialSchemes.tian,
            "kr": TrinomialSchemes.kamrad_ritchken,
        }
        if self.method not in schemes:
            raise ValueError(f"Unknown trinomial scheme: {self.method}")
        return schemes[self.method](self.spot, self.rate, self.vol, dt)

    def _validate_params(self, dt):
        """Check probabilities are valid; return tuple (valid, params)."""
        u, d, m, pu, pm, pd = self._compute_params(dt)
        valid = (0 <= pu <= 1) and (0 <= pm <= 1) and (0 <= pd <= 1)
        return valid, (u, d, m, pu, pm, pd)

    # ------------------------------------------------------------------

    def _build_tree(self, option):
        dt = option.maturity / self.steps
        valid, params = self._validate_params(dt)

        if not valid:
            if self.adaptive:
                # Increase steps until probabilities are valid
                while not valid and self.steps < self.max_steps:
                    self.steps *= 2
                    dt = option.maturity / self.steps
                    valid, params = self._validate_params(dt)

                if not valid:
                    warnings.warn(
                        f"Scheme '{self.method}' failed to produce valid probabilities "
                        f"even with {self.steps} steps. Falling back to 'kr'."
                    )
                    params = TrinomialSchemes.kamrad_ritchken(self.spot, self.rate, self.vol, dt)
            else:
                raise ValueError(
                    f"Scheme '{self.method}' produced invalid probabilities at "
                    f"N={self.steps}, dt={dt:.4e}. Try more steps or method='kr'."
                )

        u, d, m, pu, pm, pd = params
        self.u, self.d, self.m = u, d, m
        self.pu, self.pm, self.pd = pu, pm, pd
        self.dt = dt

        # Build recombining tree with 2t+1 nodes at each level
        tree = [[self.spot]]
        for t in range(1, self.steps + 1):
            level = []
            for j in range(2 * t + 1):
                k = j - t
                price = (
                    self.spot
                    * (u ** max(0, k))
                    * (d ** max(0, -k))
                    * (m ** (t - abs(k)))
                )
                level.append(price)
            tree.append(level)

        return tree

    # ------------------------------------------------------------------

    def _step(self, i, t, payoffs, option):
        """Backward induction step: parent depends on 3 children."""
        disc = math.exp(-self.rate * self.dt)
        down = payoffs[i]
        mid = payoffs[i + 1]
        up = payoffs[i + 2]
        return disc * (self.pu * up + self.pm * mid + self.pd * down)

    # ------------------------------------------------------------------

    def price(self, option):
        """Compute option price, with adaptive refinement if enabled."""
        if not self.adaptive:
            return super().price(option)

        # Adaptive refinement loop
        prev_price = None
        while True:
            price = super().price(option)
            if prev_price is not None and abs(price - prev_price) < self.tol:
                return price
            prev_price = price
            if self.steps >= self.max_steps:
                warnings.warn(
                    f"Adaptive refinement reached max_steps={self.max_steps} "
                    f"without convergence. Returning last price."
                )
                return price
            self.steps *= 2


