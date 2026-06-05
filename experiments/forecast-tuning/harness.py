"""
harness.py — READ-ONLY eval (the ground truth). Do not let the agent edit this to game the metric.

Generates a deterministic synthetic monthly series (trend + seasonality + small noise),
holds out the last 12 months, and scores a forecast function by MAPE. Synthetic so the
blueprint runs anywhere with zero data setup. For the real finance version, replace make_series()
with the finance model's history (and keep results.tsv git-ignored — it's confidential).
"""
import math
import random

N_TOTAL = 36          # months
TEST_HORIZON = 12     # held-out months
BASE, TREND, AMP = 100.0, 2.0, 15.0


def make_series():
    random.seed(42)  # deterministic
    series = []
    for t in range(N_TOTAL):
        seasonal = AMP * math.sin(2 * math.pi * (t % 12) / 12)
        noise = random.uniform(-2.0, 2.0)
        series.append(BASE + TREND * t + seasonal + noise)
    return series


def load():
    s = make_series()
    return s[:-TEST_HORIZON], s[-TEST_HORIZON:]  # train, test


def mape(actual, pred):
    return sum(abs((a - p) / a) for a, p in zip(actual, pred)) / len(actual) * 100.0


def evaluate(forecast_fn):
    """forecast_fn(history: list[float], horizon: int) -> list[float].  Returns MAPE % (lower better)."""
    train, test = load()
    pred = forecast_fn(list(train), len(test))
    if len(pred) != len(test):
        raise ValueError(f"forecast returned {len(pred)} points, expected {len(test)}")
    return mape(test, pred)
