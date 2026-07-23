import os
import csv
import matplotlib
import matplotlib.pyplot as plt

IN_CSV = "../results4/heuristic_benchmark.csv"
PLOTS_DIR = "../results4/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)
COLORS = {"Greedy": "#e15759", "LocalSearch": "#4e79a7", "SimulatedAnnealing": "#59a14f"}


def _save_and_show(fname):
    plt.savefig(f"{PLOTS_DIR}/{fname}", dpi=150)
    try:
        plt.show()
    except Exception:
        pass
    plt.close()


def load():
    rows = []
    with open(IN_CSV) as f:
        for row in csv.DictReader(f):
            row["n"] = int(row["n"])
            row["distance_km"] = float(row["distance_km"])
            row["vehicles"] = float(row["vehicles"])
            row["time_ms"] = float(row["time_ms"])
            rows.append(row)
    return rows


def plot_quality(rows):
    plt.figure(figsize=(8, 5.5))
    for algo in ["Greedy", "LocalSearch", "SimulatedAnnealing"]:
        subset = sorted([r for r in rows if r["algorithm"] == algo], key=lambda r: r["n"])
        plt.plot([r["n"] for r in subset], [r["distance_km"] for r in subset],
                  marker="o", color=COLORS[algo], label=algo)
    plt.xlabel("n (number of customers)")
    plt.ylabel("Total route distance (km) -- lower is better")
    plt.title("Solution Quality: Total Distance vs Problem Size")
    plt.legend()
    plt.grid(True, ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("quality_vs_n.png")
    print("saved quality_vs_n.png")


def plot_runtime(rows):
    plt.figure(figsize=(8, 5.5))
    for algo in ["Greedy", "LocalSearch", "SimulatedAnnealing"]:
        subset = sorted([r for r in rows if r["algorithm"] == algo], key=lambda r: r["n"])
        plt.plot([r["n"] for r in subset], [r["time_ms"] for r in subset],
                  marker="o", color=COLORS[algo], label=algo)
    plt.yscale("log")
    plt.xlabel("n (number of customers)")
    plt.ylabel("Runtime (ms, log scale)")
    plt.title("Runtime vs Problem Size")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("runtime_vs_n.png")
    print("saved runtime_vs_n.png")


def plot_quality_vs_runtime(rows):
    """Trade-off scatter: for each n, quality improvement (%) vs extra runtime,
    relative to greedy's baseline."""
    plt.figure(figsize=(8, 5.5))
    ns = sorted(set(r["n"] for r in rows))
    for algo, marker in [("LocalSearch", "o"), ("SimulatedAnnealing", "s")]:
        xs, ys = [], []
        for n in ns:
            g = next(r for r in rows if r["algorithm"] == "Greedy" and r["n"] == n)
            a = next(r for r in rows if r["algorithm"] == algo and r["n"] == n)
            improvement_pct = 100 * (g["distance_km"] - a["distance_km"]) / g["distance_km"]
            extra_time_ms = a["time_ms"] - g["time_ms"]
            xs.append(extra_time_ms)
            ys.append(improvement_pct)
            plt.annotate(f"n={n}", (extra_time_ms, improvement_pct), fontsize=8,
                         textcoords="offset points", xytext=(5, 5))
        plt.plot(xs, ys, marker=marker, color=COLORS[algo], label=algo, linestyle="--", alpha=0.7)
    plt.xscale("log")
    plt.xlabel("Extra runtime vs greedy (ms, log scale)")
    plt.ylabel("Distance improvement over greedy (%)")
    plt.title("Quality-vs-Cost Trade-off (relative to Greedy baseline)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("quality_vs_cost_tradeoff.png")
    print("saved quality_vs_cost_tradeoff.png")


def plot_vehicles(rows):
    plt.figure(figsize=(8, 5.5))
    for algo in ["Greedy", "LocalSearch", "SimulatedAnnealing"]:
        subset = sorted([r for r in rows if r["algorithm"] == algo], key=lambda r: r["n"])
        plt.plot([r["n"] for r in subset], [r["vehicles"] for r in subset],
                  marker="o", color=COLORS[algo], label=algo)
    plt.xlabel("n (number of customers)")
    plt.ylabel("Vehicles used -- lower is better")
    plt.title("Fleet Size Required vs Problem Size")
    plt.legend()
    plt.grid(True, ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("vehicles_vs_n.png")
    print("saved vehicles_vs_n.png")


if __name__ == "__main__":
    rows = load()
    plot_quality(rows)
    plot_runtime(rows)
    plot_quality_vs_runtime(rows)
    plot_vehicles(rows)
    print("Done.")
