# raw/ — capture inbox  ·  ⚠️ GIT-IGNORED

Drop anything here you want turned into knowledge: notes, meeting jottings, links, pasted text, exported docs. Then run **`/wiki`** — the agent reads `raw/`, writes/merges clean entries into `wiki/`, and moves each processed file to `raw/_archive/`.

## Safety (this is why raw/ is git-ignored)
- **Nothing in `raw/` is committed to git** — captures may contain PHI, confidential financials, or PII. Keeping them out of git history is the hard line (guardrails #1, #2 in `CLAUDE.md`).
- Only this `README.md` is tracked, so the folder exists in the repo without exposing contents.
- **If a source must be retained durably** (e.g. for an audit trail), store it in the **your sanctioned cloud** — never in git.
- The wiki the agent writes from these captures is committed, but only after the **admission policy** strips PHI / live figures / secrets (see `references/sops/wiki-translate.md`).

## Rules
- **Move, never delete.** Processed files go to `raw/_archive/` (also git-ignored), never deleted.
- One capture per file is easiest, but the agent can split a dumped file into several wiki topics.
