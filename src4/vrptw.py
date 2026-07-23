import random
from city import haversine

AVERAGE_SPEED_KMH = 60.0


class Customer:
    __slots__ = ("id", "name", "lat", "lng", "demand", "ready", "due", "service_time")

    def __init__(self, id_, name, lat, lng, demand, ready, due, service_time):
        self.id = id_
        self.name = name
        self.lat = lat
        self.lng = lng
        self.demand = demand
        self.ready = ready
        self.due = due
        self.service_time = service_time

    def __repr__(self):
        return f"Customer({self.name}, demand={self.demand}, window=[{self.ready:.1f},{self.due:.1f}])"


class VRPTWInstance:
    def __init__(self, depot, customers, vehicle_capacity):
        self.depot = depot
        self.customers = customers
        self.n = len(customers)
        self.vehicle_capacity = vehicle_capacity
        self._build_matrices()

    def _build_matrices(self):
        """Distance (km) and travel-time (hours) matrix over depot + all
        customers. Index 0 is the depot, 1..n are the customers."""
        points = [self.depot] + self.customers
        m = len(points)
        self.dist = [[0.0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                if i != j:
                    self.dist[i][j] = haversine(points[i].lat, points[i].lng, points[j].lat, points[j].lng)
        self.time = [[d / AVERAGE_SPEED_KMH for d in row] for row in self.dist]
        self.points = points

    def route_distance(self, route):
        if not route:
            return 0.0
        total = self.dist[0][route[0]]
        for a, b in zip(route, route[1:]):
            total += self.dist[a][b]
        total += self.dist[route[-1]][0]
        return total

    def route_is_feasible(self, route):
        load = sum(self.points[c].demand for c in route)
        if load > self.vehicle_capacity:
            return False
        t = 0.0
        prev = 0
        for c in route:
            t += self.time[prev][c]
            cust = self.points[c]
            if t > cust.due:
                return False
            t = max(t, cust.ready)  # wait if we arrived early
            t += cust.service_time
            prev = c
        return True

    def solution_distance(self, routes):
        return sum(self.route_distance(r) for r in routes)

    def solution_is_feasible(self, routes):
        served = [c for r in routes for c in r]
        if sorted(served) != list(range(1, self.n + 1)):
            return False
        return all(self.route_is_feasible(r) for r in routes)


def generate_instance(n_customers=25, vehicle_capacity=100, seed=42, depot_name="Birmingham"):
    """Builds a VRPTW instance from real UK cities: one city as the depot,
    others as customers with randomised demand and time windows within an
    8-hour working day."""
    from data_loader import load_cities
    rng = random.Random(seed)

    cities = load_cities()
    uk = [c for c in cities if c.country == "United Kingdom"]
    uk_sorted = sorted(uk, key=lambda c: -c.population)[:80]

    depot_city = next((c for c in uk_sorted if c.name == depot_name), uk_sorted[0])
    others = [c for c in uk_sorted if c.id != depot_city.id]
    # only keep cities reachable from the depot within the working day -
    # otherwise no vehicle could ever serve them regardless of routing
    others = [c for c in others
              if haversine(depot_city.lat, depot_city.lng, c.lat, c.lng) / AVERAGE_SPEED_KMH < 7.0]
    sample = rng.sample(others, n_customers)

    depot = Customer(0, depot_city.name, depot_city.lat, depot_city.lng, 0, 0.0, 8.0, 0.0)

    customers = []
    for i, c in enumerate(sample, start=1):
        demand = rng.randint(5, 25)
        travel_from_depot = haversine(depot_city.lat, depot_city.lng, c.lat, c.lng) / AVERAGE_SPEED_KMH
        window_start = rng.uniform(0, 6)
        window_len = rng.uniform(1, 3)
        service = round(rng.uniform(0.1, 0.4), 2)
        # make sure the window is actually reachable from the depot
        ready = round(max(window_start, 0.0), 2)
        due = round(max(window_start + window_len, travel_from_depot + service + 0.25), 2)
        due = min(due, 8.0)
        ready = min(ready, max(0.0, due - window_len))
        customers.append(Customer(i, c.name, c.lat, c.lng, demand, ready, due, service))

    return VRPTWInstance(depot, customers, vehicle_capacity)
