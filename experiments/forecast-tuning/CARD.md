# Forecast tuning (runnable reference)

Objective: lower the backtest error of a monthly forecast.
Metric: **MAPE %** (lower is better) — computed by `harness.py` on a held-out 12-month test split.
Mutable surface: **`model.py`** (the `forecast()` function). `harness.py` is read-only ground truth.
Budget per iteration: one `python run.py` (instant on synthetic data).
Autonomy: **autonomous** — objective metric + reversible (git) + synthetic data, no sensitive data.
Sandbox: branch `experiments/<tag>`; `results.tsv` git-ignored.
Owner: {{whoever reviews winners}}.
Guardrails: synthetic data here. For a **real** version, point `harness.py` at your own history → results become confidential, so keep `results.tsv` git-ignored and never external.
Baseline: naive last-value forecast.

## Run
```bash
python tools/experiment_log.py init experiments/forecast-tuning/results.tsv
python experiments/forecast-tuning/run.py                 # prints: mape: <value>
python tools/experiment_log.py add experiments/forecast-tuning/results.tsv \
  --id baseline --metric <value> --status keep --note "naive last-value"
```
Then edit `model.py`, re-run, log, and keep (commit) if MAPE dropped — else revert. See `references/sops/experiment-loop.md`.

The shipped `model.py` is the **baseline** on purpose — room for the loop to climb (e.g. seasonal-naive + trend, damped trend, robust seasonal averaging).
