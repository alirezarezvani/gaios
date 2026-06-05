# references/sops/ — Workflows (SOPs)

The WAT "Workflows" layer for anything heavier than a quick `/skill`. Each SOP is a plain-language briefing: what the objective is, what inputs are needed, which **tools** to call (a `tools/*.py` script or an MCP), the expected output, and how to handle edge cases.

## When a workflow belongs here vs. as a skill
- **Skill** (`.claude/skills/*`) — a quick, conversational entry point you invoke with `/name`.
- **SOP** (here) — a multi-step, repeatable procedure with defined inputs/outputs that calls tools. Skills can point to an SOP for the detail.

## Template
```
# <Workflow name>
Objective: <one line>
Trigger: <when this runs>
Inputs: <what's required, and where it comes from>
Tools: <tools/xyz.py | MCP name> — <what each does>
Steps: <ordered, plain language>
Output: <what's produced, and where it lands (your sanctioned cloud / .tmp)>
Edge cases & learnings: <append as you discover them — do not overwrite without asking>
Guardrails: <the CLAUDE.md rules that apply>
```

## Inventory
| SOP | Serves | Tool |
|---|---|---|
| `render-branded-doc.md` | Produce any on-brand HTML (handoff doc, report, investor update) | `tools/render_brand_html.py` |
| `wiki-translate.md` | Turn `raw/` captures into clean `wiki/` knowledge (the second-brain loop) | `tools/wiki_lint.py` |
| `experiment-loop.md` | Autoresearch-style hill-climb: try → measure → keep/revert → log (with autonomy gate) | `tools/experiment_log.py` |
| `dynamic-workflows.md` | The pattern: goal-driven, composable, self-verifying workflows (+ card format, autonomy/cadence gate, phasing) | — (guide) |
| `wf-investor-update.md` | Monthly investor draft — pull figures → structure → render → cite-gate → approve | `render_brand_html.py` + MCPs |
| `wf-daily-triage.md` | Morning brief across Outlook/Teams/Jira/calendar with routing | MCPs + `/structure` |
| `wire-connections.md` | Checklist to wire the easy-4 MCPs (the parallel track; interactive auth) | — (guide) |
