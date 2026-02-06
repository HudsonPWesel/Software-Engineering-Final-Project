"""
passengers.py

Loads passenger demand from travelers.csv.
"""

import csv

def load_passengers(filepath):
    """
    Reads daily passenger demand for each route.
    """

    demand = {}

    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Keyed by (origin, destination)
            key = (row["origin"], row["destination"])

            # Daily passenger count
            demand[key] = int(row["daily_passengers"])

    return demand
