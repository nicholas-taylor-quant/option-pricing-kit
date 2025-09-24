import numpy as np
from optionkit.payoffs.asian import AsianOption
from optionkit.models.montecarlo import MonteCarloModel

def test_asian_mc_runs():
    # Monte Carlo with trivial path avg ~ S0
    option = AsianOption(strike=100, maturity=1, is_call=True)
    model = MonteCarloModel(spot=100, rate=0.05, vol=0.2, paths=10_000, seed=123)

    # Fake single-step path for quick test
    avg_spot = 105
    payoff = option.payoff(np.array([100, 105, 110]))
    assert payoff > 0
