import os
import time
import csv
import platform
import statistics

from network_builder import build_knn_graph
from data_loader import load_cities
from concurrent_bfs import sequential_bfs, ConcurrentBFS

OUT_CSV = "../results5/concurrency_benchmark.csv"
REPEATS = 5
WORKLOAD_SIZE = 5000
THREAD_COUNTS = [1, 2, 4, 8]


def build_graph(n=150, k=10):
    cities = load_cities()
    uk = [c for c in cities if c.country == "United Kingdom"]
    uk_sorted = sorted(uk, key=lambda c: -c.population)[:n]
    return build_knn_graph(uk_sorted, k=k), uk_sorted[0].id


def run():
    cpu_count = os.cpu_count()
    print(f"Detected CPU count (os.cpu_count()): {cpu_count}")
    print(f"Platform: {platform.platform()}")

    graph, source = build_graph()
    print(f"Graph: V={graph.num_nodes()}, E={graph.num_edges()}")

    seq_times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        sequential_bfs(graph, source, workload_size=WORKLOAD_SIZE)
        seq_times.append((time.perf_counter() - t0) * 1000)
    t_seq = statistics.mean(seq_times)
    print(f"Sequential baseline: {t_seq:.2f}ms (mean of {REPEATS} runs)")

    rows = []
    rows.append(dict(threads=0, label="sequential_reference", time_ms=t_seq, speedup=1.0))

    for threads in THREAD_COUNTS:
        times = []
        for _ in range(REPEATS):
            cbfs = ConcurrentBFS(graph, num_threads=threads, workload_size=WORKLOAD_SIZE)
            t0 = time.perf_counter()
            cbfs.run(source)
            times.append((time.perf_counter() - t0) * 1000)
        t_mean = statistics.mean(times)
        speedup = t_seq / t_mean
        efficiency = speedup / threads
        rows.append(dict(threads=threads, label=f"{threads}_threads", time_ms=t_mean,
                          speedup=speedup, efficiency=efficiency))
        print(f"  threads={threads}: {t_mean:7.2f}ms, speedup={speedup:.3f}x, efficiency={efficiency:.3f}")

    # Amdahl's Law theoretical projection, using the empirically estimated
    # parallelisable fraction (see docstring)
    t0 = time.perf_counter(); sequential_bfs(graph, source, workload_size=1); t_overhead = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); sequential_bfs(graph, source, workload_size=WORKLOAD_SIZE); t_full = (time.perf_counter() - t0) * 1000
    parallel_fraction = max(0.0, (t_full - t_overhead) / t_full)
    print(f"\nEstimated parallelisable fraction p = {parallel_fraction:.3f}")

    amdahl_rows = []
    for n in [1, 2, 4, 8, 16, 32]:
        amdahl_speedup = 1.0 / ((1 - parallel_fraction) + parallel_fraction / n)
        amdahl_rows.append(dict(threads=n, amdahl_speedup=amdahl_speedup))
        print(f"  Amdahl prediction @ {n} cores: {amdahl_speedup:.3f}x")

    os.makedirs("../results5", exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["threads", "label", "time_ms", "speedup", "efficiency"])
        writer.writeheader()
        writer.writerows(rows)

    with open("../results5/amdahl_projection.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["threads", "amdahl_speedup"])
        writer.writeheader()
        writer.writerows(amdahl_rows)

    with open("../results5/environment_info.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cpu_count", "platform", "parallel_fraction_estimated"])
        writer.writerow([cpu_count, platform.platform(), round(parallel_fraction, 4)])

    print(f"\nResults written to {OUT_CSV}")
    return rows, amdahl_rows, cpu_count, parallel_fraction


if __name__ == "__main__":
    run()
