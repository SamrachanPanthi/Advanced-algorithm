#Dijkstra's shortest-path algorithm, using the Task 1 MinHeap 

import math
from min_heap import MinHeap


def dijkstra(graph, source):
    dist = {v: math.inf for v in graph.nodes()}
    prev = {v: None for v in graph.nodes()}
    dist[source] = 0

    visited = set()
    heap = MinHeap()
    heap.push(0, source)
    order = []

    while not heap.is_empty():
        d, u = heap.pop()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)

        for v, w in graph.neighbors(u):
            if w < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            new_dist = dist[u] + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heap.push(new_dist, v)

    return dist, prev, order


def reconstruct_path(prev, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev.get(node)
    path.reverse()
    return path
