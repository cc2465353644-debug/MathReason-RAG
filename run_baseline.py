# run_baseline.py

import subprocess

print("Running baseline solver...")
subprocess.run(["python", "-m", "src.baseline_solver"], check=True)

print("Running evaluator...")
subprocess.run(["python", "-m", "src.evaluator"], check=True)

print("Baseline pipeline finished.")
