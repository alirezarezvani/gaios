# Wiki translate — raw → wiki

**Objective:** Turn captures in `raw/` into clean, cross-linked knowledge in `wiki/`, safely. The growing record of the user's thinking.

**Trigger:** `/wiki`, or "process my raw notes", "update the wiki", or after dropping files into `raw/`.

**Inputs:** files in `raw/` (git-ignored). Existing `wiki/` entries + `wiki/_index.md`.

**Tools:** `tools/wiki_lint.py` (deterministic safety + link check). Reasoning/merging is the agent's job.

## Steps
1. **Read** everything in `raw/` (skip `README.md`).
2. For each capture, decide the topic(s). **One topic per file** in `wiki/`, kebab-case filename.
3. **Read the existing wiki entry first, then merge** — never overwrite blindly. Preserve the user's phrasing where it carries signal (`references/voice.md`); don't sand it into encyclopedia tone.
4. **Apply the admission policy** (below) *as you write* — strip/replace anything inadmissible.
5. **Cross-link** related entries with relative markdown links. Update `wiki/_index.md` (add the entry under the right area; bump the "Last loop" line).
6. If a capture relates to a `projects/` workstream, surface a pointer there too.
7. **Move** each processed file from `raw/` → `raw/_archive/` (same filename). **Never delete.**
8. **Run the lint gate:** `python tools/wiki_lint.py`. Fix any broken links / orphans. If it flags possible leakage, remove or reference-out the sensitive bit before continuing.
9. **Commit** with a clear message (e.g. `wiki: translate 3 captures (fda-pathway, us-emr, team-1on1s)`).

## Admission policy (what may be committed to wiki/)
Only **interpreted, de-identified, non-confidential** knowledge.
- **No PHI** — ever. (Guardrail #1)
- **No live financial figures** (confidential financial figures) and **no named-deal specifics** — reference the source instead ("see your CRM / finance model"). (Guardrail #2)
- **No secrets / credentials.** (Guardrail #7)
- **Cite, don't invent.** For any regulatory/clinical/financial claim, cite the source or flag the gap. (Guardrail #6)
- **When uncertain, log it in the entry** ("⚠️ unconfirmed — check with a reviewer") rather than guessing.

## Hard rules (from SimpleBrain, aligned to our guardrails)
1. **Never delete** from `raw/` or `raw/_archive/` — move only.
2. **Never overwrite** a `wiki/` entry blindly — read, then merge.
3. **Never modify** `raw/_archive/` after a file lands — permanent local record.
4. **Commit after meaningful changes**, clear message.
5. **Lint before commit** — the leakage scan is a gate, not a suggestion.

## Answering questions from the wiki
To answer an ad-hoc question about past thinking: read `wiki/_index.md` first, then the 3–10 relevant entries (and `raw/_archive/` if needed). Answer with relative links to the entries used. Offer to file the answer back as a new wiki entry if it's worth keeping.

## Output
Updated `wiki/` (committed) + processed files in `raw/_archive/` (local). No sensitive data in git.
