#Turns graph_benchmark_results.csv into comparison charts

import os
import csv
import matplotlib
import matplotlib.pyplot as plt  # not forcing Agg, so plots also show on screen

IN_CSV = "../results2/graph_benchmark_results.csv"
PLOTS_DIR = "../results2/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def _save_and_show(fname):
    plt.savefig(f"{PLOTS_DIR}/{fname}", dpi=150)
    try:
        plt.show()
    except Exception:
        pass
    plt.close()
COLORS = {"Dijkstra": "#4e79a7", "Prim": "#59a14f", "BellmanFord": "#e15759"}


def load():
    rows = []
    with open(IN_CSV) as f:
        for row in csv.DictReader(f):
            row["V"] = int(row["V"])
            row["E"] = int(row["E"])
            row["time_ms"] = float(row["time_ms"])
            row["theoretical_ops"] = float(row["theoretical_ops"])
            row["observed_constant"] = float(row["observed_constant"])
            rows.append(row)
    return rows


def plot_runtime_vs_v(rows, graph_type, fname, title):
    plt.figure(figsize=(7, 5))
    algos = ["Dijkstra", "Prim", "BellmanFord"]
    for algo in algos:
        subset = sorted([r for r in rows if r["algorithm"] == algo and r["graph_type"] == graph_type],
                         key=lambda r: r["V"])
        if not subset:
            continue
        plt.plot([r["V"] for r in subset], [r["time_ms"] for r in subset],
                  marker="o", label=algo, color=COLORS[algo])
    plt.xlabel("Number of nodes (V)")
    plt.ylabel("Runtime (ms, log scale)")
    plt.yscale("log")
    plt.title(title)
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show(fname)
    print(f"saved {fname}")


def plot_constant_factor(rows):
    algos = ["Dijkstra", "Prim", "BellmanFord"]
    fig, ax = plt.subplots(figsize=(8, 5))
    for algo in algos:
        subset = [r for r in rows if r["algorithm"] == algo]
        vals = [r["observed_constant"] for r in subset]
        mean_val = sum(vals) / len(vals)
        ax.bar(algo, mean_val, color=COLORS[algo])
        ax.text(algo, mean_val * 1.05, f"{mean_val:.2e}", ha="center", fontsize=9)
    ax.set_ylabel("Observed constant\n(measured ms / theoretical op count)")
    ax.set_title("Observed Constant Factor per Algorithm\n(mean across all benchmark runs)")
    ax.set_yscale("log")
    plt.tight_layout()
    _save_and_show("observed_constant_factor.png")
    print("saved observed_constant_factor.png")


def plot_sparse_vs_dense(rows):
    algos = ["Dijkstra", "Prim", "BellmanFord"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
    for ax, algo in zip(axes, algos):
        sparse = sorted([r for r in rows 
                         if r["algorithm"] == algo and r["graph_type"] == "sparse_knn6"], 
                         key=lambda r: r["V"])
        dense = sorted([r for r in rows if r["algorithm"] == algo and r["graph_type"] == "dense"], key=lambda r: r["V"])
        ax.plot([r["V"] for r in sparse], [r["time_ms"] for r in sparse], marker="o", label="Sparse (k-NN)", color="#4e79a7")
        ax.plot([r["V"] for r in dense], [r["time_ms"] for r in dense], marker="s", label="Dense (near-complete)", color="#e15759")
        ax.set_yscale("log")
        ax.set_xlabel("V")
        ax.set_ylabel("Runtime (ms, log scale)")
        ax.set_title(algo)
        ax.legend(fontsize=9)
        ax.grid(True, which="both", ls="--", alpha=0.4)
    fig.suptitle("Sparse vs Dense Graph Runtime, per Algorithm", fontsize=14)
    plt.tight_layout()
    _save_and_show("sparse_vs_dense.png")
    print("saved sparse_vs_dense.png")


if __name__ == "__main__":
    rows = load()
    plot_runtime_vs_v(rows, "sparse_knn6", "runtime_vs_v_sparse.png",
                       "Runtime vs V — Sparse Graphs (k-NN, k=6)")
    plot_runtime_vs_v(rows, "dense", "runtime_vs_v_dense.png",
                       "Runtime vs V — Dense Graphs (~90% of all possible edges)")
    plot_sparse_vs_dense(rows)
    plot_constant_factor(rows)
    print("Done.")
