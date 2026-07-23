import os


def matrix_chain_order(p):
   
    n = len(p) - 1  # number of matrices
    if n < 1:
        return None, None, 0

    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for chain_len in range(2, n + 1):
        for i in range(1, n - chain_len + 2):
            j = i + chain_len - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s, m[1][n]


def print_optimal_parens(s, i, j):
    """Reconstructs the optimal parenthesisation from the split table."""
    if i == j:
        return f"A{i}"
    k = s[i][j]
    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)
    return f"({left} x {right})"


if __name__ == "__main__":
    # Worked example: 4 matrices A1..A4 with dimensions
    # A1: 10x30, A2: 30x5, A3: 5x60, A4: 60x10
    p = [10, 30, 5, 60, 10]
    m, s, cost = matrix_chain_order(p)

    n = len(p) - 1
    print("DP cost table m[i][j] (minimum scalar multiplications for A_i..A_j):")
    header = "      " + "".join(f"A{j:<8}" for j in range(1, n + 1))
    print(header)
    for i in range(1, n + 1):
        row = f"A{i:<4}"
        for j in range(1, n + 1):
            row += f"{m[i][j] if j >= i else '-':<9}"
        print(row)

    print(f"\nMinimum number of scalar multiplications: {cost}")
    print(f"Optimal parenthesisation: {print_optimal_parens(s, 1, n)}")
