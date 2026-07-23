"""City record used across all the tasks, plus a distance helper."""

from dataclasses import dataclass
import math


@dataclass
class City:
    id: int
    name: str
    country: str
    lat: float
    lng: float
    population: int
    distance: float = 0.0  # distance from a reference point, set by data_loader

    def __repr__(self):
        return f"City({self.name!r}, pop={self.population}, dist={self.distance:.1f}km)"

    def __lt__(self, other):
        return self.distance < other.distance


def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance in km between two lat/lng points."""
    R = 6371  # earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))
