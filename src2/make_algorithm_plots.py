"""Builds the 150-city UK network and plots Dijkstra's shortest-path tree
and Prim's MST growing outward from London, step by step, using real
lat/lng coordinates so the shape is geographically meaningful.
"""

import os
import matplotlib
import matplotlib.pyplot as plt  # not forcing Agg, so plots also show on screen

from data_loader import load_cities
from network_builder import build_knn_graph
from dijkstra import dijkstra
from prim import prim

PLOTS_DIR = "../results2/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def _save_and_show(fname):
    plt.savefig(f"{PLOTS_DIR}/{fname}", dpi=150)
    try:
        plt.show()
    except Exception:
        pass
    plt.close()


def build_demo_graph(n_cities=150, k=14):
    cities = load_cities()
    uk = [c for c in cities if c.country == "United Kingdom"]
    uk_sorted = sorted(uk, key=lambda c: -c.population)[:n_cities]
    g = build_knn_graph(uk_sorted, k=k)
    return g, uk_sorted


def _scatter_base(ax, graph):
    xs = [graph.node_data(n).lng for n in graph.nodes()]
    ys = [graph.node_data(n).lat for n in graph.nodes()]
    ax.scatter(xs, ys, s=10, color="lightgray", zorder=1)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")


def plot_dijkstra_steps(graph, source, order, prev):
    fig, axes = plt.subplots(1, 4, figsize=(20, 5.2))
    fractions = [0.25, 0.5, 0.75, 1.0]
    src_data = graph.node_data(source)

    for ax, frac in zip(axes, fractions):
        _scatter_base(ax, graph)
        n_shown = max(1, int(len(order) * frac))
        finalised = set(order[:n_shown])
        # draw tree edges among finalised nodes
        for node in finalised:
            p = prev.get(node)
            if p is not None and p in finalised:
                pd, nd = graph.node_data(p), graph.node_data(node)
                ax.plot([pd.lng, nd.lng], [pd.lat, nd.lat], color="#4e79a7", linewidth=1.1, zorder=2)
        fx = [graph.node_data(n).lng for n in finalised]
        fy = [graph.node_data(n).lat for n in finalised]
        ax.scatter(fx, fy, s=16, color="#4e79a7", zorder=3)
        ax.scatter([src_data.lng], [src_data.lat], s=90, color="#e15759", marker="*", zorder=4, label="Source (London)")
        ax.set_title(f"{int(frac*100)}% of nodes finalised\n({n_shown}/{len(order)} cities)")
        ax.legend(fontsize=8, loc="lower left")

    fig.suptitle("Dijkstra's Algorithm: Shortest-Path Tree Growing from London", fontsize=14)
    plt.tight_layout()
    _save_and_show("dijkstra_steps.png")
    print("saved dijkstra_steps.png")


def plot_prim_steps(undirected_graph, source, mst_edges):
    fig, axes = plt.subplots(1, 4, figsize=(20, 5.2))
    fractions = [0.25, 0.5, 0.75, 1.0]
    src_data = undirected_graph.node_data(source)
    total_edges = len(mst_edges)

    for ax, frac in zip(axes, fractions):
        _scatter_base(ax, undirected_graph)
        n_shown = max(1, int(total_edges * frac))
        shown_edges = mst_edges[:n_shown]
        included_nodes = {source}
        for u, v, w in shown_edges:
            ud, vd = undirected_graph.node_data(u), undirected_graph.node_data(v)
            ax.plot([ud.lng, vd.lng], [ud.lat, vd.lat], color="#59a14f", linewidth=1.3, zorder=2)
            included_nodes.add(u)
            included_nodes.add(v)
        nx = [undirected_graph.node_data(n).lng for n in included_nodes]
        ny = [undirected_graph.node_data(n).lat for n in included_nodes]
        ax.scatter(nx, ny, s=16, color="#59a14f", zorder=3)
        ax.scatter([src_data.lng], [src_data.lat], s=90, color="#e15759", marker="*", zorder=4, label="Start (London)")
        ax.set_title(f"{int(frac*100)}% of MST edges added\n({n_shown}/{total_edges} edges)")
        ax.legend(fontsize=8, loc="lower left")

    fig.suptitle("Prim's Algorithm: Minimum Spanning Tree Growing from London", fontsize=14)
    plt.tight_layout()
    _save_and_show("prim_steps.png")
    print("saved prim_steps.png")


def plot_final_comparison(graph, undirected_graph, source, prev, order, mst_edges):
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))

    ax = axes[0]
    _scatter_base(ax, graph)
    for node in order:
        p = prev.get(node)
        if p is not None:
            pd, nd = graph.node_data(p), graph.node_data(node)
            ax.plot([pd.lng, nd.lng], [pd.lat, nd.lat], color="#4e79a7", linewidth=1.1, zorder=2)
    src_data = graph.node_data(source)
    ax.scatter([src_data.lng], [src_data.lat], s=100, color="#e15759", marker="*", zorder=4)
    ax.set_title(f"Final Dijkstra Shortest-Path Tree\n({len(order)} cities reached)")

    ax = axes[1]
    _scatter_base(ax, undirected_graph)
    for u, v, w in mst_edges:
        ud, vd = undirected_graph.node_data(u), undirected_graph.node_data(v)
        ax.plot([ud.lng, vd.lng], [ud.lat, vd.lat], color="#59a14f", linewidth=1.3, zorder=2)
    ax.scatter([src_data.lng], [src_data.lat], s=100, color="#e15759", marker="*", zorder=4)
    total_w = sum(w for _, _, w in mst_edges)
    ax.set_title(f"Final Prim MST\n(total weight = {total_w:,.0f} km, {len(mst_edges)} edges)")

    plt.tight_layout()
    _save_and_show("final_tree_vs_mst.png")
    print("saved final_tree_vs_mst.png")


if __name__ == "__main__":
    graph, uk_sorted = build_demo_graph()
    london = [c for c in uk_sorted if c.name == "London"][0]
    print(f"Demo network: V={graph.num_nodes()}, E={graph.num_edges()}, density={graph.density():.3f}")

    dist, prev, order = dijkstra(graph, london.id)
    print(f"Dijkstra reached {len(order)}/{graph.num_nodes()} cities")

    und = graph.to_undirected()
    mst_edges, total_weight, connected = prim(und, london.id)
    print(f"Prim MST: {len(mst_edges)} edges, total weight={total_weight:.1f}km, connected={connected}")

    plot_dijkstra_steps(graph, london.id, order, prev)
    plot_prim_steps(und, london.id, mst_edges)
    plot_final_comparison(graph, und, london.id, prev, order, mst_edges)
