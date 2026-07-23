"""Loads worldcities.csv and turns rows into City objects."""

import csv
import random
from city import City, haversine

DEFAULT_CSV_PATH = "../data/worldcities.csv"
REFERENCE_POINT = (51.5074, -0.1278)  # London, used as the "current location"


def load_cities(path=DEFAULT_CSV_PATH, reference=REFERENCE_POINT, limit=None):
    cities = []
    ref_lat, ref_lng = reference

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row["lat"])
                lng = float(row["lng"])
                pop = row["population"]
                population = int(float(pop)) if pop not in (None, "", "NaN") else 0
                cid = int(row["id"])
                name = row["city_ascii"] or row["city"]
                country = row["country"]
            except (ValueError, KeyError):
                continue  # skip bad rows

            dist = haversine(ref_lat, ref_lng, lat, lng)
            cities.append(City(cid, name, country, lat, lng, population, dist))
            if limit and len(cities) >= limit:
                break

    return cities


def sample_cities(all_cities, n, seed=42):
    rnd = random.Random(seed)
    return rnd.sample(all_cities, n)


if __name__ == "__main__":
    cities = load_cities()
    print(f"Loaded {len(cities)} cities")
    for c in cities[:5]:
        print(" ", c)
