# Dynamic workflows (goal-driven · composable · self-verifying)

A **dynamic workflow** upgrades a static SOP. It starts from a **goal + success criteria**, **plans and routes at runtime**, **composes** existing skills/tools/MCPs, **gates quality** at each step, **verifies** before "done", and **fails safe**. Run them via `/workflow`. This is the WAT "Workflow" layer leveled up — the engine for speed, quality, and fewer errors.

## When to build one (don't workflow-ify everything)
A workflow earns its place only when the task is **recurring · multi-step · composes ≥2 capabilities · has a definable "done."** One-offs and judgment calls use a skill or direct work. Over-workflowing adds complexity for no gain (Simplicity — see `CLAUDE.md` Operating discipline).

## The five upgrades over a static SOP
1. **Goal + success criteria** — define "done" as a check, not a vibe. *(goal-driven)*
2. **Runtime plan + route** — decompose the goal, pick the right skill/tool/MCP, **branch on conditions**. *(adapts to input)*
3. **Compose** — chain existing skills/tools as Lego; don't rebuild. *(efficiency)*
4. **Quality gate per step + a final verify** — lint, cite-check, completeness, brand-render. *(quality, fewer errors)*
5. **Fail-safe + optional trigger** — on error retry/repair/escalate, never silently fail; run on a schedule/event where safe. *(speed, less time)*

## Card format
```md
# <workflow name>
Goal: <end state>
Success criteria: <the check that means "done">
Trigger: <on demand | schedule/event>            (phase 2)
Autonomy: <auto | draft-then-approve | human-in-loop>   (per the gate below)
Steps:
  1. <action: /skill | tool | MCP>  → gate/verify: <check>   → branch: <condition → path>
  2. ...
Output: <artifact + where it lands (your sanctioned cloud / draft to the user)>
Guardrails: <which CLAUDE.md rules apply>
```

## Autonomy & cadence gate (reuse the rules — don't invent a new axis)
A workflow may run **on a trigger, unsupervised** only if it passes the gate: **objective + reversible + internal, no PHI, no external send.** Any **external / irreversible / regulated** step **stops for approval** (draft-never-send; never to a sensitive recipient without approval). Scale caution to stakes (CLAUDE.md). The gate is decided per-step, not per-workflow.

## Phasing 
- **Phase 1 — now:** the pattern + composed workflows, run **on demand** via `/workflow`. Tool-backed steps already work (e.g. `render_brand_html`, `wiki_lint`); data-pull steps are **wire-and-go** once connections are live.
- **Phase 2 — after connections are wired:** add **triggers/cadence** (`/schedule` or hooks) to the safe (internal, gated) workflows so outputs land before you ask.
- **Phase 3 — big one-offs:** **parallel multi-agent** orchestration for full audits, reviews, and deep research (opt-in, heavier).

## Engine tiers
- **Lightweight (default):** `/workflow` runs skills + tools + MCPs in sequence with gates and branches. Most daily work.
- **Heavy (opt-in):** fan-out across many agents at once for comprehensiveness (audits/reviews/research). More tokens — needs an explicit go.

## Inventory: `references/sops/wf-*.md`
| Workflow | Goal | Composes | Autonomy |
|---|---|---|---|
| `wf-investor-update.md` | Monthly investor draft, every figure cited, on-brand | CRM / finance MCP · `/structure` · `render_brand_html` · cite-gate | draft-then-approve (external) |
| `wf-daily-triage.md` | A morning brief: what's urgent, what's waiting on you | email / tasks MCP · `/structure` | auto (internal) + draft for any external |
