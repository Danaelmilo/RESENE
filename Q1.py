import matplotlib.pyplot as plt

from constants import *
from functions import load_json, find_coef_U, find_power


# load temperature profiles (°C)
T_OUT = load_json("temp_out.json")
T_IN_HOUSES = load_json("temp_in_houses.json")
T_IN_OFFICES = load_json("temp_in_offices.json")


# U
U1 = find_coef_U(E1, T_IN_HOUSES, T_OUT, 1)
U2 = find_coef_U(E2, T_IN_HOUSES, T_OUT, 1)
U3 = find_coef_U(E3, T_IN_OFFICES, T_OUT, 1)
U4 = find_coef_U(E4, T_IN_HOUSES, T_OUT, 1)
U5 = find_coef_U(E5, T_IN_HOUSES, T_OUT, 1)
U6 = find_coef_U(E6, T_IN_OFFICES, T_OUT, 1)
print("U for red buildings (MW/K)")
print(U1, U2, U3)
print("U for yellow buildings (MW/K)")
print(U4, U5, U6)
print()


# powers
# compute power evolution among time for each type of building and area
P1 = find_power(U1, T_IN_HOUSES, T_OUT)
P2 = find_power(U2, T_IN_HOUSES, T_OUT)
P3 = find_power(U3, T_IN_OFFICES, T_OUT)
P4 = find_power(U4, T_IN_HOUSES, T_OUT)
P5 = find_power(U5, T_IN_HOUSES, T_OUT)
P6 = find_power(U6, T_IN_HOUSES, T_OUT)

P_red = []
for i in range(8760):
    P_red.append(P1[i]+P2[i]+P3[i])
P_RED_NOM = max(P_red)

P_yellow = []
for i in range(8760):
    P_yellow.append(P4[i]+P5[i]+P6[i])
P_YELLOW_NOM = max(P_yellow)

print("Nominal power, red area, P_RED_NOM =", P_RED_NOM, "MW")
print("Nominal power, yellow area, P_YELLOW_NOM =", P_YELLOW_NOM, "MW")


# plot (yellow area)
X = [k for k in range(8760)]
# P = f(t)
plt.plot(X, P_yellow)
plt.title("Demande de puissance en fonction du temps, \n secteur jaune", size=19)
plt.xlabel("Temps [h]", size=16)
plt.ylabel("Puissance [MW]", size=16)
plt.grid()
plt.savefig("Pjaune-temps.pdf")
plt.show()

# P = f(T)
plt.plot(T_OUT, P_yellow, ":")
plt.title("Demande en fonction de la température, \n secteur jaune", size=19)
plt.xlabel("Température [°C]", size=16)
plt.ylabel("Puissance [MW]", size=16)
plt.grid()
plt.savefig("Pjaune-température.pdf")
plt.show()

# T = f(t)
plt.plot(X, T_OUT)
plt.title("Température extérieure \n au cours de l'année", size=19)
plt.xlabel("Temps [h]", size=16)
plt.ylabel("Température extérieure [°C]", size=16)
plt.grid()
plt.savefig("Température.pdf")
plt.show()

# P = f(t*)
P_yellow.sort(reverse=True)
plt.plot(X, P_yellow, linewidth=3)
plt.title("Monotone de puissance, \n secteur jaune", size=19)
plt.xlabel("Temps* [h]", size=16)
plt.ylabel("Puissance [MW]", size=16)
plt.grid()
plt.savefig("Pjaune-monotone.pdf")
plt.show()
