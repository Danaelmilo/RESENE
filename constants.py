# Energies (MWh/year)
# information
E1 = 5312.50  # old houses red
E2 = 1679.43  # new houses red
E3 = 2730.95  # offices red

E4 = 1232.50  # old houses yellow
E5 = 673.03  # new houses yellow
E6 = 2730.95  # offices yellow

E_RED = E1 + E2 + E3
E_YELLOW = E4 + E5 + E6


# Pipes length (m)
# information
L_RED = 1600
L_YELLOW = 400


# Coefficient U (MW/K), 4 digits round
# computation
U1 = 0.1347
U2 = 0.0426
U3 = 0.0755
U4 = 0.0313
U5 = 0.0171
U6 = 0.0755


# Powers(MW), 4 digits round
# computations
P_RED_NOM = 5.586
P_YELLOW_NOM = 2.736
# Best limit power for the mix heat pump (1) + gas boiler (2)
P_LIM = 0.8023


# heat network
# information
DISTRIBUTION_INVESTMENT = 350 * L_YELLOW  # euros
DISTRIBUTION_MAINTENANCE = 0.05  # % (yearly)

SUBSTATION_NB = 36
SUBSTATION_INVESTMENT_FIXED = 1500 * SUBSTATION_NB  # euros
SUBSTATION_INVESTMENT_VARIABLE = 125  # euros/kW
SUBSTATION_MAINTENANCE = 0.05  # % (yearly)


# temporal data
# information
INTEREST_RATE = 0.035  # (yearly)
LIFESPAN = 25  # years


# Data table for optimization
# information
NAMES = ["gaz boiler", "biomass boiler", "GS heat pump", "Gas CHP"]
INVESTMENT_COSTS = [120, 700, 1570, 1100]  # euros per kW
MAINTENANCE_COSTS = [0.02, 0.025, 0.03, 0.05]  # % of investment costs
EFFICIENCES1 = [1.08, 0.86, 4, 0.56]
EFFICIENCES2 = [1, 1, 1, 0.39]
EMISSION_FACTORS1 = [198, 198, 48, 198]  # g per kWh
# EMISSION_FACTORS1 = [198, 0, 48, 198]  # g per kWh (with biomass = 0)
EMISSION_FACTORS2 = [0, 0, 0, 48]  # g per kWh
COMBUSTIBLE_PURCHASE_PRICES = [0.09, 0.05, 0.11, 0.09]  # euros per kWh
COMBUSTIBLE_SELL_PRICES = [0, 0, 0, 0.14]  # euros per kWh


# Carbon tax
# Choice
TAX = 100  # euros per tonne
