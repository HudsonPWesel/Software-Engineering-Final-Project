"""
flight_time.py
This file handles all flight time calculations.

"""

from simulation.constants import *

def climb_profile(cruise_alt_ft):
    """
    Computes total climb distance and time.
    The climb is split into:
    - 0 → 10,000 ft
    - 10,000 ft -> cruise altitude
    """

    # 0 to 10,000 ft climb

    # Horizontal distance from climb geometry
    dist1_nm = (10000 / tan_climb) / ft_per_nm

    # Time computed manually in math docs
    time1_min = 5.88

    # 10,000 -> cruise alt

    remaining_ft = cruise_alt_ft - 10000
    dist2_nm = (remaining_ft / tan_climb) / ft_per_nm

    # Time depends on cruise altitude
    # 38,000 ft corresponds to international flights
    if cruise_alt_ft == 38000:
        time2_min = 9.45
    else:
        # Simplified assumption for lower cruise altitudes
        time2_min = 8.5

    # Return total climb distance and time
    return dist1_nm + dist2_nm, time1_min + time2_min


def descent_profile(cruise_alt_ft):
    """
    Computes descent distance and time.
    Uses rule: 1,000 ft = 3 NM
    """

    # Distance based on altitude
    dist_nm = (cruise_alt_ft / 1000) * 3

    # Descent time from math docs
    if cruise_alt_ft == 38000:
        time_min = 34.0
    else:
        time_min = 30.0

    return dist_nm, time_min


def cruise_altitude(distance_miles, international):
    """
    Selects cruise altitude based on distance and route type.
    """

    if international:
        return 38000
    if distance_miles >= 1500:
        return 35000
    if distance_miles >= 350:
        return 30000
    if distance_miles >= 200:
        return 25000
    return 20000


def gate_to_gate_time(distance_nm, eastbound=True):
    """
    Computes total gate-to-gate flight time in minutes.
    """

    # Convert distance to miles for altitude rules
    distance_miles = distance_nm * nm_to_miles

    # Select cruise altitude
    cruise_alt = cruise_altitude(distance_miles, international=True)

    # Get climb and descent components
    climb_dist, climb_time = climb_profile(cruise_alt)
    descent_dist, descent_time = descent_profile(cruise_alt)

    # Cruise distance is what's left
    cruise_dist = distance_nm - climb_dist - descent_dist

    # Cruise speed is 80% of max
    cruise_speed = 0.8 * AIRCRAFT["A220-300"]["max_speed"]

    # Convert cruise time from hours to minutes
    cruise_time = (cruise_dist / cruise_speed) * 60

    # Total airborne time
    airborne_time = climb_time + cruise_time + descent_time

    # Apply east/west Earth rotation adjustment
    if eastbound:
        airborne_time *= eastbound_factor
    else:
        airborne_time *= westbound_factor

    # Add runway time (taxi handled elsewhere)
    total_time = airborne_time + takeoff_runway_min + landing_runway_min

    return total_time
