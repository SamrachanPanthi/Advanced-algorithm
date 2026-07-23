"""Correctness tests for the VRPTW model and all three heuristics."""

from vrptw import generate_instance
from heuristic_greedy import greedy_construction
from heuristic_local_search import local_search
from heuristic_simulated_annealing import simulated_annealing


def test_greedy_feasible_and_complete():
    inst = generate_instance(n_customers=15, seed=1)
    routes, dropped = greedy_construction(inst)
    assert not dropped
    assert inst.solution_is_feasible(routes)
    served = sorted(c for r in routes for c in r)
    assert served == list(range(1, inst.n + 1))
    print(f"  Greedy: {len(routes)} routes, total distance={inst.solution_distance(routes):.1f}km -- OK")


def test_local_search_improves_or_matches():
    inst = generate_instance(n_customers=15, seed=1)
    routes0, _ = greedy_construction(inst)
    d0 = inst.solution_distance(routes0)
    routes1, _ = local_search(inst, routes0)
    d1 = inst.solution_distance(routes1)
    assert inst.solution_is_feasible(routes1)
    served = sorted(c for r in routes1 for c in r)
    assert served == list(range(1, inst.n + 1))
    assert d1 <= d0 + 1e-6
    print(f"  Local search: {d0:.1f}km -> {d1:.1f}km (improvement={d0-d1:.1f}km) -- OK")


def test_simulated_annealing_feasible_and_complete():
    inst = generate_instance(n_customers=15, seed=1)
    routes0, _ = greedy_construction(inst)
    routes_sa, _ = simulated_annealing(inst, routes0, iterations=500, seed=1)
    assert inst.solution_is_feasible(routes_sa)
    served = sorted(c for r in routes_sa for c in r)
    assert served == list(range(1, inst.n + 1))
    d_sa = inst.solution_distance(routes_sa)
    d0 = inst.solution_distance(routes0)
    print(f"  Simulated annealing: {d0:.1f}km -> {d_sa:.1f}km -- OK")


def test_larger_instance_all_heuristics():
    inst = generate_instance(n_customers=40, vehicle_capacity=100, seed=7)
    routes_g, dropped = greedy_construction(inst)
    assert not dropped
    assert inst.solution_is_feasible(routes_g)

    routes_ls, _ = local_search(inst, routes_g)
    assert inst.solution_is_feasible(routes_ls)

    routes_sa, _ = simulated_annealing(inst, routes_g, iterations=1000, seed=2)
    assert inst.solution_is_feasible(routes_sa)

    d_g = inst.solution_distance(routes_g)
    d_ls = inst.solution_distance(routes_ls)
    d_sa = inst.solution_distance(routes_sa)
    print(f"  n=40: greedy={d_g:.1f}km, local_search={d_ls:.1f}km, SA={d_sa:.1f}km -- OK")


if __name__ == "__main__":
    test_greedy_feasible_and_complete()
    test_local_search_improves_or_matches()
    test_simulated_annealing_feasible_and_complete()
    test_larger_instance_all_heuristics()
    print("\nAll Task 4 correctness checks passed.")
