"""
costs.py

Handles fuel consumption and airport fees.
"""

from simulation.constants import *

def fuel_cost(airborne_minutes, international=True):
    """
    Computes fuel burned and fuel cost.
    """

    # Convert minutes to hours
    airborne_hours = airborne_minutes / 60

    # Fuel burned (gallons)
    gallons = airborne_hours * aircraft["A220-300"]["burn_gph"]

    # Fuel price depends on country
    if international:
        liters = gallons * gallon_to_liter
        cost = liters * fr_fuel_cost_per_liter
    else:
        cost = gallons * us_fuel_cost

    return gallons, cost


def airport_fees(international=True):
    """
    Computes takeoff and landing fees.
    """

    if international:
        return us_takeoff_fee + fr_landing_fee

    return us_takeoff_fee + us_landing_fee
