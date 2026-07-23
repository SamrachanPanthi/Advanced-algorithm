import os
import matplotlib
import matplotlib.pyplot as plt

from vrptw import generate_instance
from heuristic_greedy import greedy_construction
from heuristic_local_search import local_search
from heuristic_simulated_annealing import simulated_annealing

PLOTS_DIR = "../results4/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)
ROUTE_COLORS = plt.cm.tab10.colors


def _save_and_show(fname):
    plt.savefig(f"{PLOTS_DIR}/{fname}", dpi=150)
    try:
        plt.show()
    except Exception:
        pass
    plt.close()


def _plot_routes_on_axis(ax, instance, routes, title):
    depot = instance.points[0]
    ax.scatter([depot.lng], [depot.lat], s=160, color="black", marker="s", zorder=5, label="Depot")
    for i, route in enumerate(routes):
        color = ROUTE_COLORS[i % len(ROUTE_COLORS)]
        path = [0] + route + [0]
        xs = [instance.points[c].lng for c in path]
        ys = [instance.points[c].lat for c in path]
        ax.plot(xs, ys, color=color, marker="o", markersize=5, linewidth=1.6, zorder=3)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")


def plot_route_comparison():
    inst = generate_instance(n_customers=25, vehicle_capacity=100, seed=3)
    routes_g, dropped = greedy_construction(inst)
    routes_ls, _ = local_search(inst, routes_g)
    routes_sa, _ = simulated_annealing(inst, routes_g, iterations=3000, seed=1)

    d_g = inst.solution_distance(routes_g)
    d_ls = inst.solution_distance(routes_ls)
    d_sa = inst.solution_distance(routes_sa)

    fig, axes = plt.subplots(1, 3, figsize=(19, 6.5))
    _plot_routes_on_axis(axes[0], inst, routes_g, f"Greedy Construction\n{len(routes_g)} vehicles, {d_g:.0f}km")
    _plot_routes_on_axis(axes[1], inst, routes_ls, f"+ Local Search (2-opt/or-opt)\n{len(routes_ls)} vehicles, {d_ls:.0f}km")
    _plot_routes_on_axis(axes[2], inst, routes_sa, f"Simulated Annealing\n{len(routes_sa)} vehicles, {d_sa:.0f}km")
    fig.suptitle(f"VRPTW Solutions: {inst.n} UK cities served from {inst.depot.name}", fontsize=14)
    plt.tight_layout()
    _save_and_show("route_comparison.png")
    print("saved route_comparison.png")


def plot_sa_convergence():
    inst = generate_instance(n_customers=30, vehicle_capacity=100, seed=3)
    routes_g, dropped = greedy_construction(inst)
    routes_sa, history = simulated_annealing(inst, routes_g, iterations=5000, t0=50.0, cooling_rate=0.998, seed=1)

    iters = [h[0] for h in history]
    current_costs = [h[1] for h in history]
    best_costs = [h[2] for h in history]

    plt.figure(figsize=(9, 5.5))
    plt.plot(iters, current_costs, color="#f28e2b", alpha=0.6, linewidth=1, label="Current solution (accepted moves, incl. worse ones)")
    plt.plot(iters, best_costs, color="#4e79a7", linewidth=2, label="Best solution found so far")
    plt.axhline(inst.solution_distance(routes_g), color="#e15759", linestyle="--", label="Greedy starting point")
    plt.xlabel("Iteration")
    plt.ylabel("Total distance (km)")
    plt.title("Simulated Annealing Convergence\n(note early acceptance of worse moves while temperature is high)")
    plt.legend()
    plt.grid(True, ls="--", alpha=0.4)
    plt.tight_layout()
    _save_and_show("sa_convergence.png")
    print("saved sa_convergence.png")


if __name__ == "__main__":
    plot_route_comparison()
    plot_sa_convergence()
    print("Done.")
