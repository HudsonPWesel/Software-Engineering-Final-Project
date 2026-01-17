import json
import csv

# import requests
from geopy.distance import great_circle

# API_TOKEN = "7c9a792f46b1b7c63b174cc811c45a6ec439e49d3ab497be5c174636b9382bc50346678f6ef0810492fa9f28ce62068c"

icao_codes = [
    "KATL",
    "KDFW",
    "KDEN",
    "KORD",
    "KLAX",
    "KJFK",
    "KCLT",
    "KLAS",
    "KMCO",
    "KMIA",
    "KPHX",
    "KSEA",
    "KSFO",
    "KEWR",
    "KIAH",
    "KBOS",
    "KMSP",
    "KFLL",
    "KLGA",
    "KDTW",
    "KPHL",
    "KSLC",
    "KBWI",
    "KIAD",
    "KSAN",
    "KDCA",
    "KTPA",
    "KBNA",
    "KAUS",
    "PHNL",
]


# def fetch_airports(codes: list[str]) -> dict:
#     data = {}
#     for icao in codes:
#         url = f"https://airportdb.io/api/v1/airport/{icao}?apiToken={API_TOKEN}"
#         request = requests.get(url, timeout=30)
#         data[icao] = request.json()
#      airports = fetch_airports(icao_codes)

#      with open("airports.json", "w") as f:
#      f.write(json.dumps(airports))

#     return data


def main():

    with open("airports.json", "r") as f:
        airports = json.load(f)
    calculate_distances(airports)


def calculate_distances(airports: dict) -> None:
    distances: dict = {}
    airport_coords: list[tuple] = []

    for airport, airport_data in airports.items():
        if not latitude or not longitude:
            print(
                f"[-] Unable fetch GPS data for {airport}"
            )  # May want to throw an err here but since we're jsut processing data idc
        icao, latitude, longitude = (
            airport,
            airport_data.get("latitude_deg"),
            airport_data.get("longitude_deg"),
        )

        airport_coords.append((icao, latitude, longitude))

    print(airport_coords)

    with open(
        "distances.csv",
        "w",
    ) as f:
        writer = csv.writer(f)
        writer.writerow([""] + icao_codes)
        for source_airport, *source_airport_coords in airport_coords:
            distances[source_airport] = [
                (
                    round(
                        great_circle(source_airport_coords, dest_airport_coords).miles,
                        5,
                    )
                    if source_airport != dest_airport
                    else 0.00
                )
                for dest_airport, *dest_airport_coords in airport_coords
            ]

            writer.writerow([source_airport] + distances[source_airport])


# Filter by reachable airports (more than 150 miles apart & operates when landing)


def is_reachable_airport():
    obj = TimezoneFinder()
    tf = TimezoneFinder(in_memory=True)
    query_points = [(13.358, 52.5061)]
    for lng, lat in query_points:
        tz = tf.timezone_at(lng=lng, lat=lat)
        print(tz)


def calc_number_of_flyers(
    source_metro_pop: float,
    dest_metro_pop: float,
    total_reachable_pop_excluding_source: float,
):
    daily_flyers = source_metro_pop * PERCENT_OF_FLYERS
    panther_flyers = daily_flyers * MARKET_SHARE

    dest_share = dest_metro_pop / total_reachable_pop_excluding_source
    return panther_flyers * dest_share


main()
# print(calc_number_of_flyers(1_000_000, 10_000_000, 175_000_000))

if __name__ == "__main__":
    main()
