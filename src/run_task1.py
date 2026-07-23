
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

STEPS = [
    ("Correctness checks", "test_structures.py"),
    ("Empirical benchmark (this takes ~10-20 seconds)", "benchmark.py"),
    ("Generating graphs", "make_plots.py"),
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
    print("ALL TASK 1 STEPS COMPLETE")
    print("=" * 70)
    print("Results:  ../results/benchmark_results.csv")
    print("Graphs:   ../results/plots/  (5 PNG files)")
    print("Charts should also have popped up on screen as they were made.")


if __name__ == "__main__":
    main()
