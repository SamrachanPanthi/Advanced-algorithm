##Simulated annealing for VRPTW.
import math
import random


def _random_move(instance, routes, rng):
    routes = [r[:] for r in routes]
    non_empty = [i for i, r in enumerate(routes) if r]
    if not non_empty:
        return None

    if rng.choice(["relocate", "swap"]) == "relocate":
        r1 = rng.choice(non_empty)
        pos = rng.randrange(len(routes[r1]))
        cust = routes[r1].pop(pos)
        r2 = rng.randrange(len(routes))
        ins = rng.randrange(len(routes[r2]) + 1)
        routes[r2].insert(ins, cust)
    else:
        r1 = rng.choice(non_empty)
        r2 = rng.choice(non_empty)
        if not routes[r1] or not routes[r2]:
            return None
        p1 = rng.randrange(len(routes[r1]))
        p2 = rng.randrange(len(routes[r2]))
        routes[r1][p1], routes[r2][p2] = routes[r2][p2], routes[r1][p1]

    return [r for r in routes if r]


def simulated_annealing(instance, initial_routes, iterations=3000,
                         t0=50.0, cooling_rate=0.997, seed=0):
    rng = random.Random(seed)
    current = [r[:] for r in initial_routes]
    current_cost = instance.solution_distance(current)
    best = [r[:] for r in current]
    best_cost = current_cost

    t = t0
    history = [(0, current_cost, best_cost)]

    for it in range(1, iterations + 1):
        candidate = _random_move(instance, current, rng)
        if candidate is None or not instance.solution_is_feasible(candidate):
            t *= cooling_rate
            continue

        candidate_cost = instance.solution_distance(candidate)
        delta = candidate_cost - current_cost

        accept = delta < 0 or (t > 1e-9 and rng.random() < math.exp(-delta / t))
        if accept:
            current, current_cost = candidate, candidate_cost
            if current_cost < best_cost:
                best, best_cost = [r[:] for r in current], current_cost

        t *= cooling_rate
        if it % max(1, iterations // 100) == 0:
            history.append((it, current_cost, best_cost))

    history.append((iterations, current_cost, best_cost))
    return best, history
