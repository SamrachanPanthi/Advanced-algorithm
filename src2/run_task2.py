
import os, sys, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))

STEPS = [
    ("Correctness checks", "test_algorithms.py"),
    ("Dijkstra/Prim step-by-step visualisations", "make_algorithm_plots.py"),
    ("Empirical benchmark (~30-60 seconds)", "benchmark_graphs.py"),
    ("Generating comparison graphs", "make_benchmark_plots.py"),
]

def main():
    for description, script in STEPS:
        print("\n" + "=" * 70)
        print(f"STEP: {description}  ({script})")
        print("=" * 70)
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            print(f"\n*** {script} failed (see error above) -- stopping. ***")
            sys.exit(1)
    print("\n" + "=" * 70)
    print("ALL TASK 2 STEPS COMPLETE")
    print("=" * 70)
    print("Results:  ../results2/graph_benchmark_results.csv")
    print("Graphs:   ../results2/plots/")

if __name__ == "__main__":
    main()
