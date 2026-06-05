# gAIOS — a generic AI Operating System blueprint

Clone this folder, run `/setup`, and turn Claude Code into **your** personal AI Operating System — a second brain + Chief of Staff that holds your context, structures your work, drafts in your voice, and runs reliable workflows.

It's the open, customizable skeleton: **fork it for any role, company, or domain.** Nothing here is tied to one business.

---

## Quick start
1. **Clone** this folder to your machine.
2. **Open it in Claude Code** and run **`/setup`**.
3. Answer the guided interview (identity, voice, priorities, stack, team, guardrails). It fills `CLAUDE.md`, `context/`, `references/voice.md`, and `connections.md`.
4. Try the first prompt: *"what should I focus on this week?"*

---

## What's inside (the architecture)

**The Four Cs** — Context (knows your business) · Connections (reaches your stuff) · Capabilities (knows how to do the work) · Cadence (runs without being asked).

**The Three Ms** — Mindset · Method · Machine (`references/3ms-framework.md`). *Both frameworks © Nate Herk — see `NOTICE`.*

**WAT — Workflows · Agents · Tools.** Probabilistic AI reasons; deterministic code executes. Boring, testable, auditable.

**Features (all included):**
- `/structure` — turn any fuzzy input into a clear brief.
- `/wiki` — a second brain: drop notes in `raw/`, get clean cross-linked knowledge in `wiki/` (with a leakage-scanning lint gate).
- `/workflow` — **dynamic workflows**: goal-driven, composable, self-verifying pipelines with a quality gate per step.
- `/experiment` — an **autoresearch** loop (try → measure → keep/revert → log), with a runnable forecast example.
- `/exec-cockpit` — a leadership-transition / exec-cockpit template.
- `tools/` — deterministic Python (branded-HTML renderer, wiki lint, experiment log).
- **Operating discipline** baked into `CLAUDE.md` (think-before-acting, simplicity, surgical changes, goal-driven, verify-before-done).
- A **brand kit** template (`brand-assets/`) so outputs render on-brand.

---

## Structure
```
CLAUDE.md            ← the operating manual (filled by /setup)
context/             ← about you, the business, the team, priorities
wiki/  · raw/        ← second brain (wiki committed; raw git-ignored)
projects/            ← active workstreams
experiments/         ← autoresearch harness (+ runnable forecast example)
tools/               ← deterministic Python (WAT execution layer)
references/sops/     ← workflows / SOPs (incl. dynamic-workflows + examples)
references/          ← 3ms framework, voice, API guides
brand-assets/        ← CI/CD template (tokens + preview)
connections.md       ← registry of systems the AIOS can reach
decisions/log.md     ← append-only decision record
.claude/skills/      ← /setup, /structure, /wiki, /workflow, /experiment, /exec-cockpit, /onboard, /audit, /level-up
```

See `EXPANSIONS.md` for what to add as you grow.

---

## Customize for your domain
The `Guardrails` block in `CLAUDE.md` ships with safe defaults. **Set your sensitive-data line and compliance rules** (GDPR / HIPAA / SOC2 / medical-device / …) during `/setup` — don't run the generic defaults unchanged for a regulated business.

## License & attribution
gAIOS is **© 2026 Alireza Rezvani**, MIT-licensed (see `LICENSE`). It builds on Nate Herk's MIT-licensed AIS-OS starter kit; the Three Ms / Four Cs frameworks and the base structure remain © Nate Herk and are credited as the source (see `NOTICE`). The added layers — WAT integration, second-brain wiki, autoresearch harness, dynamic workflows, Operating discipline, the tools — are Alireza Rezvani's work. Preserve the framework attribution; don't repackage the frameworks as anyone's own.
