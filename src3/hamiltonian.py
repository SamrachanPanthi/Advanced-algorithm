"""
hamiltonian.py
--------------
Task 3.3 - Backtracking: Hamiltonian Cycle.

Given an undirected graph (as an adjacency matrix), determine whether a
cycle exists that visits every vertex exactly once and returns to the
starting vertex. This is NP-complete, so in the worst case there is no
known way to avoid exploring an exponential number of candidate paths --
backtracking with pruning is the standard approach.

Pruning strategy:
    We build the path one vertex at a time. Before adding a candidate
    vertex v to the path, we check:
        1. is v adjacent to the last vertex placed?              (edge exists)
        2. has v already been visited in this path?              (no repeats)
    If either check fails, that branch is abandoned immediately -- we never
    explore any of the (n - depth)! orderings that would have followed it.
    This is what keeps the algorithm usable in practice even though its
    worst-case complexity is still O(n!).
"""

import os


class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = [[0] * n for _ in range(n)]

    def add_edge(self, u, v):
        self.adj[u][v] = 1
        self.adj[v][u] = 1


def _is_safe(v, adj, path, pos):
    """Check both pruning conditions for placing vertex v at path[pos]."""
    if adj[path[pos - 1]][v] == 0:
        return False  # no edge from the previous vertex to v
    if v in path[:pos]:
        return False  # v already used earlier in this path
    return True


def _solve(adj, path, pos, n):
    if pos == n:
        # All n vertices placed -- just need an edge back to the start
        return adj[path[pos - 1]][path[0]] == 1

    for v in range(1, n):  # vertex 0 is fixed as the start
        if _is_safe(v, adj, path, pos):
            path[pos] = v
            if _solve(adj, path, pos + 1, n):
                return True
            path[pos] = -1  # backtrack: undo the choice and try the next v

    return False


def hamiltonian_cycle(graph):
    """
    Returns a list of vertices forming a Hamiltonian cycle (starting and
    ending at vertex 0), or None if no such cycle exists.
    """
    n = graph.n
    if n == 0:
        return None

    path = [-1] * n
    path[0] = 0  # fix vertex 0 as the starting point (a cycle has no fixed
    # "start", so this cuts the search space by a factor of n with no loss
    # of correctness)

    if _solve(graph.adj, path, 1, n):
        return path + [path[0]]
    return None


if __name__ == "__main__":
    # Worked example: a 5-cycle plus one shortcut edge, which does contain
    # a Hamiltonian cycle (the outer 0-1-2-3-4-0 ring).
    g = Graph(5)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]:
        g.add_edge(u, v)

    result = hamiltonian_cycle(g)
    print("Graph with a Hamiltonian cycle:")
    print("  Cycle found:" if result else "  No cycle found:", result)

    # Worked example: a "star" graph (one hub connected to 4 leaves, leaves
    # not connected to each other) -- no Hamiltonian cycle can exist here,
    # since any leaf would need two neighbours to be part of a cycle.
    g2 = Graph(5)
    for leaf in [1, 2, 3, 4]:
        g2.add_edge(0, leaf)

    result2 = hamiltonian_cycle(g2)
    print("\nStar graph (no Hamiltonian cycle should exist):")
    print("  Cycle found:" if result2 else "  No cycle found (correct):", result2)
