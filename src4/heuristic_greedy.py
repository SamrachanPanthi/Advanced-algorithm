
def greedy_construction(instance):
    unserved = set(range(1, instance.n + 1))
    routes = []

    while unserved:
        route = []
        current = 0
        t = 0.0
        load = 0
        progress = True

        while progress:
            progress = False
            best_c, best_dist, best_start = None, None, None
            for c in unserved:
                cust = instance.points[c]
                if load + cust.demand > instance.vehicle_capacity:
                    continue
                arrival = t + instance.time[current][c]
                if arrival > cust.due:
                    continue
                start_service = max(arrival, cust.ready)
                d = instance.dist[current][c]
                if best_dist is None or d < best_dist:
                    best_c, best_dist, best_start = c, d, start_service

            if best_c is not None:
                route.append(best_c)
                load += instance.points[best_c].demand
                t = best_start + instance.points[best_c].service_time
                current = best_c
                unserved.discard(best_c)
                progress = True

        if route:
            routes.append(route)
        else:
            break  # nothing left can be placed on any route

    return routes, list(unserved)
