# gAIOS — your personal AI Operating System

Clone it, run `/setup`, and it becomes **yours** in **Claude Code or Codex** — a second brain + Chief of Staff that holds your context, structures your work, drafts in your voice, and runs reliable workflows.

Open-source and opinionated — complete out of the box, not a blank slate. **Fork it and make it yours for any role, company, or domain.**

---

## Quick start
1. **Clone** this folder to your machine.
2. **Open it in Claude Code or Codex** and run **`/setup`** (in Codex: invoke the `setup` skill or just ask it to "run setup").
3. Answer the guided interview (identity, voice, priorities, stack, team, guardrails). It fills `CLAUDE.md`, `context/`, `references/voice.md`, and `connections.md`.
4. Try the first prompt: *"what should I focus on this week?"*

> Runtime compatibility (Claude Code · Codex · others) is summarized in [Compatibility](#compatibility) below.

---

## What's inside (the architecture)

**The Four Cs** — Context (knows your business) · Connections (reaches your stuff) · Capabilities (knows how to do the work) · Cadence (runs without being asked).

**The Three Ms** — Mindset · Method · Machine (`references/3ms-framework.md`). *Both frameworks inspired by Nate Herk's work — see `NOTICE`.*

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
AGENTS.md            ← Codex / cross-tool runtime bootstrap (mirrors CLAUDE.md's rules)
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
.codex/skills/       ← symlink → .claude/skills (so Codex discovers the same skills)
```

See `EXPANSIONS.md` for what to add as you grow.

---

## Customize for your domain
The `Guardrails` block in `CLAUDE.md` ships with safe defaults. **Set your sensitive-data line and compliance rules** (GDPR / HIPAA / SOC2 / medical-device / …) during `/setup` — don't run the defaults unchanged for a regulated business.

## Compatibility

gAIOS runs on any agentic coding tool that reads a project-instructions file. **Claude Code is first-class; Codex / Codex CLI is supported** via `AGENTS.md`.

| Runtime | Reads | gAIOS workflows (skills) | Status |
|---------|-------|--------------------------|--------|
| **Claude Code** | `CLAUDE.md` | Native slash skills (`/setup`, `/structure`, …) in `.claude/skills/` | ✅ First-class |
| **Codex / Codex CLI** | `AGENTS.md` → points it to `CLAUDE.md` + `context/` | Auto-discovered from `.codex/skills` (symlink → `.claude/skills`), or invoke by name | ✅ Supported |
| **Other agents** (Cursor, Gemini CLI, Copilot, …) | `AGENTS.md` / `CLAUDE.md` | Ask for a workflow by name; the agent reads the matching `.claude/skills/*/SKILL.md` or `references/sops/` | ⚠️ Works via instructions |

**Using gAIOS in Codex:** open the repo in Codex CLI — it loads `AGENTS.md` automatically, which directs it to `CLAUDE.md` and `context/` and restates the hard guardrails. Project skills load from `.codex/skills` (a symlink to `.claude/skills`); on Windows without symlink support, the agent reads `.claude/skills/` directly as instructed in `AGENTS.md`. Configure MCP servers in `~/.codex/config.toml` and keep secrets in `.env`. Details: [`AGENTS.md`](AGENTS.md).

> One source of truth: `CLAUDE.md` holds the canonical, `/setup`-filled content; `AGENTS.md` mirrors its rules for other runtimes and defers to it on any conflict.

## License & attribution
gAIOS is **© 2026 Alireza Rezvani**, MIT-licensed (see `LICENSE`). It is inspired by Nate Herk's AIS-OS starter kit and his Three Ms / Four Cs frameworks, which are credited as inspiration (see `NOTICE`); those framework names are Nate Herk's trademarks. Everything in this repo — the WAT integration, second-brain wiki, autoresearch harness, dynamic workflows, Operating discipline, and the tools — is Alireza Rezvani's work. Please keep the inspiration credit to Nate Herk.
