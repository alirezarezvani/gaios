# Experiment loop (autoresearch pattern)

**Objective:** Improve a measurable artifact by hill-climbing — try a change, measure against one objective metric, keep if better, revert if not, log the trail. Adapted from Karpathy's `autoresearch`; generalized and guardrailed.

**Trigger:** `/experiment`, "run an experiment loop on X", "autoresearch X".

**Tools:** `tools/experiment_log.py` (the results trail). The experiment's own eval harness computes the metric.

---

## The autonomy gate (check BEFORE looping — this is the safety line)

**Autonomous looping (run many iterations unsupervised) is allowed ONLY if ALL hold:**
1. **Objective, cheap, automatable metric** — computed by code in seconds-to-minutes (e.g. MAPE, AUC, latency). Not "is this good?".
2. **Reversible sandbox** — a git branch / throwaway dataset / `.tmp`. Reverting a bad change is free.
3. **No PHI, no confidential data in the loop; no external send; no production deploy.**

If **any** fails → **human-in-the-loop:** the agent proposes each change, the human approves, no overnight run. (This is the *scale-caution-to-stakes* rule from `CLAUDE.md` — produce on reversible/internal, stop-and-confirm on irreversible/regulated.)

Regulated or production outcomes are **never auto-deployed** — the winning experiment feeds the **human-reviewed, regulated** change process.

---

## Read-only vs mutable (don't let the agent game the metric)
- **Eval harness = read-only ground truth** (like autoresearch's `prepare.py`). The agent never edits the metric/eval.
- **Mutable surface = ONE file/area** the agent changes (like `train.py`). Keeps diffs reviewable.

## The loop
1. **Branch:** `git checkout -b experiments/<tag>` (isolated; never on `main`).
2. **Define** (in the experiment's `CARD.md`): metric + direction (min/max), the one mutable surface, a **fixed budget per iteration**, and the baseline.
3. **Baseline first:** run the harness unmodified, log it (`experiment_log.py add ... --status keep --note baseline`).
4. **LOOP:**
   a. Change the mutable surface with one idea.
   b. Run the eval harness → read the metric (redirect output to a log; grep the metric line).
   c. `experiment_log.py add` the result.
   d. **Keep or revert:** improved → keep/commit (advance). Equal-or-worse → `git reset` back. *Simpler-and-equal = keep* (simplicity criterion).
5. **Stop:** human interrupt; or (autonomous) a set iteration/wall-clock budget. Crashes → fix if trivial, else log `crash` and skip.
6. **Hand off the winner + the trail** for human review. Don't ship regulated/production changes from the loop.

## Output / logging
`results.tsv` (`id  metric  status  note`) via `tools/experiment_log.py`. **Run artifacts (results.tsv, run.log, data/) are git-ignored** — metrics on real runs may be confidential; the *blueprint* (harness, mutable surface, CARD) is tracked.

## Per-experiment layout
```
experiments/<name>/
  CARD.md      — the spec: objective, metric(+direction), mutable surface, budget, autonomy, owner, guardrails
  harness.py   — read-only eval (computes the metric)        [the ground truth]
  <surface>    — the one file the agent edits                [e.g. model.py]
  run.py       — glue: run surface through harness, print metric
  results.tsv  — the trail (git-ignored)
```
See `experiments/forecast-tuning/` for a runnable reference, and `experiments/README.md` for the use-case cards.
