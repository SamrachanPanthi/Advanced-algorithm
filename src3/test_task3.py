from matrix_chain import matrix_chain_order
from platforms import min_platforms, min_platforms_brute_force
from hamiltonian import Graph, hamiltonian_cycle


def test_matrix_chain():
    # Classic textbook example: p = [30, 35, 15, 5, 10, 20, 25], 6 matrices,
    # known optimal cost is 15125.
    p = [30, 35, 15, 5, 10, 20, 25]
    _, _, cost = matrix_chain_order(p)
    assert cost == 15125, f"expected 15125, got {cost}"

    # A single matrix needs no multiplications at all.
    _, _, cost_single = matrix_chain_order([10, 20])
    assert cost_single == 0

    # Two matrices: cost is just the one multiplication p0*p1*p2.
    _, _, cost_two = matrix_chain_order([10, 20, 30])
    assert cost_two == 10 * 20 * 30

    print("Matrix Chain Multiplication: OK")


def test_platforms():
    arrivals = [900, 940, 950, 1100, 1150, 1500]
    departures = [910, 1200, 1120, 1130, 1200, 1900]
    greedy = min_platforms(arrivals, departures)
    exact = min_platforms_brute_force(arrivals, departures)
    assert greedy == exact, f"greedy {greedy} != brute force {exact}"

    # No overlap at all -> only ever 1 platform needed.
    assert min_platforms([100, 200, 300], [150, 250, 350]) == 1

    # All trains present together -> needs one platform per train.
    assert min_platforms([100, 100, 100], [200, 200, 200]) == 3

    print("Minimum Number of Platforms: OK")


def test_hamiltonian():
    # Ring + shortcut: has a Hamiltonian cycle.
    g1 = Graph(5)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]:
        g1.add_edge(u, v)
    result1 = hamiltonian_cycle(g1)
    assert result1 is not None
    # Every vertex appears exactly once (ignoring the repeated start/end).
    assert sorted(result1[:-1]) == list(range(5))
    assert result1[0] == result1[-1]

    # Star graph: no Hamiltonian cycle can exist.
    g2 = Graph(5)
    for leaf in [1, 2, 3, 4]:
        g2.add_edge(0, leaf)
    assert hamiltonian_cycle(g2) is None

    # Complete graph K4: always has a Hamiltonian cycle.
    g3 = Graph(4)
    for i in range(4):
        for j in range(i + 1, 4):
            g3.add_edge(i, j)
    result3 = hamiltonian_cycle(g3)
    assert result3 is not None

    print("Hamiltonian Cycle: OK")


if __name__ == "__main__":
    test_matrix_chain()
    test_platforms()
    test_hamiltonian()
    print("\nAll Task 3 correctness checks passed.")
