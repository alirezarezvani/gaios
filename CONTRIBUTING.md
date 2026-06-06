# Contributing to gAIOS

gAIOS runs an **automated, AI-orchestrated CI/CD pipeline**. You open a PR; Claude reviews it,
deterministic gates run, and it merges itself when everything is green. Humans stay in the loop
only where it matters: a manual stop button, and a deliberate signal for production.

## Branching strategy

```
feature/* · fix/* · hotfix/*  ──PR──▶  dev  ──PR──▶  main
                              (auto-merge      (auto-merge ONLY
                               when green)      with ship-it)
```

- **`main`** — protected release branch, always deployable. **Never committed directly.** PRs into
  `main` may come **only from `dev`** (or `hotfix/*`), and merge only with the `ship-it` signal.
- **`dev`** — integration branch and the **default** for PRs. Everyday work lands here first.
- **`feature/*` · `fix/*` · `hotfix/*`** — short-lived branches. Branch from `dev` (from `main` for
  a `hotfix/*`); open a PR back into `dev`.

### Day-to-day flow

```bash
git checkout dev && git pull
git checkout -b feat/short-description
# ...work...
git push -u origin feat/short-description
gh pr create --base dev --title "feat: short description"   # title = Conventional Commit
```

That's it. **Don't merge manually** — once the checks pass, the PR auto-merges (squash) and the
branch is auto-deleted. To release, open `dev → main` and apply **`ship-it`** (or comment
**`@claude ship`**).

## How review & merge are automated (the WAT split)

Probabilistic AI **reasons**; deterministic code **executes**.

1. **`ai-review`** — Claude reviews every PR (correctness, security, guardrail compliance) and
   emits an `APPROVE` / `REQUEST_CHANGES` verdict. This is a **required check** and **replaces
   manual human approval**. Fail-closed: no clear approval → no merge.
2. **Deterministic gates** run in parallel and are **never bypassed**.
3. **Auto-merge** merges the PR the moment all required checks are green.

### Manual controls (humans still in the loop)
- **Stop a merge:** add the **`hold`** (or `do-not-merge`) label, or keep the PR a **draft**.
- **Ship to production:** `dev → main` needs the **`ship-it`** label or a **`@claude ship`**
  comment from the owner (enforced by the `release-gate` check). Everything else is hands-off.

## Required checks (gates)

| Check | What it does |
|-------|--------------|
| `ai-review` | Claude's review verdict — the merge gate (replaces human approval) |
| `commit-lint` | PR title must be a Conventional Commit |
| `lint` | `py_compile` + `ruff` (real-error subset) on Python |
| `wiki-lint` | `tools/wiki_lint.py` — broken links + leakage scan (no secrets/IBAN/PHI in `wiki/`) |
| `secret-scan` | Gitleaks — no secrets anywhere in the repo |
| `bandit` | Python security scan (fails on medium+ severity) |
| `guard` | (into `main` only) rejects sources other than `dev`/`hotfix/*` |
| `release-gate` | (into `main` only) requires the `ship-it` signal |

## Commit messages (Conventional Commits)

Auto-merge **squashes**, and the repo is set so the **PR title becomes the commit message** — so
keep titles clean and professional:

```
<type>: <imperative, lowercase summary>     e.g.  feat: add daily brief skill
```

Types: `feat` · `fix` · `docs` · `chore` · `ci` · `refactor` · `test` · `perf` · `build` · `revert`.
Put detail (and `Closes #<n>`) in the PR body — it becomes the commit body.

## Issues

Open issues with the templates (bug / feature / task). New issues are **auto-triaged** by Claude
(labels + a first-pass assessment). Link work with **`Closes #<n>`** in the PR body so the issue
closes on merge. Tag **`@claude`** in any issue/PR comment to ask for help.

## Rules

1. **No secrets, confidential figures, or PHI/PII** in the repo — ever. Keys live in `.env` (git-ignored).
2. **No direct pushes** to `main`/`dev` — everything goes through a PR.
3. Keep changes **surgical**; update `CLAUDE.md`/docs when behavior or structure changes.
4. New skills follow `references/sops/authoring-skills.md`.

## Maintainers & autonomy

The repository owner is the admin (can bypass in emergencies). Production (`dev → main`) keeps a
deliberate human checkpoint (`ship-it`) by design — the Bike Method. Dial it up (full auto) or
down (human-approved) by editing the branch-protection required checks and `auto-merge.yml`.
