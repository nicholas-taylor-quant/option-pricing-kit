from optionkit.payoffs.european import EuropeanOption
from optionkit.models.black_scholes import BlackScholesModel

# Define option
option = EuropeanOption(strike=100, maturity=1, is_call=True)

# Define model
model = BlackScholesModel(spot=100, rate=0.05, vol=0.2)

# Price & Greeks
print("Price:", model.price(option))
print("Delta:", model.delta(option))
print("Gamma:", model.gamma(option))
print("Vega:", model.vega(option))
print("Theta:", model.theta(option))
print("Rho:", model.rho(option))
