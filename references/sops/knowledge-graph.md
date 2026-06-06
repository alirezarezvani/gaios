# SOP: Knowledge graph (graphify) in gAIOS

**Objective:** Turn the gAIOS repo — its **code** and its **committed `wiki/`** — into a queryable
knowledge graph, so you can *see* what you built (no dark code), find the real constraint (God Nodes),
and ask the structure questions instead of grepping. graphify is the WAT **tool**; `/graph`,
`/graph-query`, and `/graph-ingest` are the **workflows**; you (the agent) are the decision-maker who
keeps the scope safe and honors the audit trail.

**When to use:**
- Before reasoning about a non-trivial part of the codebase ("graph it before you reason about it").
- After a batch of `/wiki` entries lands — refresh the graph so the second brain is connected, not siloed.
- When a change feels risky and you need impact analysis ("what depends on this?").
- On a recurring `/weekly` cadence, or auto via the post-commit hook / `--watch`.
- To pull an external source (a doc, a repo, a URL) into the loop via `/graph-ingest`.

Reuse first: graphify is already installed as a tool (see `connections.md`); don't rebuild graph
logic. Full CLI/flag/MCP reference lives in **`references/graphify-api.md`** — this SOP is the *how
and the guardrails*, that file is the *exact commands*.

---

## The second-brain loop

graphify plugs into the existing capture → admit cycle. It adds a **graph** stage and a **query**
stage on top of `raw/ → /wiki → wiki/`, and it **never reads `raw/`**.

```
  CAPTURE            ADMIT                 GRAPH                  QUERY
  ───────            ─────                 ─────                  ─────
  /graph-ingest      /wiki                 /graph                 /graph-query
  graphify add <url> de-identify + merge   graphify update over   query_graph / path /
   → ./raw/          + wiki_lint gate       CODE + committed      explain over graph.json
                     → wiki/  (committed)    wiki/  → graphify-out/  (CLI or MCP)
  [git-ignored]      [the safety gate]      [graphify-out/ git-ignored]

      raw/  ──────►  wiki/  ──────►  graph  ──────►  answers
   (never graphed)  (safe to graph)  (derived)     (cite the audit trail)
```

The seam between **capture** and **admit** is the guardrail line: raw material (which can hold PHI/PII/
financials before de-identification) is fetched into `raw/` and **stops there** until `/wiki` has
de-identified it and `wiki_lint.py` has passed. Only the committed, clean `wiki/` — plus code — is
ever handed to the graph builder.

---

## Inputs

- **Code** in the repo (tree-sitter AST extraction — local, deterministic, no LLM).
- The **committed `wiki/`** (already de-identified / non-confidential per the wiki admission policy).
- Optionally, external sources pulled by `/graph-ingest` → `raw/` → `/wiki` → `wiki/` *before* graphing.
- **Never:** `raw/`, `.env`, `.tmp/`, or any sensitive/secret path. See **Guardrails**.

---

## Procedure

### 1. Scope the graph (the safety step — do this first)
Decide what to feed. Default scope = **code + committed `wiki/` only**. Confirm the target path(s)
exclude `raw/`, `.env`, `.tmp/`, `archives/` of secrets, and anything regulated.
- **Verify:** the path you'll pass to graphify does **not** resolve into `raw/` or a secret dir;
  `git check-ignore graphify-out` returns a match (the output dir is ignored). If in doubt, scope to
  `wiki/` and the source dirs explicitly rather than the repo root.

### 2. Ingest external material (only if needed) — `/graph-ingest`
For a URL / doc / repo you want in the second brain: `graphify add <url>` fetches to `./raw/` (it does
**not** graph it yet). Then run `/wiki` to de-identify + merge into `wiki/`, and let `wiki_lint.py` gate it.
- **Verify:** the fetched file is in `raw/` (git-ignored), the resulting wiki entry passes
  `python tools/wiki_lint.py`, and the raw capture has moved to `raw/_archive/`. Nothing sensitive is
  staged for commit.

### 3. Build / update the graph — `/graph`
Run graphify over the scoped target (code re-extraction is no-LLM; non-code text in `wiki/` is
extracted by the **host IDE session**, not a third party). Outputs land in `graphify-out/`
(`graph.html`, `graph.json`, `GRAPH_REPORT.md`, `cost.json`, `cache/`).
- **Verify:** `graphify-out/graph.json` exists and `GRAPH_REPORT.md` lists God Nodes + Surprising
  Connections; confirm `graphify-out/` is git-ignored (it is a derived artifact — never commit it).

### 4. Read the report before querying
Open `GRAPH_REPORT.md`: **God Nodes** (highest-connectivity = likely constraints), **Surprising
Connections**, **Suggested Questions**. This is your Map-the-Process artifact — read it like one.
- **Verify:** you can name the top God Nodes and at least one surprising edge before acting on the graph.

### 5. Query — `/graph-query`
Ask structure questions: `graphify query "<q>"`, `graphify path "A" "B"`, `graphify explain "X"`.
For repeated/programmatic querying, stand up the MCP server
(`python3 -m graphify.serve graphify-out/graph.json` → `query_graph`, `get_node`, `get_neighbors`,
`get_community`, `god_nodes`, `graph_stats`, `shortest_path`).
- **Verify:** every claim you carry out of a query is traceable to an edge labelled
  **EXTRACTED / INFERRED / AMBIGUOUS** — and you carry that label forward (cite, don't invent).

### 6. Keep it fresh (cadence)
Wire one of the cadence options below so the graph tracks reality instead of going stale.
- **Verify:** after a representative commit, the graph reflects the change (re-run a known query, or
  check the hook/`watch` rebuilt `graph.json`).

---

## The 3Ms mapping (100% integrated)

graphify is not a bolt-on — it expresses each layer of the operator brain (`references/3ms-framework.md`).

### MINDSET (how to think)
- **The Curiosity Rule → anti-dark-code.** Never accept structure you can't see. The graph *visualizes
  what you built* (`graph.html`, God Nodes), turning "dark code" into something you can explain. If you
  can't explain how a part connects, you've built a liability — graph it until you can.
- **The Default Shift → "graph it before you reason about it."** Before tracing dependencies by hand or
  grepping for callers, ask: could the graph answer this? Make graphing the *first* move on any
  non-trivial reasoning task, not the fallback.

### METHOD (how to decide)
- **Find the Constraint → God Nodes + impact analysis.** The "if 500 clients showed up, what breaks
  first?" question has a structural answer: the **God Nodes** (highest-connectivity nodes) are the
  bottlenecks; `shortest_path` / `get_neighbors` give you blast-radius before a risky change.
- **Map the Process → the graph *is* the map.** `GRAPH_REPORT.md` + `graph.html` are the
  Map-the-Process artifact (trigger → data → transform → decision → destination, made visible). Don't
  draw the map by hand when the tool produces it.

### MACHINE (how to build and operate)
- **Boring is Beautiful → deterministic core.** Code extraction is tree-sitter AST, **no LLM** — the
  reliable, repeatable half of the system. The probabilistic part (non-code extraction by the host
  session) is scoped to the *already-safe* `wiki/` only.
- **The Lego Principle → composable queries.** Small, single-purpose graph queries (`query`, `path`,
  `explain`, MCP tools) chain into bigger answers — one input, one output per block.
- **The Validation Chain → the honesty audit trail = cite-don't-invent.** Every edge is labelled
  **EXTRACTED** (in the source), **INFERRED** (the model's leap), or **AMBIGUOUS** (uncertain). That
  label *is* the citation — it satisfies gAIOS Guardrail #6 ("cite, don't invent"). Treat INFERRED /
  AMBIGUOUS edges as claims to verify, not facts.
- **Cadence (Operate) → auto-rebuild.** The post-commit **hook** and **`--watch`** keep the graph
  current with low ceremony — Boring-is-Beautiful operations, not heroics.

---

## Guardrails (from CLAUDE.md — HARD)

1. **Scope = code + committed `wiki/` ONLY.** Hard-exclude `raw/`, `.env`, `.tmp/`, and any
   sensitive/secret path. **Never point graphify's document extraction at `raw/`** — it can hold raw
   PHI/PII/financials before de-identification. (Guardrails #1, #2, #7.)
2. **`wiki/` is safe to graph** precisely because the wiki admission policy already made it
   de-identified, non-confidential, secret-free (`references/sops/wiki-translate.md`,
   `tools/wiki_lint.py`).
3. **`graphify-out/` is git-ignored** — a derived artifact. Never commit the graph, the cache, or
   `cost.json`. Regenerate, don't persist.
4. **Non-code extraction uses the host IDE session**, not a third party — graphify does not read
   `ANTHROPIC_API_KEY` or call out in-IDE, and auto-skips sensitive files during detection. Acceptable
   *because* the only non-code input we feed it is the already-safe `wiki/`.
5. **Honor the audit trail.** Carry **EXTRACTED / INFERRED / AMBIGUOUS** forward into any answer or
   artifact. Never launder an INFERRED edge into a stated fact. (Guardrail #6: cite, don't invent.)
6. **Draft-not-send still applies.** Anything the graph helps you write for an external audience is a
   draft; the human sends. (Guardrail #3.)

If a build would pull a path outside the sanctioned scope, **stop and re-scope** — do not "just try the
repo root."

---

## Cadence options (keep the graph alive)

Pick the lightest that keeps the graph honest (Boring is Beautiful — default low):

- **Post-commit hook (recommended).** `graphify hook install` rebuilds the graph after each commit, so
  code changes are reflected without thinking about it. `graphify hook status` to check;
  `graphify hook uninstall` to stop. Scope stays code + `wiki/` by config.
- **`--watch`.** `graphify ... --watch` (or `/graph --watch`) rebuilds on file changes during an active
  work session — good while actively refactoring a subsystem.
- **`/weekly` graph refresh.** Fold a graph rebuild + a skim of `GRAPH_REPORT.md` (new God Nodes, new
  Surprising Connections) into the weekly operating review — a deliberate, human-in-the-loop checkpoint
  even if the hook is off.

All three obey the same scope guardrail: code + committed `wiki/`, never `raw/`/`.env`/`.tmp/`.

---

## Edge cases

- **Sensitive file slips into scope.** graphify auto-skips detected sensitive files, but treat that as a
  backstop, not the control. If lint or detection flags anything, **stop**, re-scope to explicit safe
  dirs, and (if it reached `raw/` via ingest) finish `/wiki` de-identification before graphing.
- **`raw/` accidentally targeted.** Never graph `raw/`. If a command would, abort and point at `wiki/` +
  source dirs instead. raw material is graphed *only after* it has become a committed wiki entry.
- **Stale graph.** If a query contradicts the code, the graph is stale — re-run `/graph` (or check the
  hook/`watch` is active) before trusting it.
- **INFERRED / AMBIGUOUS answer.** Don't act on it as fact: verify against the source, or label it
  "⚠️ inferred — confirm" exactly as the wiki loop logs uncertainty.
- **`graphify-out/` shows up in `git status`.** It must be ignored; if it isn't, add it to
  `.gitignore` — never commit derived graph artifacts (they can re-encode repo internals).
- **Large repo / cost.** Check `graphify-out/cost.json`; scope tighter (specific subdirs) and use
  `--no-cluster` / `--no-viz` for faster, cheaper rebuilds when you only need the graph data.

---

## Pointers

- **Skills:** `/graph` (build/update) · `/graph-query` (ask the graph) · `/graph-ingest` (pull a source
  into `raw/` → `/wiki` → graph).
- **Tool reference:** `references/graphify-api.md` — full CLI commands, slash flags, outputs, and the
  MCP server tools.
- **Related SOPs:** `references/sops/wiki-translate.md` (the admit gate) · `references/3ms-framework.md`
  (the operator brain) · `connections.md` (graphify registered as a tool).
