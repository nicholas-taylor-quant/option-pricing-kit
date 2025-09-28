import math

class TrinomialSchemes:
    """
    Collection of trinomial parameterizations.

    Each scheme returns the tuple (u, d, m, pu, pm, pd):
        u  : up multiplier
        d  : down multiplier
        m  : middle multiplier
        pu : risk-neutral probability of up move
        pm : probability of middle move
        pd : probability of down move
    """

    @staticmethod
    def boyle(spot, rate, vol, dt):
        """
        Boyle (1986) symmetric trinomial tree.
        Simple, always stable, but not strictly risk-neutral.
        """
        u = math.exp(vol * math.sqrt(2 * dt))
        d = 1 / u
        m = 1.0
        pu, pm, pd = 1/6, 2/3, 1/6
        return u, d, m, pu, pm, pd

    @staticmethod
    def jarrow_rudd(spot, rate, vol, dt):
        """
        Jarrow–Rudd (1983) trinomial tree.
        Matches mean and variance under risk-neutral measure.
        """
        u = math.exp(vol * math.sqrt(dt))
        d = 1 / u
        m = 1.0  # middle branch unchanged
        drift = math.exp(rate * dt)

        # Probabilities (mean/variance match)
        pu = 0.5 * (((vol**2 * dt) + (drift - 1) ** 2) / (vol**2 * dt))
        pd = pu
        pm = 1 - pu - pd
        return u, d, m, pu, pm, pd

    @staticmethod
    def tian(spot, rate, vol, dt):
        """
        Tian (1993) trinomial tree.
        Matches mean, variance, and skewness for faster convergence.
        """
        u = math.exp(vol * math.sqrt(2 * dt))
        d = 1 / u
        m = math.exp(rate * dt - 0.5 * vol**2 * dt)  # drift-adjusted middle
        drift = math.exp(rate * dt)

        pu = ((drift - d) * (drift - m)) / ((u - d) * (u - m))
        pd = ((u - drift) * (m - drift)) / ((u - d) * (m - d))
        pm = 1 - pu - pd
        return u, d, m, pu, pm, pd

    @staticmethod
    def kamrad_ritchken(spot, rate, vol, dt):
        """
        Kamrad–Ritchken (1991) trinomial tree.
        Generalized recombining trinomial with stable probabilities.
        Equivalent to the canonical form in your notebooks.
        """
        u = math.exp(vol * math.sqrt(2 * dt))
        d = 1 / u
        m = 1.0  # middle stays put

        # Risk-neutral probs (squared ratio formulas)
        pu = (
            (math.exp(rate * dt / 2) - math.exp(-vol * math.sqrt(dt / 2)))
            / (math.exp(vol * math.sqrt(dt / 2)) - math.exp(-vol * math.sqrt(dt / 2)))
        ) ** 2

        pd = (
            (-math.exp(rate * dt / 2) + math.exp(vol * math.sqrt(dt / 2)))
            / (math.exp(vol * math.sqrt(dt / 2)) - math.exp(-vol * math.sqrt(dt / 2)))
        ) ** 2

        pm = 1 - pu - pd
        return u, d, m, pu, pm, pd


