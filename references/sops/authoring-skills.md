# SOP: Authoring & expanding gAIOS workflows (skills)

**Objective:** add a new workflow to gAIOS consistently, so the library can grow without drift —
and work in **both** Claude Code and Codex with no extra wiring.

**When to use:** a manual task recurs 3+ times (surfaced by `/level-up`), or a Chief-of-Staff
capability is missing. Reuse first — check `.claude/skills/*` and `references/sops/` before building.

---

## Skill vs SOP — which to write
- **Skill** (`.claude/skills/<name>/SKILL.md`) — a quick, invocable entry point (`/<name>`). Most
  workflows are skills.
- **SOP** (`references/sops/<name>.md`) — a heavier, multi-step procedure a skill *references* when
  the steps are long or shared across skills (like this file).

## Skill anatomy (the standard — every skill follows it)
Frontmatter (required — this exact shape is what both Claude Code *and* Codex read):
```
---
name: <kebab-case>
description: Use when <trigger situation>. <one line on what it produces>. Trigger on "/<name>", "<phrase>", "<phrase>".
---
```
The `description` is the *router* — load it with concrete trigger phrases, or the skill won't fire.

Body sections (match the house style in `.claude/skills/structure/SKILL.md`):
1. **# Title + one-line purpose**
2. **## When to run** — the situations that should trigger it.
3. **## The output (always this shape)** — a fenced template of the deliverable. Determinism in the *output contract* is what makes a skill reliable.
4. **## Process** — numbered steps: which **tools** to call (scripts in `tools/` or MCPs in `connections.md`), in what order, with a **gate/verify** per step.
5. **## Autonomy** — the default level (see below). Default to the **lowest that works**.
6. **## Guardrails (from CLAUDE.md)** — the hard rules this skill must honor.

## WAT discipline (probabilistic reasons, deterministic executes)
- Push anything repeatable/checkable into a **tool** (`tools/*.py`) — chained 90%-accurate LLM steps decay fast; boring code doesn't.
- **Reuse before building.** Compose existing skills/tools.
- **Self-improvement loop:** on failure → read error → fix the tool → verify → update this/the SOP. Log notable changes to `decisions/log.md`.

## Autonomy spectrum (from the 3Ms — default to the lowest that works)
`L0` manual · `L1` AI suggests, human decides · `L2` AI drafts, human reviews · `L3` rules set, AI runs, human validates · `L4` autonomous. **New skills default to L2** (draft-not-send). Raise per skill only once trusted.

## Composability (Lego)
Build small, single-purpose skills. Let `/workflow` orchestrate them and `/structure` feed them. A
good skill does one job and names the others it hands off to (e.g. `/triage` → `/structure` per item).

## Cross-runtime (free, by design)
Because `.codex/skills` is a symlink to `.claude/skills`, **any skill you add here appears in Codex
automatically** — same `SKILL.md` (`name` + `description`) format. Don't author twice. Keep heavier
logic in `references/sops/` (plain markdown any agent can read).

## Quality bar (ship-ready checklist)
- [ ] Frontmatter `description` has ≥3 concrete trigger phrases.
- [ ] Output section shows the exact deliverable shape.
- [ ] Each step names the tool/skill it calls and a verify-check.
- [ ] Autonomy level stated; defaults to draft-not-send for anything external.
- [ ] Guardrails section references the relevant `CLAUDE.md` rules.
- [ ] A **verification scenario** (how to know it works) + ideally a sample output in `examples/`.
- [ ] Added to: `CLAUDE.md` "Your skills", `README.md` features + structure map, and `AGENTS.md` skills table.
- [ ] If it needs determinism, a `tools/<name>.py` exists and is referenced.
