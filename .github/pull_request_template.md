<!--
  Branching: feature/* · fix/* · hotfix/*  ──▶  dev  ──▶  main
  • Open against `dev` (default). Only `dev`/`hotfix/*` may target `main`.
  • TITLE must be a Conventional Commit — it becomes the squash commit message.
      e.g.  feat: add daily brief skill   |   fix: handle empty priorities   |   docs: ...
  • This PR AUTO-MERGES once all checks pass. To stop it: add the `hold` label or keep it a draft.
  • dev → main also needs the `ship-it` label (or comment `@claude ship`).
-->

## What & why
<!-- One or two lines: what this changes and the reason. -->

## Linked issues
<!-- Closes #123 — auto-closes the issue on merge. -->

## Type
- [ ] feat
- [ ] fix
- [ ] docs / chore / ci
- [ ] refactor / perf / test

## Checklist
- [ ] Title is a Conventional Commit (`commit-lint` will enforce it)
- [ ] Base branch is correct (`dev` for normal work; `main` only from `dev`/`hotfix/*`)
- [ ] No secrets, confidential figures, or PHI/PII added to the repo
- [ ] Docs / `CLAUDE.md` updated if behavior or structure changed

## Notes for the AI reviewer
<!-- Anything that needs a closer look: tradeoffs, risks, follow-ups. -->
