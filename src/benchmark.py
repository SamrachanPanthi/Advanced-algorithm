
import os
import time
import random
import csv as csvmod
import statistics

from data_loader import load_cities, sample_cities
from bst import BST
from avl import AVLTree
from min_heap import MinHeap
from hash_table import HashTableChaining

SIZES = [100, 1_000, 10_000]
REPEATS = 5          # independent rebuilds per (structure, n) for stable timing
N_PROBE = 200         # number of search/delete probes per repeat
OUTPUT_CSV = "../results/benchmark_results.csv"


def time_it(fn, *args, **kwargs):
    start = time.perf_counter()
    fn(*args, **kwargs)
    return (time.perf_counter() - start) * 1000  # ms


# BST/AVL
def bench_tree(tree_cls, cities, rng):
    tree = tree_cls()
    t0 = time.perf_counter()
    for c in cities:
        tree.insert(c.distance, c)
    insert_ms = (time.perf_counter() - t0) * 1000

    probes = rng.sample(cities, min(N_PROBE, len(cities)))
    t0 = time.perf_counter()
    for c in probes:
        tree.search(c.distance)
    search_ms = (time.perf_counter() - t0) * 1000 / len(probes)

    del_probes = rng.sample(cities, min(N_PROBE, len(cities)))
    t0 = time.perf_counter()
    for c in del_probes:
        tree.delete(c.distance)
    delete_ms = (time.perf_counter() - t0) * 1000 / len(del_probes)

    return insert_ms, search_ms, delete_ms


# ------------------------------------------------------------------ Heap
def bench_heap(cities, rng):
    heap = MinHeap()
    t0 = time.perf_counter()
    for c in cities:
        heap.push(c.distance, c)
    insert_ms = (time.perf_counter() - t0) * 1000

    # "search" for a heap is not its purpose (O(n) linear scan) -- instead we
    # measure its core operation: extract-min, repeated N_PROBE times.
    n_pops = min(N_PROBE, len(heap))
    t0 = time.perf_counter()
    for _ in range(n_pops):
        heap.pop()
    pop_ms = (time.perf_counter() - t0) * 1000 / n_pops

    return insert_ms, pop_ms


# ------------------------------------------------------------------ HashTable
def bench_hash(cities, rng):
    def key(c):
        return f"{c.name}|{c.country}|{c.id}"  # unique key per city

    ht = HashTableChaining()
    t0 = time.perf_counter()
    for c in cities:
        ht.insert(key(c), c)
    insert_ms = (time.perf_counter() - t0) * 1000

    probes = rng.sample(cities, min(N_PROBE, len(cities)))
    t0 = time.perf_counter()
    for c in probes:
        ht.search(key(c))
    search_ms = (time.perf_counter() - t0) * 1000 / len(probes)

    del_probes = rng.sample(cities, min(N_PROBE, len(cities)))
    t0 = time.perf_counter()
    for c in del_probes:
        ht.delete(key(c))
    delete_ms = (time.perf_counter() - t0) * 1000 / len(del_probes)

    return insert_ms, search_ms, delete_ms


def run():
    print("Loading dataset...")
    all_cities = load_cities()
    print(f"  {len(all_cities)} cities available\n")

    rows = []
    for n in SIZES:
        print(f"=== n = {n} ===")
        bst_i, bst_s, bst_d = [], [], []
        avl_i, avl_s, avl_d = [], [], []
        heap_i, heap_p = [], []
        hash_i, hash_s, hash_d = [], [], []

        for rep in range(REPEATS):
            rng = random.Random(1000 + rep)
            cities = sample_cities(all_cities, n, seed=2000 + rep)

            i, s, d = bench_tree(BST, cities, rng)
            bst_i.append(i); bst_s.append(s); bst_d.append(d)

            i, s, d = bench_tree(AVLTree, cities, rng)
            avl_i.append(i); avl_s.append(s); avl_d.append(d)

            i, p = bench_heap(cities, rng)
            heap_i.append(i); heap_p.append(p)

            i, s, d = bench_hash(cities, rng)
            hash_i.append(i); hash_s.append(s); hash_d.append(d)

            print(f"  rep {rep + 1}/{REPEATS} done")

        def m(lst):
            return statistics.mean(lst)

        rows.append(dict(structure="BST", n=n, insert_ms=m(bst_i), search_ms=m(bst_s), delete_ms=m(bst_d)))
        rows.append(dict(structure="AVL", n=n, insert_ms=m(avl_i), search_ms=m(avl_s), delete_ms=m(avl_d)))
        rows.append(dict(structure="MinHeap", n=n, insert_ms=m(heap_i), search_ms=m(heap_p), delete_ms=""))
        rows.append(dict(structure="HashTable", n=n, insert_ms=m(hash_i), search_ms=m(hash_s), delete_ms=m(hash_d)))
        print()

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csvmod.DictWriter(f, fieldnames=["structure", "n", "insert_ms", "search_ms", "delete_ms"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results written to {OUTPUT_CSV}")
    return rows


if __name__ == "__main__":
    run()
