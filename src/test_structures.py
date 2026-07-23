"""Quick correctness checks for the four data structures."""

import math
from bst import BST
from avl import AVLTree
from min_heap import MinHeap
from hash_table import HashTableChaining
from data_loader import load_cities, sample_cities


def check_bst_avl(cities):
    bst, avl = BST(), AVLTree()
    for c in cities:
        bst.insert(c.distance, c)
        avl.insert(c.distance, c)

    assert len(bst) == len(cities)
    assert len(avl) == len(cities)

    bst_keys = [k for k, _ in bst.inorder()]
    avl_keys = [k for k, _ in avl.inorder()]
    assert bst_keys == sorted(bst_keys)
    assert avl_keys == sorted(avl_keys)
    assert bst_keys == avl_keys

    n = len(cities)
    max_allowed_height = 1.45 * math.log2(n + 2)
    assert avl.height() <= max_allowed_height, "AVL is not staying balanced!"
    print(f"  BST height = {bst.height()}, AVL height = {avl.height()} "
          f"(ideal log2(n) = {math.log2(n):.1f}) -- OK")

    probe = cities[len(cities) // 2]
    assert probe in bst.search(probe.distance)
    assert probe in avl.search(probe.distance)

    target = cities[0]
    assert bst.delete(target.distance)
    assert avl.delete(target.distance)
    assert len(bst) == len(cities) - 1
    assert len(avl) == len(cities) - 1
    print("  BST/AVL insert-search-delete: OK")


def check_heap(cities):
    heap = MinHeap()
    for c in cities:
        heap.push(c.distance, c)
    popped = []
    while not heap.is_empty():
        priority, value = heap.pop()
        popped.append(priority)
    assert popped == sorted(c.distance for c in cities)
    print("  MinHeap pops in ascending distance order: OK")


def check_hash_table(cities):
    ht = HashTableChaining()
    for c in cities:
        ht.insert(c.name + "|" + c.country, c)

    unique_keys = {c.name + "|" + c.country for c in cities}
    assert len(ht) == len(unique_keys)

    probe = cities[len(cities) // 3]
    found = ht.search(probe.name + "|" + probe.country)
    assert found is probe

    assert ht.delete(probe.name + "|" + probe.country)
    assert ht.search(probe.name + "|" + probe.country) is None
    print(f"  HashTable load_factor={ht.load_factor():.2f}, "
          f"max_chain_length={ht.max_chain_length()} -- OK")


if __name__ == "__main__":
    all_cities = load_cities()
    sample = sample_cities(all_cities, 2000)

    print("Testing BST/AVL...")
    check_bst_avl(sample)
    print("Testing MinHeap...")
    check_heap(sample)
    print("Testing HashTable...")
    check_hash_table(sample)
    print("\nAll structural correctness checks passed.")
