"""
model.py — THE MUTABLE SURFACE. This is the one file the agent edits to lower MAPE.
Everything is fair game inside forecast(); just keep the signature and return `horizon` points.
"""


def forecast(history, horizon):
    """Baseline: naive — repeat the last observed value."""
    return [history[-1]] * horizon
