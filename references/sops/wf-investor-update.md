# wf-investor-update (example workflow)

Goal: a complete, on-brand recurring stakeholder/investor update **draft**, every figure traced to a source, ready ahead of the send date.
Success criteria: HTML draft rendered; every number has a source; no secrets/confidential leak (lint passes); ready before the deadline.
Trigger: a few days before the recurring send date *(phase 2 — `/schedule`; until then, on demand)*.
Autonomy: **draft-then-approve** — it's external, so the workflow stops at the draft; **you send** (guardrail #3).
Owner: you prepare; your finance owner supplies figures.

## Steps
1. **Pull live figures** — CRM pipeline + finance model.  `MCP / export`
   → gate: all required metrics present?
   → branch: **figure missing or stale → flag + ask the finance owner, do NOT guess** (cite-don't-invent).
2. **Structure the narrative** — `/structure` → highlights, variance story, updates, targets.
   → gate: every claim maps to a pulled figure or cited source.
3. **Assemble content JSON** (sections, KPI cards, tables with variance tones). Write to `.tmp/`.
4. **Render** — `tools/render_brand_html.py --content .tmp/report.json --out .tmp/report.html`.
5. **Quality gate** — scan the draft: every number sourced? no secrets/confidential leak?
   → branch: **leak or unsourced number → stop, fix, re-gate.**
6. **Deliver as a draft** to you for review → you send. **Never auto-send. Figures never committed to git** (guardrail #2).

## Guardrails
#2 no confidential figures in git · #3 draft-never-send external · #6 cite-don't-invent · leakage gate before "done".
