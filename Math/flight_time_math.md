# Flight Time Calculations

This document describes how gate-to-gate flight times are calculated.

## Components of Flight Time
Gate-to-gate time consists of:
- Taxi out
- Takeoff runway time
- Airborne time (climb + cruise + descent)
- Landing runway time
- Taxi in

## Taxi Time
### Hub Airports
For hubs with metro population greater than 9 million:
taxi = min(20, 15 + ceil((population − 9M) / 2M))

### Non-Hub Airports
taxi = min(13, population × 0.0000075)

Total taxi time is the sum of taxi out and taxi in.

## Runway Time
- Takeoff runway time: 1 minute
- Landing runway time: 2 minutes

Total runway time per flight: 3 minutes.

## Cruise Altitude Selection
- International flights: 38,000 ft
- Domestic flights ≥ 1,500 miles: 35,000 ft
- Domestic flights < 1,500 miles: 30,000 ft
- Flights < 350 miles: 25,000 ft
- Flights < 200 miles: 20,000 ft

## Climb Calculations
- Climb angle: 6°
- tan(6°) = 0.105104
- 1 NM = 6,076 ft

### 0 → 10,000 ft
Horizontal distance:
10,000 / tan(6°) = 95,066 ft = 15.64 NM

Acceleration:
150 → 250 kt at 25 kt/min = 4.0 min

Remaining climb time at 250 kt:
0.55 min

Total time:
5.88 min

### 10,000 ft → Cruise Altitude (38,000 ft example)
Vertical change: 28,000 ft  
Horizontal distance: 43.8 NM  

Acceleration:
250 → 280 kt = 1.2 min

Remaining climb at 280 kt:
8.25 min

Total time:
9.45 min

### Total Climb
- Distance: 59.44 NM
- Time: 15.33 min

## Descent Calculations
Rule:
1,000 ft = 3 NM

From 38,000 ft:
- Distance: 114 NM

Deceleration:
250 → 200 kt = 1.43 min

Remaining descent at 200 kt:
32.6 min

Total descent time:
34.0 min

## Cruise Time
Cruise distance is calculated as:
total distance − climb distance − descent distance

Cruise speed:
0.8 × max aircraft speed

Cruise time = cruise distance / cruise speed

## East–West Adjustment
- Eastbound flights: −4.5% time
- Westbound flights: +4.5% time

This adjustment is applied to total airborne time.

## Final Gate-to-Gate Time
gate-to-gate =
taxi + runway + airborne (adjusted)
