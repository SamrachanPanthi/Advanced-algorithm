
from min_heap import MinHeap
def prim(undirected_graph, source):
    visited = {source}
    mst_edges = []
    heap = MinHeap()

    for v, w in undirected_graph.neighbors(source):
        heap.push(w, (source, v))

    total_nodes = undirected_graph.num_nodes()

    while not heap.is_empty() and len(visited) < total_nodes:
        w, (u, v) = heap.pop()
        if v in visited:
            continue
        visited.add(v)
        mst_edges.append((u, v, w))
        for v2, w2 in undirected_graph.neighbors(v):
            if v2 not in visited:
                heap.push(w2, (v, v2))

    total_weight = sum(w for _, _, w in mst_edges)
    connected = len(visited) == total_nodes
    return mst_edges, total_weight, connected
