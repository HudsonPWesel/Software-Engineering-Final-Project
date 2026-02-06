# Passenger Demand and Routing

This document describes how passenger demand is handled in the simulation.

## Demand Source
Passenger demand is read directly from `travelers.csv`.

Each row represents:
- origin airport
- destination airport
- daily passenger count

## Routing Rules
### Domestic Routes
- Passengers fly direct if a flight exists
- Otherwise, passengers are routed through one hub

### International Routes (Paris)
- All Paris traffic must route through a New York hub
- Valid hubs: JFK, EWR, LGA
- No direct spoke-to-Paris flights are allowed

## Capacity Constraints
Passengers boarded on a flight are limited by aircraft seat capacity.

Unboarded passengers:
- wait for the next available flight
- may be forced into overnight stays

## Connections
- Minimum connection time: 30 minutes
- Connections shorter than this result in missed connections
