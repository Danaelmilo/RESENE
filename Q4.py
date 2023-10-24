import matplotlib.pyplot as plt

from constants import *
from functions import load_json, find_power, compute_lcoe


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


# compute the LCOE for different powers
P_limit = []
Cost = []
n = 1000

for k in range(n+1):
    P_double_system = P_NOM*k/n
    lcoe = compute_lcoe(INVESTMENT_COSTS[2], INVESTMENT_COSTS[0],
                        MAINTENANCE_COSTS[2], MAINTENANCE_COSTS[0],
                        EFFICIENCES1[2], EFFICIENCES1[0],
                        EFFICIENCES2[2], EFFICIENCES2[0],
                        COMBUSTIBLE_PURCHASE_PRICES[2], COMBUSTIBLE_PURCHASE_PRICES[0],
                        COMBUSTIBLE_SELL_PRICES[2], COMBUSTIBLE_SELL_PRICES[0],
                        EMISSION_FACTORS1[2], EMISSION_FACTORS1[0],
                        EMISSION_FACTORS2[2], EMISSION_FACTORS2[0],
                        P, P_NOM, P_double_system)
    P_limit.append(P_double_system*1000)
    Cost.append(lcoe)

min_lcoe = min(Cost)
index = Cost.index(min_lcoe)
best_P = P_limit[index]
print("P1 =", best_P, "kW and P2 =", P_NOM*1000 - best_P, "kW")
print("LCOE =", min_lcoe, "euros per kWh")


# plot
# LCOE = f(P)
plt.plot(P_limit, Cost)
plt.title("Coût actualisé de l'énergie en fonction de la puissance limite", size=19)
plt.xlabel("Puissance [kW]", size=16)
plt.ylabel("Coût [euros/kWh]", size=16)
plt.grid()
plt.savefig("LCOE.pdf")
plt.show()


# On this graph, we can clearly see a minimum on the cost function
