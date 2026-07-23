import threading
import numpy as np


def _simulate_edge_cost_computation(weight, workload_size):
    
    arr = np.full(workload_size, weight, dtype=np.float64)
    return float(np.sqrt(arr * 1.7 + 3.0).sum())


def sequential_bfs(graph, source, workload_size=2000):
    visited = {source}
    frontier = [source]
    order = [source]
    while frontier:
        next_frontier = []
        for u in frontier:
            for v, w in graph.neighbors(u):
                _simulate_edge_cost_computation(w, workload_size)
                if v not in visited:
                    visited.add(v)
                    next_frontier.append(v)
                    order.append(v)
        frontier = next_frontier
    return visited, order


class ConcurrentBFS:
    def __init__(self, graph, num_threads, workload_size=2000, max_compute_slots=None):
        self.graph = graph
        self.num_threads = max(1, num_threads)
        self.workload_size = workload_size
        self.visited_lock = threading.Lock()
        self.compute_semaphore = threading.Semaphore(max_compute_slots or self.num_threads)
        self.barrier = threading.Barrier(self.num_threads)

    def run(self, source):
        visited = {source}
        frontier = [source]
        order = [source]

        while frontier:
            next_frontier = []
            chunks = [frontier[i::self.num_threads] for i in range(self.num_threads)]

            def worker(my_chunk):
                local_new = []
                for u in my_chunk:
                    for v, w in self.graph.neighbors(u):
                        with self.compute_semaphore:
                            _simulate_edge_cost_computation(w, self.workload_size)
                        with self.visited_lock:
                            if v not in visited:
                                visited.add(v)
                                local_new.append(v)
                if local_new:
                    with self.visited_lock:
                        next_frontier.extend(local_new)
                        order.extend(local_new)
                self.barrier.wait()

            threads = [threading.Thread(target=worker, args=(chunk,)) for chunk in chunks]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            frontier = next_frontier

        return visited, order
