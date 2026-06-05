"""
run.py — glue. Runs the mutable surface (model.forecast) through the read-only harness
and prints the metric in a grep-able line:  `mape: <value>`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run from anywhere
import harness  # noqa: E402
import model    # noqa: E402

score = harness.evaluate(model.forecast)
print(f"mape: {score:.6f}")
