from network_builder import build_knn_graph
from data_loader import load_cities
from concurrent_bfs import sequential_bfs, ConcurrentBFS


def _build_test_graph(n=60, k=6):
    cities = load_cities()
    uk = [c for c in cities if c.country == "United Kingdom"]
    uk_sorted = sorted(uk, key=lambda c: -c.population)[:n]
    return build_knn_graph(uk_sorted, k=k), uk_sorted[0].id


def test_concurrent_matches_sequential_reachable_set():
    graph, source = _build_test_graph()
    seq_visited, _ = sequential_bfs(graph, source, workload_size=50)
    for threads in [1, 2, 4, 8]:
        cbfs = ConcurrentBFS(graph, num_threads=threads, workload_size=50)
        conc_visited, _ = cbfs.run(source)
        assert conc_visited == seq_visited, f"threads={threads}: visited set differs from sequential!"
    print("  Concurrent BFS reaches the same node set as sequential, at 1/2/4/8 threads -- OK")


def test_no_duplicate_visits_under_stress():
    graph, source = _build_test_graph(n=80, k=8)
    for trial in range(20):
        cbfs = ConcurrentBFS(graph, num_threads=8, workload_size=20)
        visited, order = cbfs.run(source)
        assert len(order) == len(set(order)), f"trial {trial}: duplicate node -- race condition!"
        assert len(order) == len(visited), f"trial {trial}: length mismatch -- race condition!"
    print("  20 stress-test runs at 8 threads: no duplicate visits, no lost updates -- OK")


def test_all_nodes_reachable_from_dense_source():
    graph, source = _build_test_graph(n=50, k=15)
    seq_visited, _ = sequential_bfs(graph, source, workload_size=20)
    cbfs = ConcurrentBFS(graph, num_threads=4, workload_size=20)
    conc_visited, _ = cbfs.run(source)
    assert conc_visited == seq_visited
    print(f"  Dense graph: both reach {len(seq_visited)}/{graph.num_nodes()} nodes -- OK")


if __name__ == "__main__":
    test_concurrent_matches_sequential_reachable_set()
    test_no_duplicate_visits_under_stress()
    test_all_nodes_reachable_from_dense_source()
    print("\nAll Task 5 correctness/race-condition checks passed.")
