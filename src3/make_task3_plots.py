"""
make_task3_plots.py
--------------------
Reads results3/task3_benchmark_results.csv and produces the graphs for the
Task 3 report:
  1. Matrix Chain Multiplication: runtime vs number of matrices (cubic growth)
  2. Minimum Number of Platforms: runtime vs number of trains (n log n growth)
  3. Hamiltonian Cycle: runtime vs number of vertices, has-cycle case vs the
     worst-case (no-cycle) case on a log-y axis, showing the exponential
     blow-up in the worst case compared to the pruned "easy" case
"""

import os
import csv
import matplotlib
# NOTE: no matplotlib.use("Agg") -- lets an interactive backend be picked
# automatically on a normal desktop so plt.show() opens a real window.
import matplotlib.pyplot as plt

# Anchor these paths to this file's own location, not the terminal's working
# directory, so this still works when run by clicking "Run" in VS Code.
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
IN_CSV = os.path.join(THIS_DIR, "..", "results3", "task3_benchmark_results.csv")
PLOTS_DIR = os.path.join(THIS_DIR, "..", "results3", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)


def _save_and_show(fname):
    plt.savefig(os.path.join(PLOTS_DIR, fname), dpi=150)
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
            row["time_ms"] = float(row["time_ms"])
            rows.append(row)
    return rows


def plot_matrix_chain(rows):
    subset = sorted([r for r in rows if r["algorithm"] == "MatrixChain"], key=lambda r: r["n"])
    plt.figure(figsize=(7, 5))
    plt.plot([r["n"] for r in subset], [r["time_ms"] for r in subset], marker="o", color="#4e79a7")
    plt.xlabel("Number of matrices (n)")
    plt.ylabel("Runtime (ms)")
    plt.title("Matrix Chain Multiplication (DP) -- Runtime vs n\n(expected O(n^3) growth)")
    plt.grid(True, ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("matrix_chain_runtime.png")
    print("saved matrix_chain_runtime.png")


def plot_platforms(rows):
    subset = sorted([r for r in rows if r["algorithm"] == "MinPlatforms"], key=lambda r: r["n"])
    plt.figure(figsize=(7, 5))
    plt.plot([r["n"] for r in subset], [r["time_ms"] for r in subset], marker="o", color="#59a14f")
    plt.xlabel("Number of trains (n)")
    plt.ylabel("Runtime (ms)")
    plt.xscale("log")
    plt.title("Minimum Number of Platforms (Greedy) -- Runtime vs n\n(expected O(n log n) growth)")
    plt.grid(True, ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("platforms_runtime.png")
    print("saved platforms_runtime.png")


def plot_hamiltonian(rows):
    has_cycle = sorted([r for r in rows if r["algorithm"] == "HamiltonianCycle_HasCycle"], key=lambda r: r["n"])
    no_cycle = sorted([r for r in rows if r["algorithm"] == "HamiltonianCycle_NoCycle"], key=lambda r: r["n"])

    plt.figure(figsize=(7, 5))
    plt.plot([r["n"] for r in has_cycle], [r["time_ms"] for r in has_cycle],
              marker="o", label="Has a cycle (pruning very effective)", color="#59a14f")
    plt.plot([r["n"] for r in no_cycle], [r["time_ms"] for r in no_cycle],
              marker="s", label="Worst case: dense, no cycle exists", color="#e15759")
    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Runtime (ms, log scale)")
    plt.yscale("log")
    plt.title("Hamiltonian Cycle (Backtracking) -- Runtime vs n\n"
              "Pruning keeps the easy case fast; the true worst case still explodes")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("hamiltonian_runtime.png")
    print("saved hamiltonian_runtime.png")


if __name__ == "__main__":
    rows = load()
    plot_matrix_chain(rows)
    plot_platforms(rows)
    plot_hamiltonian(rows)
    print("Done.")
