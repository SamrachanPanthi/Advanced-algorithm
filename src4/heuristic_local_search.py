def _two_opt_pass(instance, routes):
    improved_any = False
    for r_idx, route in enumerate(routes):
        n = len(route)
        for i in range(n - 1):
            for j in range(i + 1, n):
                candidate = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                if candidate == route:
                    continue
                if instance.route_distance(candidate) < instance.route_distance(route) - 1e-9 \
                        and instance.route_is_feasible(candidate):
                    routes[r_idx] = candidate
                    route = candidate
                    improved_any = True
    return improved_any


def _or_opt_pass(instance, routes):
    improved_any = False
    r_count = len(routes)
    for r1 in range(r_count):
        pos = 0
        while pos < len(routes[r1]):
            cust = routes[r1][pos]
            without = routes[r1][:pos] + routes[r1][pos + 1:]
            removal_saving = instance.route_distance(routes[r1]) - instance.route_distance(without)

            best_gain, best_target = 1e-9, None
            for r2 in range(r_count):
                base = without if r2 == r1 else routes[r2]
                for ins in range(len(base) + 1):
                    candidate = base[:ins] + [cust] + base[ins:]
                    insertion_cost = instance.route_distance(candidate) - instance.route_distance(base)
                    gain = removal_saving - insertion_cost
                    if gain > best_gain and instance.route_is_feasible(candidate):
                        if r2 == r1 or instance.route_is_feasible(without):
                            best_gain, best_target = gain, (r2, ins, candidate)

            if best_target is not None:
                r2, ins, candidate = best_target
                if r2 == r1:
                    routes[r1] = candidate
                else:
                    routes[r1] = without
                    routes[r2] = candidate
                improved_any = True
                pos = 0  # indices shifted, restart this route's scan
                continue
            pos += 1

    routes[:] = [r for r in routes if r]
    return improved_any


def local_search(instance, initial_routes, max_passes=50):
    routes = [r[:] for r in initial_routes]
    history = [instance.solution_distance(routes)]

    for _ in range(max_passes):
        improved = _two_opt_pass(instance, routes)
        improved = _or_opt_pass(instance, routes) or improved
        history.append(instance.solution_distance(routes))
        if not improved:
            break

    routes = [r for r in routes if r]
    return routes, history
