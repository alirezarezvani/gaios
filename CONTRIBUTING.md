# Contributing to gAIOS

## Branching strategy

```
feature/*  ┐
fix/*      ├──PR──▶  dev  ──PR──▶  main
hotfix/*   ┘        (review +      (review + ALL
                     scans)         checks + guard)
```

- **`main`** — protected release branch. Always deployable. **Never committed to directly.**
  PRs into `main` may come **only from `dev`** (or `hotfix/*` for emergencies) and require
  review + all status checks to pass.
- **`dev`** — integration branch and the **default** for new PRs. All everyday work merges here
  first, behind review + scans.
- **`feature/*`, `fix/*`, `hotfix/*`** — short-lived working branches. Branch from `dev`
  (or `main` for a `hotfix/*`), open a PR back into `dev`.

### Day-to-day flow

```bash
git checkout dev && git pull
git checkout -b feature/short-description      # or fix/...  (hotfix/... branches from main)
# ...commit work...
git push -u origin feature/short-description
gh pr create --base dev                        # PRs default to dev
```

When `dev` is ready to release, open a PR **from `dev` into `main`**. It must pass review and
every status check (the `guard` check rejects PRs into `main` from anything but `dev`/`hotfix/*`).

## Required checks (gates)

Every PR runs and must pass:

| Check | What it does |
|-------|--------------|
| `lint` | `py_compile` + `ruff` (real-error subset) on Python |
| `wiki-lint` | `tools/wiki_lint.py` — broken links + leakage scan (no secrets/IBAN/PHI in `wiki/`) |
| `secret-scan` | Gitleaks — no secrets anywhere in the repo |
| `bandit` | Python security scan (fails on medium+ severity) |
| `guard` | (PRs into `main` only) rejects sources other than `dev`/`hotfix/*` |

`dependency-review` runs on PRs and the Claude Code Review bot comments automatically.
Tag **`@claude`** in an issue or PR comment to ask for help.

## Rules

1. **No secrets, confidential figures, or PHI/PII** in the repo — ever. Keys live in `.env` (git-ignored).
2. **No direct pushes to `main` or `dev`** — everything goes through a PR.
3. **Contributor PRs need owner review + green checks** before merge.
4. Keep changes surgical; update `CLAUDE.md`/docs when behavior or structure changes.

## Maintainers

The repository owner reviews and merges. Branch protection is configured so that, as the
project gains a second maintainer, admin-bypass can be turned off to make review mandatory for
everyone (see the note in the repo's branch-protection settings).
