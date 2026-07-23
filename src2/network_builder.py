##Builds transportation-network graphs from the worldcities dataset.

import random
from city import haversine
from graph import DirectedGraph


def _perturbed(base_km, rng):
    return round(base_km * rng.uniform(0.9, 1.3), 3)


def build_knn_graph(cities, k=4, seed=7):
    """Sparse graph: each city connects to its k nearest neighbours."""
    rng = random.Random(seed)
    g = DirectedGraph()
    for c in cities:
        g.add_node(c.id, c)

    for c in cities:
        nearest = sorted(
            ((other, haversine(c.lat, c.lng, other.lat, other.lng)) for other in cities if other.id != c.id),
            key=lambda t: t[1]
        )[:k]
        for other, d in nearest:
            g.add_edge(c.id, other.id, _perturbed(d, rng))
    return g


def build_dense_graph(cities, edge_fraction=0.9, seed=7):
    """Dense graph: connect (almost) every pair of cities, for comparison."""
    rng = random.Random(seed)
    g = DirectedGraph()
    for c in cities:
        g.add_node(c.id, c)

    for c in cities:
        for other in cities:
            if other.id == c.id:
                continue
            if rng.random() <= edge_fraction:
                d = haversine(c.lat, c.lng, other.lat, other.lng)
                g.add_edge(c.id, other.id, _perturbed(d, rng))
    return g

def build_negative_weight_demo():
    g = DirectedGraph() #Small hand-built graphs to demonstrate Bellman-Ford's negative-weight
# and negative-cycle
    edges = [
        ("A", "B", 4), ("A", "C", 5),
        ("B", "C", -3), ("B", "D", 6),
        ("C", "D", 4), ("D", "E", 2),
        ("C", "E", 7), ("E", "B", -1),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g


def build_negative_cycle_demo():
    g = DirectedGraph()
    edges = [
        ("A", "B", 4), ("B", "C", -6),
        ("C", "D", 2), ("D", "B", 1),  # B->C->D->B = -6+2+1 = -3, a negative cycle
        ("A", "E", 3), ("E", "D", 1),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g
