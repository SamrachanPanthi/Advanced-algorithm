
import os
import time
import csv
import statistics

from vrptw import generate_instance
from heuristic_greedy import greedy_construction
from heuristic_local_search import local_search
from heuristic_simulated_annealing import simulated_annealing

OUT_CSV = "../results4/heuristic_benchmark.csv"
REPEATS = 3


def time_ms(fn):
    t0 = time.perf_counter()
    result = fn()
    return result, (time.perf_counter() - t0) * 1000


def run():
    rows = []
    sizes = [10, 20, 30, 40, 50]

    for n in sizes:
        print(f"=== n = {n} customers ===")
        g_dists, g_vehicles, g_times = [], [], []
        ls_dists, ls_vehicles, ls_times = [], [], []
        sa_dists, sa_vehicles, sa_times = [], [], []

        for rep in range(REPEATS):
            inst = generate_instance(n_customers=n, vehicle_capacity=100, seed=100 + rep)

            (routes_g, dropped), t_g = time_ms(lambda: greedy_construction(inst))
            assert not dropped, f"dropped customers: {dropped}"
            g_dists.append(inst.solution_distance(routes_g))
            g_vehicles.append(len(routes_g))
            g_times.append(t_g)

            (routes_ls, _), t_ls = time_ms(lambda: local_search(inst, routes_g))
            ls_dists.append(inst.solution_distance(routes_ls))
            ls_vehicles.append(len(routes_ls))
            ls_times.append(t_ls)

            (routes_sa, _), t_sa = time_ms(lambda: simulated_annealing(inst, routes_g, iterations=2000, seed=rep))
            sa_dists.append(inst.solution_distance(routes_sa))
            sa_vehicles.append(len(routes_sa))
            sa_times.append(t_sa)

        def m(lst):
            return statistics.mean(lst)

        rows.append(dict(algorithm="Greedy", n=n, distance_km=m(g_dists), vehicles=m(g_vehicles), time_ms=m(g_times)))
        rows.append(dict(algorithm="LocalSearch", n=n, distance_km=m(ls_dists), vehicles=m(ls_vehicles), time_ms=m(ls_times)))
        rows.append(dict(algorithm="SimulatedAnnealing", n=n, distance_km=m(sa_dists), vehicles=m(sa_vehicles), time_ms=m(sa_times)))

        print(f"  Greedy:              {m(g_dists):8.1f}km, {m(g_vehicles):.1f} vehicles, {m(g_times):7.2f}ms")
        print(f"  Local Search:        {m(ls_dists):8.1f}km, {m(ls_vehicles):.1f} vehicles, {m(ls_times):7.2f}ms")
        print(f"  Simulated Annealing: {m(sa_dists):8.1f}km, {m(sa_vehicles):.1f} vehicles, {m(sa_times):7.2f}ms")

    os.makedirs("../results4", exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["algorithm", "n", "distance_km", "vehicles", "time_ms"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nResults written to {OUT_CSV}")
    return rows


if __name__ == "__main__":
    run()
