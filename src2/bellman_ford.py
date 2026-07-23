import math
def bellman_ford(graph, source):
    nodes = list(graph.nodes())
    edges = graph.edge_list()
    dist = {v: math.inf for v in nodes}
    prev = {v: None for v in nodes}
    dist[source] = 0

    rounds_used = 0
    for i in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        rounds_used += 1
        if not updated:  # converged early, no point doing more rounds
            break

    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, prev, has_negative_cycle, rounds_used
