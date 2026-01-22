import json
import csv
import os
from typing import Union, Optional, Callable, Any
import requests
from datetime import datetime
import zoneinfo
from collections import defaultdict
from geopy.distance import great_circle  # type: ignore

# import requests
API_TOKEN = "7c9a792f46b1b7c63b174cc811c45a6ec439e49d3ab497be5c174636b9382bc50346678f6ef0810492fa9f28ce62068c"

PERCENT_OF_FLYERS: float = 0.005
MARKET_SHARE: float = 0.5
MIN_MILES: float = 150.0
HUBS: set[str] = set()

HUBS.add("KATL")
HUBS.add("KDFW")
HUBS.add("KDEN")

ICAO_TO_TIMEZONE = {
    "KATL": "America/New_York",
    "KDFW": "America/Chicago",
    "KDEN": "America/Denver",
    "KORD": "America/Chicago",
    "KLAX": "America/Los_Angeles",
    "KJFK": "America/New_York",
    "KCLT": "America/New_York",
    "KLAS": "America/Los_Angeles",  # Follows Pacific Time of las_vegas
    "KMCO": "America/New_York",
    "KMIA": "America/New_York",
    "KPHX": "America/Phoenix",  # no DST
    "KSEA": "America/Los_Angeles",
    "KSFO": "America/Los_Angeles",
    "KEWR": "America/New_York",
    "KIAH": "America/Chicago",
    "KBOS": "America/New_York",
    "KMSP": "America/Chicago",
    "KFLL": "America/New_York",
    "KLGA": "America/New_York",
    "KDTW": "America/New_York",
    "KPHL": "America/New_York",
    "KSLC": "America/Denver",
    "KBWI": "America/New_York",
    "KIAD": "America/New_York",
    "KSAN": "America/Los_Angeles",
    "KDCA": "America/New_York",
    "KTPA": "America/New_York",
    "KBNA": "America/Chicago",
    "KAUS": "America/Chicago",
    "PHNL": "Pacific/Honolulu",  # Hawaii
    "LFPG": "Europe/Paris",  # Charles de Gaulle
}
ICAO_TO_METRO_POPULATION: dict[str, float] = {
    "KATL": 6_300_000,  # Atlanta
    "KDFW": 7_900_000,  # Dallas–Fort Worth
    "KDEN": 3_000_000,  # Denver
    "KORD": 9_500_000,  # Chicago
    "KLAX": 13_200_000,  # Los Angeles
    "KJFK": 20_200_000,  # New York City
    "KCLT": 2_800_000,  # Charlotte
    "KLAS": 2_300_000,  # Las Vegas
    "KMCO": 2_700_000,  # Orlando
    "KMIA": 6_200_000,  # Miami–Fort Lauderdale
    "KPHX": 5_100_000,  # Phoenix
    "KSEA": 4_100_000,  # Seattle
    "KSFO": 7_800_000,  # San Francisco Bay Area
    "KEWR": 20_200_000,  # NYC metro
    "KIAH": 7_300_000,  # Houston
    "KBOS": 5_000_000,  # Boston
    "KMSP": 3_700_000,  # Minneapolis–St. Paul
    "KFLL": 6_200_000,  # Miami–Fort Lauderdale
    "KLGA": 20_200_000,  # NYC metro
    "KDTW": 4_300_000,  # Detroit
    "KPHL": 6_200_000,  # Philadelphia
    "KSLC": 1_300_000,  # Salt Lake City
    "KBWI": 6_200_000,  # Baltimore–Washington
    "KIAD": 6_200_000,  # Washington DC metro
    "KSAN": 3_300_000,  # San Diego
    "KDCA": 6_200_000,  # Washington DC metro
    "KTPA": 3_200_000,  # Tampa Bay
    "KBNA": 2_000_000,  # Nashville
    "KAUS": 2_400_000,  # Austin
    "PHNL": 1_000_000,  # Honolulu
    "LFPG": 13_000_000,  # Paris metro
}


def main() -> None:
    airports = load_data("airports.json", fetch_and_mark_airports)

    # FIXME: Passing data to every calc

    distances = load_data("distances.json", lambda: calculate_distances(airports))

    calc_number_of_flyers(distances)

    for key in ICAO_TO_TIMEZONE.values():
        get_time_of_city(key)

    get_best_hub_locations()  # USE load_data instead
    taxi_times: dict[str, float] = load_data(
        "taxi-times.json", lambda: calc_time_to_taxi()
    )


def get_best_hub_locations():
    counts = defaultdict(int)
    with open("travelers.csv", "r") as f:
        counts = defaultdict(int)
        reader = csv.DictReader(f)
        for row in reader:
            for col_name, value in row.items():
                try:
                    counts[col_name] += int(value)
                except:
                    continue

        with open("hubs.json", "w") as f:
            json.dump(
                {
                    city_name: value
                    for city_name, value in sorted(
                        counts.items(), key=lambda x: x[-1], reverse=True
                    )
                },
                f,
            )


def load_data(
    filename: str,
    build_func: Callable[[], dict],
    post_processs_func: Optional[Callable[[], Any]] = None,
) -> dict:
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            return json.load(f)
    data: dict = build_func()
    with open(filename, "w") as f:
        json.dump(data, f)
    return data


def calculate_distances(airports: dict) -> dict:
    airport_coords: list[tuple] = []
    distances_csv: dict = {}
    distances_json: dict[str, dict[str, float]] = defaultdict(dict)

    for airport, airport_data in airports.items():
        icao, latitude, longitude = (
            airport,
            airport_data.get("latitude_deg"),
            airport_data.get("longitude_deg"),
        )

        if not latitude or not longitude:
            raise ValueError(f"[-] Unable fetch GPS data for {airport}")

        airport_coords.append((icao, latitude, longitude))

    with open(
        "distances.csv",
        "w",
    ) as f:
        # TODO: This should be exported but I'm too lazy
        writer = csv.writer(f)
        writer.writerow([""] + list(ICAO_TO_TIMEZONE.keys()))

        for source_airport, *source_airport_coords in airport_coords:
            row: list[Union[float, str]] = []
            for dest_airport, *dest_airport_coords in airport_coords:
                if source_airport == dest_airport:
                    row.append(0.00)
                    continue

                miles: float = great_circle(
                    source_airport_coords, dest_airport_coords
                ).miles

                row.append(round(miles, 5) if miles >= MIN_MILES else -1.000)

                distances_json[source_airport][dest_airport] = (
                    round(miles, 5) if miles >= MIN_MILES else -1.000
                )

            distances_csv[source_airport] = row
            writer.writerow([source_airport] + row)
    return distances_json


"""
Format of timezone expected : "America/New_York" | "Europe/Paris"
"""


"""
DOES NOT ACCOUNT FOR FULL GATES 
"""


def is_hub(icao: str) -> bool:
    return False


def calc_time_to_taxi() -> dict:
    taxi_times: dict[str, float] = {}
    for current_icao, current_population in ICAO_TO_METRO_POPULATION.items():
        taxi_times[current_icao] = (
            min(13, (current_population * 0.0000075))
            if not is_hub(current_icao)
            else min(
                20,
                15
                if current_population <= 9_000_000
                else ((current_population - 15) // 2) + 15,
            )
        )
    return taxi_times


def get_time_of_city(iana_time_zone: str) -> datetime:
    local_timezone = zoneinfo.ZoneInfo(iana_time_zone)
    local_time = datetime.now(local_timezone)
    print(f"Time in ({iana_time_zone.split('/')[-1]}) : ", end="")
    print(
        local_time.strftime("%Y-%m-%d %H:%M:%S ")
    )  # Could add %Z timezone zone (e.g UTC,EST), %z outputs the UTC Offset
    return local_time


def calculate_total_reachable_airport_populations(
    source_airport_name: str,
    distances: dict[str, dict[str, float]],
) -> float:
    # TODO: FILTER for reachable using distances and time
    populations_counter: float = 0.0
    for dest_airport_name, dest_airport_distance in distances.items():
        if distances[source_airport_name].get(
            dest_airport_name, 0
        ):  # if lower than 150 then -1, and don't include source_airport_name
            populations_counter += ICAO_TO_METRO_POPULATION[dest_airport_name]
    print(f"[+] Total Population from {source_airport_name} : {populations_counter}")

    return populations_counter


# TODO: Make return in JSON format like with distances but our get_best_hubs reads the csv file instead
def calc_number_of_flyers(
    airport_distances: dict[str, dict[str, float]],
):
    with open(
        "travelers.csv",
        "w",
    ) as f:
        writer = csv.writer(f)
        writer.writerow([""] + list(ICAO_TO_METRO_POPULATION.keys()))

        for (
            source_city_name,
            source_city_population,
        ) in ICAO_TO_METRO_POPULATION.items():
            total_reachable_population = calculate_total_reachable_airport_populations(
                source_city_name,
                airport_distances,
            )
            daily_flyers = source_city_population * PERCENT_OF_FLYERS
            panther_flyers = daily_flyers * MARKET_SHARE
            row: list[int] = []
            for (
                distination_city_name,
                destination_city_population,
            ) in ICAO_TO_METRO_POPULATION.items():
                if source_city_name != distination_city_name:
                    dest_share = (
                        destination_city_population / total_reachable_population
                    )
                    row.append(round(panther_flyers * dest_share))
                else:
                    row.append(0)
            writer.writerow([source_city_name] + row)


"""
Fetches airport data from random api that uses wikipedia and adds attributes "is_hub" to that data and returns that data as dict to write to airports.json
"""


def fetch_and_mark_airports() -> dict:
    fetched_airports_data = fetch_airports()
    return mark_airports_as_hubs(fetched_airports_data)


def mark_airports_as_hubs(fetched_airports_data: dict) -> dict:
    for icao in fetched_airports_data:
        if icao in HUBS:
            fetched_airports_data[icao]["is_hub"] = True
            print(f"[+] Marked {icao} as hub")
    return fetched_airports_data


def fetch_airports() -> dict:
    airline_data = {}
    for icao in ICAO_TO_TIMEZONE.keys():
        url = f"https://airportdb.io/api/v1/airport/{icao}?apiToken={API_TOKEN}"
        print(f"[+] Fetching {icao} ({url})")
        request = requests.get(url, timeout=30)
        airline_data[icao] = request.json()

    return airline_data


# print(calc_number_of_flyers(1_000_000, 10_000_000, 175_000_000))

if __name__ == "__main__":
    main()
