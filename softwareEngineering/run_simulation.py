"""
run_simulation.py

Entry point for the simulation.
Currently runs a single test route to validate math.
"""

import json
from simulation.flight_time import gate_to_gate_time
from simulation.costs import fuel_cost, airport_fees
from simulation.passengers import load_passengers
from simulation.constants import aircraft

# Load Data Files

# Load distance data
with open("distances.json") as f:
    distances = json.load(f)

# Load passenger demand
passengers = load_passengers("travelers.csv")

# Test route 


origin = "KJFK"
destination = "LFPG"

# Lookup distance
distance_nm = distances[origin][destination]

# Time Calculation


# Compute gate-to-gate flight time
gate_time_min = gate_to_gate_time(distance_nm, eastbound=True)

# Cost Calculation

# Fuel usage and cost
fuel_gallons, fuel_cost_usd = fuel_cost(gate_time_min, international=True)

# Airport fees
fees = airport_fees(international=True)

# Total operating cost
total_cost = fuel_cost_usd + fees

# REVENUE CALCULATION

# Aircraft seating
seats = AIRCRAFT["A220-300"]["seats"]

# Pricing assumption (30% load factor)
fare = total_cost / (0.30 * seats)

# Actual boarded passengers (75%)
actual_passengers = int(seats * 0.75)

# Revenue
revenue = fare * actual_passengers

# Profit
profit = revenue - total_cost

# Output Results

print("Route:", origin, "→", destination)
print("Gate-to-gate time (min):", round(gate_time_min, 1))
print("Fuel used (gallons):", round(fuel_gallons))
print("Total cost ($):", round(total_cost))
print("Revenue ($):", round(revenue))
print("Profit ($):", round(profit))
