import json

from constants import *


def load_json(file):
    # used to load temperature profiles
    with open(file, "r") as f:
        return json.load(f)


def find_coef_U(Energie, Tin, Tout, deltat):
    # coefficient U of proportionnality between the power and the temperature delta (MW/K)
    somme = 0
    for k in range(8760):
        tout = Tout[k]
        tin = Tin[k]
        somme += max(0, deltat * (tin - tout))
    U = Energie / somme
    return U


def find_power(U, Tin, Tout):
    # P is the list of powers among time, over one year (MW)
    P = []
    for k in range(8760):
        tout = Tout[k]
        tin = Tin[k]
        P.append(max(0, U*(tin - tout)))
    return P


def find_energy(P1, P2, power_function):
    # computes an area and return the yearly energy (MWh)
    E = 0
    for t in range(len(power_function)):
        if (power_function[t] - P1) >= P2 - P1:
            E += P2 - P1
        else:
            E += power_function[t] - P1
    return E


def production_distribution(P, P_limit):
    # P is the comsuption profile over the year
    # P_limit is the nominal capacity of the basis system
    # computation of the instantaneous power (MW) for each subsystem and the corresponding energy (MWh/year)
    P_subsystem1 = []
    P_subsystem2 = []
    for p in P:
        p_subsystem1 = min(p, P_limit)
        p_subsystem2 = max(0, p - P_limit)
        P_subsystem1.append(p_subsystem1)
        P_subsystem2.append(p_subsystem2)

    Annual_heat1 = 0
    Annual_heat2 = 0
    for i in range(len(P_subsystem1)):
        Annual_heat1 += P_subsystem1[i] * 1
        Annual_heat2 += P_subsystem2[i] * 1
    return (max(P_subsystem1), max(P_subsystem2), Annual_heat1, Annual_heat2)


def co2_emissions(energy, efficiency, emission_factor):
    # in g per year
    return energy * emission_factor / efficiency


# cost functions
# computations
# intermediate functions to compute the LCOE

def capex_network(power):
    # sum of the investment costs for the heat distribution network (euros)
    return (DISTRIBUTION_INVESTMENT + SUBSTATION_INVESTMENT_FIXED +
            SUBSTATION_INVESTMENT_VARIABLE * power)


def capex_subsystem(investment_cost, power):
    # sum of the investment costs for a production subsystem (euros)
    return investment_cost * power


def opex_network(power):
    # sum of the operationnal costs for the heat distribution network (euros)
    return (DISTRIBUTION_MAINTENANCE * DISTRIBUTION_INVESTMENT +
            SUBSTATION_MAINTENANCE * (SUBSTATION_INVESTMENT_FIXED + SUBSTATION_INVESTMENT_VARIABLE * power))


def opex_subsytem(investment_cost, power, maintenance):
    # sum of the operationnal costs for a production subsystem (euros)
    return maintenance * investment_cost * power


def variable_cost(energy, efficiency1, efficiency2,
                  combustible_purchase_price, combustible_sell_price):
    # sum of the variable costs necessary for the production (euros)
    return (energy / efficiency1 * combustible_purchase_price -
            energy / efficiency1 * efficiency2 * combustible_sell_price)


def carbon_tax(energy, efficiency, emission_factor, price):
    # we put a price (carbon tax) on co2 emission to integrate it for the LCOE
    # the result is a price in euros
    return co2_emissions(energy, efficiency, emission_factor) * price / 1000000


def M_CO2(Eb1, Eb2, CO2_11, CO2_12, CO2_21, CO2_22, r11, r12, r21, r22):
    # computation of CO2 from the energy consumed by the buildings, Ebi is supplied to the building by the system i
    M = (Eb1*(CO2_11/r11 + CO2_21/r21) +
         Eb2*(CO2_12/r12 + CO2_22/r22)) / (Eb1+Eb2)
    return M


def levelization(cost):
    # the cost is levelized over the years (euros)
    somme = 0
    for k in range(1, LIFESPAN+1):
        somme += cost / (1 + INTEREST_RATE)**k
    return somme


def compute_lcoe(investment_cost1, investment_cost2, maintenance1, maintenance2,
                 efficiency11, efficiency12, efficiency21, efficiency22,
                 combustible_purchase_price1, combustible_purchase_price2,
                 combustible_sell_price1, combustible_sell_price2,
                 emission_factor11, emission_factor12, emission_factor21, emission_factor22,
                 P, P_nom, P_double_system):

    P1_nom, P2_nom, E_system1, E_system2 = production_distribution(
        P, P_double_system)  # power and energy repartition between the two subsystems
    P_nom *= 1000  # kW
    P_double_system *= 1000  # kW
    P1_nom *= 1000  # kW
    P2_nom *= 1000  # kW
    E_system1 *= 1000  # kWh
    E_system2 *= 1000  # kWh

    capex0 = capex_network(P_nom)
    capex1 = capex_subsystem(investment_cost1, P1_nom)
    capex2 = capex_subsystem(investment_cost2, P2_nom)
    CAPEX = capex0 + capex1 + capex2

    opex0 = opex_network(P_nom)
    opex1 = opex_subsytem(investment_cost1, P1_nom, maintenance1)
    opex2 = opex_subsytem(investment_cost2, P2_nom, maintenance2)
    OPEX = opex0 + opex1 + opex2

    variable1 = variable_cost(E_system1, efficiency11, efficiency21,
                              combustible_purchase_price1, combustible_sell_price1)
    variable2 = variable_cost(E_system2, efficiency12, efficiency22,
                              combustible_purchase_price2, combustible_sell_price2)
    VARIABLE = variable1 + variable2

    ENERGY = E_system1 + E_system2

    emission11 = carbon_tax(E_system1, efficiency11, emission_factor11, TAX)
    emission12 = carbon_tax(E_system2, efficiency12, emission_factor12, TAX)
    emission21 = carbon_tax(E_system1, efficiency11 /
                            efficiency21, emission_factor21, TAX)
    emission22 = carbon_tax(E_system2, efficiency12 /
                            efficiency22, emission_factor22, TAX)
    EMISSION = emission11 + emission12 + emission21 + emission22

    # LCOE with or without the carbon tax
    LCOE = (CAPEX + levelization(OPEX) +
            levelization(VARIABLE)) / levelization(ENERGY)
    '''LCOE = (CAPEX + levelization(OPEX) +
            levelization(VARIABLE) + levelization(EMISSION)) / levelization(ENERGY)'''
    # sum of all the costs with a levelization for some terms
    # LCOE is in euros per kWh
    return LCOE


def select_best_power(investment_cost1, investment_cost2, maintenance1, maintenance2,
                      efficiency11, efficiency12, efficiency21, efficiency22,
                      combustible_purchase_price1, combustible_purchase_price2,
                      combustible_sell_price1, combustible_sell_price2,
                      emission_factor11, emission_factor12, emission_factor21, emission_factor22,
                      P, P_nom):
    # for 2 given production subsytems, returns the cheapest LCOE
    # and the best nominal capacity for subsytem 1

    min_lcoe = 1000000
    best_p_limit = 0
    n = 100

    for k in range(n+1):
        P_double_system = P_nom*k/n
        # P_double_system goes is variable and goes from 0 to P_nom

        LCOE = compute_lcoe(investment_cost1, investment_cost2, maintenance1, maintenance2,
                            efficiency11, efficiency12, efficiency21, efficiency22,
                            combustible_purchase_price1, combustible_purchase_price2,
                            combustible_sell_price1, combustible_sell_price2,
                            emission_factor11, emission_factor12, emission_factor21, emission_factor22,
                            P, P_nom, P_double_system)

        if LCOE < min_lcoe:
            min_lcoe = LCOE
            best_p_limit = P_double_system*1000

    return (min_lcoe, best_p_limit)
