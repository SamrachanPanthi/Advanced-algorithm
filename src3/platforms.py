
def min_platforms(arrivals, departures):
    arr = sorted(arrivals)
    dep = sorted(departures)

    n = len(arr)
    i, j = 0, 0
    in_use = 0
    max_platforms = 0

    while i < n and j < n:
        if arr[i] <= dep[j]:
            in_use += 1
            max_platforms = max(max_platforms, in_use)
            i += 1
        else:
            # A departure happens first -> a platform is freed.
            in_use -= 1
            j += 1

    return max_platforms


def min_platforms_brute_force(arrivals, departures):
    n = len(arrivals)
    best = 0
    for i in range(n):
        t = arrivals[i]
        overlap = sum(1 for j in range(n) if arrivals[j] <= t <= departures[j])
        best = max(best, overlap)
    return best


if __name__ == "__main__":
    # Worked example (times as minutes past midnight for simplicity)
    arrivals = [900, 940, 950, 1100, 1150, 1500]
    departures = [910, 1200, 1120, 1130, 1200, 1900]

    greedy_result = min_platforms(arrivals, departures)
    exact_result = min_platforms_brute_force(arrivals, departures)

    print(f"Arrivals:   {arrivals}")
    print(f"Departures: {departures}")
    print(f"Greedy minimum platforms:      {greedy_result}")
    print(f"Brute-force minimum platforms: {exact_result}")
    print("Match:", greedy_result == exact_result)
