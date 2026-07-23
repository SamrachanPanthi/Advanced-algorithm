"""Reads benchmark_results.csv and plots insert/search/delete time vs n
for all four structures, plus a growth-multiplier chart comparing the
measured slowdown (1000 -> 10000 nodes) to the theoretical prediction.
"""

import os
import csv
import math
import matplotlib
# not forcing the Agg backend here so plots also pop up on screen when run
# on a normal desktop - falls back fine if there's no display available
# actually opens a window. If this script is run in a headless environment
# with no display, plt.show() will simply be skipped (see try/except below)
# and the PNG files are still saved as normal.
import matplotlib.pyplot as plt

RESULTS_CSV = "../results/benchmark_results.csv"
PLOTS_DIR = "../results/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def _save_and_show(fname):
    """Save the current figure to PLOTS_DIR and also pop it up on screen.
    Close the window to continue to the next plot."""
    plt.savefig(f"{PLOTS_DIR}/{fname}", dpi=150)
    try:
        plt.show()
    except Exception:
        pass  # no display available (e.g. running on a headless server) -- file is still saved
    plt.close()

COLORS = {"BST": "#e15759", "AVL": "#4e79a7", "MinHeap": "#59a14f", "HashTable": "#f28e2b"}


def load_results():
    data = {}  # structure -> {n: {insert, search, delete}}
    with open(RESULTS_CSV) as f:
        for row in csv.DictReader(f):
            s, n = row["structure"], int(row["n"])
            data.setdefault(s, {})[n] = {
                "insert": float(row["insert_ms"]),
                "search": float(row["search_ms"]),
                "delete": float(row["delete_ms"]) if row["delete_ms"] else None,
            }
    return data


def plot_metric(data, metric, ylabel, title, fname, per_op=False):
    plt.figure(figsize=(7, 5))
    ns = [100, 1000, 10000]
    for structure, series in data.items():
        ys = [series[n][metric] for n in ns if series[n][metric] is not None]
        xs = [n for n in ns if series[n][metric] is not None]
        if not ys:
            continue
        plt.plot(xs, ys, marker="o", label=structure, color=COLORS.get(structure))
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of nodes (n)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show(fname)
    print(f"  saved {fname}")


def plot_growth_multiplier(data):
    """Bar chart: how much slower is each op at n=10,000 vs n=1,000 (empirical),
    against the theoretical expectation for O(log n) vs O(n)."""
    structures = ["BST", "AVL", "HashTable"]
    metrics = ["insert", "search", "delete"]
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharey=True)
    log_ratio_theoretical = math.log10(10000) / math.log10(1000)  # ~1.33x for O(log n)
    linear_ratio_theoretical = 10  # 10x for O(n)

    for ax, metric in zip(axes, metrics):
        vals = []
        for s in structures:
            v1000 = data[s][1000][metric]
            v10000 = data[s][10000][metric]
            if v1000 and v10000:
                vals.append(v10000 / v1000)
            else:
                vals.append(0)
        bars = ax.bar(structures, vals, color=[COLORS[s] for s in structures])
        ax.axhline(log_ratio_theoretical, color="gray", ls="--",
                    label=f"O(log n) expected (~{log_ratio_theoretical:.1f}x)")
        ax.axhline(linear_ratio_theoretical, color="black", ls=":",
                    label=f"O(n) expected ({linear_ratio_theoretical}x)")
        ax.set_title(f"{metric.capitalize()}: n=1,000 -> n=10,000")
        ax.set_ylabel("Slowdown multiplier (x)")
        ax.legend(fontsize=8)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 0.15, f"{v:.2f}x",
                     ha="center", fontsize=9)
    plt.tight_layout()
    _save_and_show("growth_multiplier.png")
    print("  saved growth_multiplier.png")


def plot_bar_at_10000(data):
    """Simple grouped bar chart comparing all 4 structures at n=10,000."""
    structures = list(data.keys())
    metrics = ["insert", "search", "delete"]
    x = range(len(structures))
    width = 0.25
    plt.figure(figsize=(8, 5))
    for i, metric in enumerate(metrics):
        vals = [data[s][10000][metric] or 0 for s in structures]
        plt.bar([xi + i * width for xi in x], vals, width=width, label=metric)
    plt.xticks([xi + width for xi in x], structures)
    plt.yscale("log")
    plt.ylabel("Time (ms, log scale)")
    plt.title("Operation cost at n = 10,000 (lower is better)")
    plt.legend()
    plt.tight_layout()
    _save_and_show("comparison_at_10000.png")
    print("  saved comparison_at_10000.png")


if __name__ == "__main__":
    data = load_results()
    print("Generating plots...")
    plot_metric(data, "insert", "Bulk insert time (ms, log scale)",
                "Insertion time vs n (all n cities inserted)", "insert_time_vs_n.png")
    plot_metric(data, "search", "Avg. per-op search time (ms, log scale)",
                "Search time vs n (avg over 200 lookups)", "search_time_vs_n.png")
    plot_metric(data, "delete", "Avg. per-op delete time (ms, log scale)",
                "Delete time vs n (avg over 200 deletes)", "delete_time_vs_n.png")
    plot_growth_multiplier(data)
    plot_bar_at_10000(data)
    print("Done.")
