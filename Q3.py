from constants import *
from functions import load_json, find_power, production_distribution, select_best_power, co2_emissions, M_CO2


# load temperature profiles (°C)
T_OUT = load_json("temp_out.json")
T_IN_HOUSES = load_json("temp_in_houses.json")
T_IN_OFFICES = load_json("temp_in_offices.json")


# powers (MW)
P4 = find_power(U4, T_IN_HOUSES, T_OUT)
P5 = find_power(U5, T_IN_HOUSES, T_OUT)
P6 = find_power(U6, T_IN_OFFICES, T_OUT)

P = []
for i in range(8760):
    P.append(P4[i]+P5[i]+P6[i])
P_NOM = max(P)


# Evaluation of all the combinations
for i in range(len(NAMES)):
    for j in range(len(NAMES)):
        if j == i:
            pass
        else:
            print("Association between :", NAMES[i], "and", NAMES[j])
            lcoe, P_limit = select_best_power(INVESTMENT_COSTS[i], INVESTMENT_COSTS[j],
                                              MAINTENANCE_COSTS[i], MAINTENANCE_COSTS[j],
                                              EFFICIENCES1[i], EFFICIENCES1[j],
                                              EFFICIENCES2[i], EFFICIENCES2[j],
                                              COMBUSTIBLE_PURCHASE_PRICES[i], COMBUSTIBLE_PURCHASE_PRICES[j],
                                              COMBUSTIBLE_SELL_PRICES[i], COMBUSTIBLE_SELL_PRICES[j],
                                              EMISSION_FACTORS1[i], EMISSION_FACTORS1[j],
                                              EMISSION_FACTORS2[i], EMISSION_FACTORS2[j],
                                              P, P_NOM)
            p1, p2, e1, e2 = production_distribution(P, P_limit/1000)
            emission1 = co2_emissions(
                e1, EFFICIENCES1[i], EMISSION_FACTORS1[i])
            emission2 = co2_emissions(
                e2, EFFICIENCES1[j], EMISSION_FACTORS1[j])
            mco2 = M_CO2(e1, e2, EMISSION_FACTORS1[i], EMISSION_FACTORS1[j],
                         EMISSION_FACTORS2[i], EMISSION_FACTORS2[j], EFFICIENCES1[i], EFFICIENCES1[j],
                         EFFICIENCES2[i], EFFICIENCES2[j])
            print("P1 =", P_limit, "kW and P2 =", P_NOM*1000 - P_limit, "kW")
            try:
                Heq1 = e1/p1
            except ZeroDivisionError:
                Heq1 = 0
            try:
                Heq2 = e2/p2
            except ZeroDivisionError:
                Heq2 = 0
            print("equivalent operational duration, system 1, Heq1 =", Heq1, "h")
            print("equivalent operational duration, system 2, Heq2 =", Heq2, "h")
            print("LCOE =", lcoe, "euros per kWh")
            print("Emission factor, M_CO2 =", mco2, "g per kWh")
            print("CO2 emissions :", (emission1 + emission2) /
                  1000, "Tonnes per year")
            print()


# Analysis

# Some combinations are impossible because one of the system is cheapest no matter the limit power

# The best scenario is with a heat pump for the basis and gaz boiler for the extra
# Compromise to do between LCOE and CO2 emissions.
