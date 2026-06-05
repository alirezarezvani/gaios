---
name: wiki
description: Use to run the second-brain loop — turn captures in raw/ into clean, cross-linked knowledge in wiki/, and to answer questions from past thinking. Trigger on "/wiki", "process my raw notes", "update the wiki", "add this to my brain/wiki", "what did I think about X", "what do my notes say about X". Follows references/sops/wiki-translate.md. Enforces the admission policy: no PHI, no live financials, no secrets in the committed wiki.
---

# Wiki — the user's second brain

The loop: **drop notes in `raw/` → `/wiki` translates them into `wiki/` → processed captures move to `raw/_archive/`.** `wiki/` is committed (durable knowledge); `raw/` is git-ignored (may hold sensitive material). Full procedure: `references/sops/wiki-translate.md`.

## Two modes

### 1. Translate (ingest)
When there are files in `raw/`, or the user says "add this to the wiki":
1. Read `raw/` (skip `README.md`) and `wiki/_index.md`.
2. For each capture → pick topic(s), **read the existing entry, then merge** (never overwrite blindly). One topic per file, kebab-case.
3. **Apply the admission policy while writing** — strip PHI, replace live financial figures / named-deal specifics with a reference, drop secrets, cite sources, log uncertainty in-line.
4. Cross-link related entries; update `wiki/_index.md`.
5. **Move** processed files `raw/` → `raw/_archive/` (never delete).
6. Run `python tools/wiki_lint.py` — fix broken links/orphans; if it flags leakage, fix before committing.
7. Commit: `wiki: translate N captures (...)`. (Ask before committing if unsure.)

### 2. Answer (query)
When the user asks what he thought/decided about something:
1. Read `wiki/_index.md`, then the 3–10 relevant entries (+ `raw/_archive/` if needed).
2. Answer in his voice, with relative links to the entries used.
3. Offer to file the answer back as a new entry if it's worth keeping.

## Guardrails (from CLAUDE.md)
- **Admission policy is non-negotiable:** no PHI, no live financials, no secrets in `wiki/`. Reference sensitive specifics, don't transcribe them.
- **Move, never delete** from `raw/` / `raw/_archive/`.
- **Read-then-merge**, never blind overwrite.
- **Lint is a gate** before commit, not a suggestion.
- When uncertain, log it in the entry rather than guessing.

## Boundary (don't duplicate)
`wiki/` = evolving thinking & notes. Keep it distinct from `context/` (stable business facts), `decisions/log.md` (decisions), and the `memory/` store (cross-session facts). If something belongs in one of those, put it there and link, don't copy.
