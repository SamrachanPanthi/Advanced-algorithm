"""
benchmark_task3.py
-------------------
Empirical wall-clock benchmark for the three Task 3 algorithms:

    - Matrix Chain Multiplication (Dynamic Programming)
    - Minimum Number of Platforms (Greedy)
    - Hamiltonian Cycle (Backtracking)

Each experiment is repeated several times and averaged.
Results are written immediately to CSV so that partial
results are not lost if execution is interrupted.
"""

import os
import time
import random
import csv
import statistics

from matrix_chain import matrix_chain_order
from platforms import min_platforms
from hamiltonian import Graph, hamiltonian_cycle


# Reduce repetitions to speed up execution
REPEATS = 3

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_CSV = os.path.join(
    THIS_DIR,
    "..",
    "results3",
    "task3_benchmark_results.csv"
)


def time_it(fn, *args, **kwargs):
    start = time.perf_counter()
    fn(*args, **kwargs)
    end = time.perf_counter()

    return (end - start) * 1000  # milliseconds


# ============================================================
# Matrix Chain Multiplication Benchmark
# ============================================================

def bench_matrix_chain(n_matrices):

    dimensions = [
        random.randint(5, 100)
        for _ in range(n_matrices + 1)
    ]

    times = []

    for _ in range(REPEATS):
        t = time_it(matrix_chain_order, dimensions)
        times.append(t)

    return statistics.mean(times)


# ============================================================
# Minimum Platforms Benchmark
# ============================================================

def bench_platforms(n_trains):

    arrivals = [
        random.randint(0, 2000)
        for _ in range(n_trains)
    ]

    departures = [
        arrival + random.randint(1, 200)
        for arrival in arrivals
    ]

    times = []

    for _ in range(REPEATS):
        t = time_it(min_platforms, arrivals, departures)
        times.append(t)

    return statistics.mean(times)


# ============================================================
# Hamiltonian Graph Generators
# ============================================================

def random_hamiltonian_graph(n_vertices, extra_edge_prob=0.5):

    graph = Graph(n_vertices)

    order = list(range(n_vertices))
    random.shuffle(order)

    # Create guaranteed cycle
    for i in range(n_vertices):
        graph.add_edge(
            order[i],
            order[(i + 1) % n_vertices]
        )

    # Add random edges
    for u in range(n_vertices):
        for v in range(u + 1, n_vertices):

            if graph.adj[u][v] == 0:

                if random.random() < extra_edge_prob:
                    graph.add_edge(u, v)

    return graph


def worst_case_graph(n_vertices):

    left_size = n_vertices // 2 - 1

    graph = Graph(n_vertices)

    for i in range(left_size):
        for j in range(left_size, n_vertices):
            graph.add_edge(i, j)

    return graph


# ============================================================
# Hamiltonian Benchmarks
# ============================================================

def bench_hamiltonian(n_vertices):

    times = []

    for _ in range(REPEATS):

        graph = random_hamiltonian_graph(n_vertices)

        t = time_it(
            hamiltonian_cycle,
            graph
        )

        times.append(t)

    return statistics.mean(times)


def bench_hamiltonian_worst_case(n_vertices):

    graph = worst_case_graph(n_vertices)

    return time_it(
        hamiltonian_cycle,
        graph
    )


# ============================================================
# Main Benchmark
# ============================================================

def main():

    random.seed(42)

    os.makedirs(
        os.path.dirname(OUTPUT_CSV),
        exist_ok=True
    )

    with open(
        OUTPUT_CSV,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["algorithm", "n", "time_ms"]
        )

        # ----------------------------------------------------
        # Matrix Chain Multiplication
        # ----------------------------------------------------

        print(
            "Benchmarking Matrix Chain Multiplication (DP)..."
        )

        for n in [10, 50, 100, 200, 300]:

            t = bench_matrix_chain(n)

            writer.writerow(
                ["MatrixChain", n, t]
            )

            file.flush()

            print(
                f"  n={n} matrices: {t:.4f} ms"
            )

        # ----------------------------------------------------
        # Minimum Platforms
        # ----------------------------------------------------

        print(
            "\nBenchmarking Minimum Number of Platforms (Greedy)..."
        )

        for n in [100, 1000, 10000, 100000]:

            t = bench_platforms(n)

            writer.writerow(
                ["MinPlatforms", n, t]
            )

            file.flush()

            print(
                f"  n={n} trains: {t:.4f} ms"
            )

        # ----------------------------------------------------
        # Hamiltonian Cycle (has cycle)
        # ----------------------------------------------------

        print(
            "\nBenchmarking Hamiltonian Cycle (graph contains cycle)..."
        )

        for n in [8, 10, 12, 14]:

            t = bench_hamiltonian(n)

            writer.writerow(
                ["HamiltonianCycle_HasCycle", n, t]
            )

            file.flush()

            print(
                f"  n={n} vertices: {t:.4f} ms"
            )

        # ----------------------------------------------------
        # Hamiltonian Worst Case
        # ----------------------------------------------------

        print(
            "\nBenchmarking Hamiltonian Cycle (worst case, no cycle)..."
        )

        for n in [8, 10, 12]:

            t = bench_hamiltonian_worst_case(n)

            writer.writerow(
                ["HamiltonianCycle_NoCycle", n, t]
            )

            file.flush()

            print(
                f"  n={n} vertices: {t:.4f} ms"
            )

    print("\nBenchmark completed successfully.")

    print(
        f"Results written to:\n{OUTPUT_CSV}"
    )


if __name__ == "__main__":
    main()