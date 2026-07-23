"""Weighted directed graph for the transportation network, stored as an
adjacency list.

Adjacency list over adjacency matrix because road networks are sparse -
each city only connects to a handful of others, not to every city in the
country. That means O(V+E) memory instead of O(V^2), and Dijkstra/Prim/
Bellman-Ford only ever need to iterate over a node's real neighbours,
which an adjacency list gives directly.
"""

from collections import defaultdict


class DirectedGraph:
    def __init__(self):
        self._adj = defaultdict(list)
        self._nodes = set()
        self._node_data = {}

    def add_node(self, node, data=None):
        self._nodes.add(node)
        if data is not None:
            self._node_data[node] = data

    def add_edge(self, u, v, weight):
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append((v, weight))

    def neighbors(self, u):
        return self._adj[u]

    def nodes(self):
        return self._nodes

    def node_data(self, u):
        return self._node_data.get(u)

    def num_nodes(self):
        return len(self._nodes)

    def num_edges(self):
        return sum(len(v) for v in self._adj.values())

    def edge_list(self):
        return [(u, v, w) for u, edges in self._adj.items() for v, w in edges]

    def density(self):
        v = self.num_nodes()
        max_edges = v * (v - 1)
        return self.num_edges() / max_edges if max_edges else 0

    def to_undirected(self):
        """Build an undirected graph for Prim's MST. Where a directed edge
        exists both ways with different weights, use the cheaper one."""
        und = UndirectedGraph()
        for u in self._nodes:
            und.add_node(u, self._node_data.get(u))
        seen = set()
        for u, edges in self._adj.items():
            for v, w in edges:
                key = (u, v) if u <= v else (v, u)
                if key in seen:
                    continue
                reverse_w = None
                for v2, w2 in self._adj.get(v, []):
                    if v2 == u:
                        reverse_w = w2
                        break
                final_w = min(w, reverse_w) if reverse_w is not None else w
                und.add_edge(u, v, final_w)
                seen.add(key)
        return und


class UndirectedGraph:
    """Simple undirected weighted graph - only used as Prim's MST input."""

    def __init__(self):
        self._adj = defaultdict(list)
        self._nodes = set()
        self._node_data = {}

    def add_node(self, node, data=None):
        self._nodes.add(node)
        if data is not None:
            self._node_data[node] = data

    def add_edge(self, u, v, weight):
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append((v, weight))
        self._adj[v].append((u, weight))

    def neighbors(self, u):
        return self._adj[u]

    def nodes(self):
        return self._nodes

    def node_data(self, u):
        return self._node_data.get(u)

    def num_nodes(self):
        return len(self._nodes)

    def num_edges(self):
        return sum(len(v) for v in self._adj.values()) // 2
