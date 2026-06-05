# Wiki — index

Your second brain: the growing web of *interpreted knowledge* — what's been learned, decided, and figured out. Written by the agent from captures in `raw/` via `/wiki`. **Committed to git**, so it's durable and versioned.

**This is not** `context/` (stable facts), `decisions/log.md` (the decision record), or any cross-session memory store. The wiki is dynamic thinking-and-notes, cross-linked, one topic per file.

## Admission policy (what may live here)
Only interpreted, **de-identified, non-confidential** knowledge. **No secrets, no confidential figures, no sensitive/regulated data** (PHI/PII/etc.). Reference sensitive specifics — don't transcribe them. Cite sources; log uncertainty. Full rules: `references/sops/wiki-translate.md`. Enforced by `tools/wiki_lint.py`.

## Conventions
- One topic per file, **kebab-case** (`my-topic.md`).
- Cross-link with relative markdown links (`[other topic](other-topic.md)`).
- Headings/bullets only when earned. Match `references/voice.md`.

## Map
- [example note](example-note.md) — sample entry showing the format _(delete once you have your own)_

---
_Last loop: none yet. Run `/wiki` after dropping notes into `raw/`._
