import os #Dijkstra, Prim, and Bellman-Ford on sparse (k-NN) and dense graphs
import time
import math
import csv
import statistics

from data_loader import load_cities
from network_builder import build_knn_graph, build_dense_graph
from dijkstra import dijkstra
from prim import prim
from bellman_ford import bellman_ford

REPEATS = 3
OUT_CSV = "../results2/graph_benchmark_results.csv"


def theoretical_ops(algo, v, e):
    if algo == "Dijkstra":
        return (v + e) * math.log2(max(v, 2))
    if algo == "Prim":
        return e * math.log2(max(v, 2))
    if algo == "BellmanFord":
        return v * e
    raise ValueError(algo)


def time_ms(fn):
    t0 = time.perf_counter()
    fn()
    return (time.perf_counter() - t0) * 1000


def bench_one(graph, source, label, v, e):
    rows = []

    dij_times = [time_ms(lambda: dijkstra(graph, source)) for _ in range(REPEATS)]
    dij_mean = statistics.mean(dij_times)
    rows.append(dict(algorithm="Dijkstra", graph_type=label, V=v, E=e,
                      time_ms=dij_mean,
                      theoretical_ops=theoretical_ops("Dijkstra", v, e),
                      observed_constant=dij_mean / theoretical_ops("Dijkstra", v, e)))

    und = graph.to_undirected()
    prim_times = [time_ms(lambda: prim(und, source)) for _ in range(REPEATS)]
    prim_mean = statistics.mean(prim_times)
    e_und = und.num_edges()
    rows.append(dict(algorithm="Prim", graph_type=label, V=v, E=e_und,
                      time_ms=prim_mean,
                      theoretical_ops=theoretical_ops("Prim", v, e_und),
                      observed_constant=prim_mean / theoretical_ops("Prim", v, e_und)))

    bf_times = [time_ms(lambda: bellman_ford(graph, source)) for _ in range(REPEATS)]
    bf_mean = statistics.mean(bf_times)
    rows.append(dict(algorithm="BellmanFord", graph_type=label, V=v, E=e,
                      time_ms=bf_mean,
                      theoretical_ops=theoretical_ops("BellmanFord", v, e),
                      observed_constant=bf_mean / theoretical_ops("BellmanFord", v, e)))

    return rows


def run():
    cities = load_cities()
    uk = [c for c in cities if c.country == "United Kingdom"]
    uk_sorted = sorted(uk, key=lambda c: -c.population)

    all_rows = []

    print("=== Sparse graphs (k-NN, k=6) ===")
    for n in [50, 100, 200, 400]:
        sample = uk_sorted[:n]
        g = build_knn_graph(sample, k=6)
        source = sample[0].id
        v, e = g.num_nodes(), g.num_edges()
        print(f"  n={n}: V={v} E={e} (density={g.density():.4f})")
        all_rows += bench_one(g, source, "sparse_knn6", v, e)

    print("=== Dense graphs (near-complete) ===")
    for n in [20, 40, 80, 120]:
        sample = uk_sorted[:n]
        g = build_dense_graph(sample, edge_fraction=0.9)
        source = sample[0].id
        v, e = g.num_nodes(), g.num_edges()
        print(f"  n={n}: V={v} E={e} (density={g.density():.4f})")
        all_rows += bench_one(g, source, "dense", v, e)

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["algorithm", "graph_type", "V", "E", "time_ms",
                                                 "theoretical_ops", "observed_constant"])
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\nResults written to {OUT_CSV}")
    return all_rows


if __name__ == "__main__":
    run()
