from constants import *


# d and Heq for both areas
d_red = E_RED / L_RED
print("heat density, red area, d_red =", d_red, "MWh/m")

d_yellow = E_YELLOW / L_YELLOW
print("heat density, yellow area, d_yellow =", d_yellow, "MWh/m")
print()


Heq_red = E_RED / P_RED_NOM
print("equivalent operational duration, red area, Heq_red =", Heq_red, "h")

Heq_yellow = E_YELLOW / P_YELLOW_NOM
print("equivalent operational duration, yellow area, Heq_yellow =", Heq_yellow, "h")

# Yellow area is chosen
