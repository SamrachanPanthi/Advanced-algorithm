"""Correctness tests for Dijkstra, Prim, and Bellman-Ford."""

import math
from graph import DirectedGraph
from dijkstra import dijkstra, reconstruct_path
from prim import prim
from bellman_ford import bellman_ford
from network_builder import build_negative_weight_demo, build_negative_cycle_demo


def test_dijkstra_simple():
    g = DirectedGraph()
    edges = [("A", "B", 4), ("A", "C", 1), ("C", "B", 1), ("B", "D", 1), ("C", "D", 5)]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    dist, prev, order = dijkstra(g, "A")
    assert dist["B"] == 2  # A->C->B = 1+1
    assert dist["D"] == 3  # A->C->B->D = 1+1+1
    assert reconstruct_path(prev, "D") == ["A", "C", "B", "D"]
    print("  Dijkstra simple graph: OK", dist)


def test_dijkstra_matches_bellman_ford_on_nonnegative_graph():
    g = DirectedGraph()
    edges = [("A", "B", 4), ("A", "C", 1), ("C", "B", 1), ("B", "D", 1),
             ("C", "D", 5), ("D", "E", 2), ("B", "E", 8)]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    d1, _, _ = dijkstra(g, "A")
    d2, _, neg_cycle, _ = bellman_ford(g, "A")
    assert not neg_cycle
    for node in d1:
        assert abs(d1[node] - d2[node]) < 1e-9
    print("  Dijkstra and Bellman-Ford agree on a non-negative graph: OK")


def test_bellman_ford_negative_weights():
    g = build_negative_weight_demo()
    dist, prev, neg_cycle, rounds = bellman_ford(g, "A")
    assert not neg_cycle
    assert dist["D"] < math.inf
    print(f"  Bellman-Ford negative-weight demo: {dist}, converged in {rounds} rounds -- OK")


def test_bellman_ford_negative_cycle_detection():
    g = build_negative_cycle_demo()
    dist, prev, neg_cycle, rounds = bellman_ford(g, "A")
    assert neg_cycle is True
    print("  Bellman-Ford correctly detected the negative cycle: OK")


def test_prim_mst():
    g = DirectedGraph()
    edges = [("A", "B", 1), ("B", "A", 1), ("B", "C", 2), ("C", "B", 2),
             ("A", "C", 4), ("C", "A", 4), ("C", "D", 1), ("D", "C", 1)]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    und = g.to_undirected()
    mst_edges, total_weight, connected = prim(und, "A")
    assert connected
    assert len(mst_edges) == 3
    assert total_weight == 4
    print(f"  Prim MST: edges={mst_edges}, total_weight={total_weight} -- OK")


if __name__ == "__main__":
    test_dijkstra_simple()
    test_dijkstra_matches_bellman_ford_on_nonnegative_graph()
    test_bellman_ford_negative_weights()
    test_bellman_ford_negative_cycle_detection()
    test_prim_mst()
    print("\nAll graph algorithm correctness checks passed.")
