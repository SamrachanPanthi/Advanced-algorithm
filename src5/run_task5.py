"""
run_task5.py — click Run (or run `python run_task5.py`) to execute the
entire Task 5 pipeline: correctness/race-condition tests, the concurrency
benchmark, and plot generation, in order.
"""
import os, sys, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))

STEPS = [
    ("Correctness and race-condition stress tests", "test_concurrency.py"),
    ("Concurrency benchmark (~10-20 seconds)", "benchmark_concurrency.py"),
    ("Generating speedup/scalability graphs", "make_concurrency_plots.py"),
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
    print("ALL TASK 5 STEPS COMPLETE")
    print("=" * 70)
    print("Results:  ../results5/*.csv")
    print("Graphs:   ../results5/plots/")

if __name__ == "__main__":
    main()
