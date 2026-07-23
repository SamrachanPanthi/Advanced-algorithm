import os
import csv
import matplotlib
import matplotlib.pyplot as plt

RESULTS_DIR = "../results5"
PLOTS_DIR = "../results5/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def _save_and_show(fname):
    plt.savefig(f"{PLOTS_DIR}/{fname}", dpi=150)
    try:
        plt.show()
    except Exception:
        pass
    plt.close()


def load_csv(name):
    rows = []
    with open(f"{RESULTS_DIR}/{name}") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def plot_speedup_vs_threads():
    rows = load_csv("concurrency_benchmark.csv")
    amdahl = load_csv("amdahl_projection.csv")
    measured = [(int(r["threads"]), float(r["speedup"])) for r in rows if int(r["threads"]) > 0]
    amdahl_pts = [(int(r["threads"]), float(r["amdahl_speedup"])) for r in amdahl if int(r["threads"]) <= 8]

    plt.figure(figsize=(8.5, 6))
    xs_m = [p[0] for p in measured]
    ys_m = [p[1] for p in measured]
    plt.plot(xs_m, ys_m, marker="o", color="#e15759", linewidth=2, markersize=8,
              label="Measured speedup (this machine, 1 physical core)")

    xs_a = [p[0] for p in amdahl_pts]
    ys_a = [p[1] for p in amdahl_pts]
    plt.plot(xs_a, ys_a, marker="s", color="#4e79a7", linestyle="--",
              label="Amdahl's Law projection (theoretical, genuine multi-core hardware)")

    ideal_x = [1, 2, 4, 8]
    plt.plot(ideal_x, ideal_x, color="gray", linestyle=":", label="Ideal linear speedup (unattainable reference)")
    plt.axhline(1.0, color="black", linewidth=0.8, alpha=0.5)

    plt.xlabel("Number of threads")
    plt.ylabel("Speedup vs sequential baseline")
    plt.title("Speedup vs Thread Count: Measured (this sandbox) vs Theoretical (multi-core)")
    plt.legend()
    plt.grid(True, ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("speedup_vs_threads.png")
    print("saved speedup_vs_threads.png")


def plot_time_vs_threads():
    rows = load_csv("concurrency_benchmark.csv")
    pts = [(int(r["threads"]), float(r["time_ms"])) for r in rows]
    pts.sort()
    plt.figure(figsize=(8, 5.5))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    labels = ["seq" if x == 0 else str(x) for x in xs]
    plt.bar(range(len(xs)), ys, color=["#59a14f"] + ["#4e79a7"] * (len(xs) - 1))
    plt.xticks(range(len(xs)), labels)
    plt.xlabel("Threads (\"seq\" = sequential reference)")
    plt.ylabel("Wall-clock time (ms)")
    plt.title("Raw Runtime vs Thread Count\n(more threads = MORE time here -- pure overhead, no real parallelism available)")
    for i, y in enumerate(ys):
        plt.text(i, y + 0.5, f"{y:.1f}ms", ha="center", fontsize=9)
    plt.tight_layout()
    _save_and_show("time_vs_threads.png")
    print("saved time_vs_threads.png")


def plot_efficiency():
    rows = load_csv("concurrency_benchmark.csv")
    pts = [(int(r["threads"]), float(r["efficiency"])) for r in rows if int(r["threads"]) > 0]
    pts.sort()
    plt.figure(figsize=(8, 5.5))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    plt.plot(xs, ys, marker="o", color="#f28e2b", linewidth=2, markersize=8)
    plt.axhline(1.0, color="gray", linestyle=":", label="Ideal efficiency (100%)")
    plt.xlabel("Number of threads")
    plt.ylabel("Efficiency (speedup / thread count)")
    plt.title("Parallel Efficiency vs Thread Count\n(efficiency collapses as threads compete for 1 physical core)")
    plt.legend()
    plt.grid(True, ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("efficiency_vs_threads.png")
    print("saved efficiency_vs_threads.png")


if __name__ == "__main__":
    plot_speedup_vs_threads()
    plot_time_vs_threads()
    plot_efficiency()
    print("Done.")
