# experiments/ — autoresearch harness

Hill-climb a measurable artifact: **try a change → measure one objective metric → keep if better, revert if not → log the trail.** Adapted from Karpathy's [autoresearch](https://github.com/karpathy/autoresearch), generalized and guardrailed. Procedure: `references/sops/experiment-loop.md`. Entry point: `/experiment`.

> The *engine* (`tools/experiment_log.py`, the SOP, this pattern) is **domain-agnostic**. The `forecast-tuning` example is fully runnable with stdlib + synthetic data — it works out of the box.

## The autonomy gate (non-negotiable)
Unsupervised looping needs **all three**: ① objective, cheap, automatable metric · ② reversible sandbox (branch / throwaway data / `.tmp`) · ③ no sensitive/confidential data, no external send, no prod deploy. If any fails → human-in-the-loop. Regulated/production winners feed a human-reviewed change process — never auto-deploy.

## Anatomy
```
experiments/<name>/
  CARD.md      — spec (objective · metric+direction · mutable surface · budget · autonomy · owner · guardrails)
  harness.py   — read-only eval that computes the metric   (ground truth — never edited)
  <surface>    — the ONE file the agent edits              (e.g. model.py)
  run.py       — glue: run surface through harness, print metric
  results.tsv  — the trail (git-ignored)
```

## Where it fits (examples)
| Use case | Metric | Fit | Autonomy |
|---|---|---|---|
| **Model / ML tuning** | accuracy/AUC on a held-out set | strong | autonomous in sandbox; winners → human review |
| **Inference cost / latency** | p95 latency + accuracy guard | strong | autonomous in a branch |
| **Forecast / numeric model** | backtest error (MAPE) | strong | **`forecast-tuning/` runnable here** |
| **Copy / landing A/B** | conversion rate | medium | human-in-the-loop (slow eval) |
| **Prompt / skill / SOP tuning** | rubric score (human-rated) | medium | human-in-the-loop |

Tasks with **no cheap objective metric** (most strategy/comms/regulatory work) are a **poor fit** — don't autoresearch those.
