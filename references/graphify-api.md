# graphify — reference (API / CLI / MCP)

> The `references/{tool}-api.md` companion `connections.md` points to. Everything the AIOS needs to wire and drive graphify: install, privacy model, full CLI, the `/graphify` slash skill, outputs, the MCP server, and the gAIOS guardrails that scope it. This is the complete feature reference — keep it in sync when graphify updates.

## What graphify is

graphify is a knowledge-graph builder: point it at a codebase or a folder of documents and it extracts entities and relationships into an explorable graph — nodes (files, functions, classes, concepts, docs), edges (calls, imports, references, conceptual links), communities (clusters), and "God Nodes" (the high-centrality hubs everything depends on). Code is parsed locally via tree-sitter (no LLM); non-code text is read by your own IDE session. The result lands in `graphify-out/` as an interactive `graph.html`, a queryable `graph.json`, and a `GRAPH_REPORT.md`. In gAIOS it gives you a second-brain map over your code **and** your committed `wiki/` — so you can ask "what depends on X", "how do A and B connect", and "what are the hubs I keep forgetting about".

## Install

```bash
uv tool install graphifyy          # PyPI package "graphifyy", CLI "graphify", module "graphify"
# fallbacks:
pipx install graphifyy
pip  install graphifyy
```

Then install graphify's own `/graphify` skill into a platform's global skills dir:

```bash
graphify install --platform claude   # Claude Code
graphify install --platform codex    # Codex
```

No account, no signup. `tools/graphify_setup.py` automates the above (install check + both platform installs) — prefer it so setup is reproducible and logged. Uninstall with `graphify uninstall` (add `--purge` to also remove caches/config).

## Data & privacy

- **Code is processed locally.** tree-sitter builds the AST on your machine — no LLM, no network call for code extraction.
- **Non-code text uses the host session.** Docs / markdown / PDF / images are extracted by the **host IDE session itself** (your own Claude or Codex). graphify does **not** read `ANTHROPIC_API_KEY` and does **not** call a third-party model in-IDE.
- **Auto-skips sensitive files.** During detection it skips files that look sensitive — but treat that as a backstop, not your boundary. The boundary is set by gAIOS scope rules below.
- **Honesty audit trail.** Every edge is labelled **`EXTRACTED`** (read directly from source), **`INFERRED`** (derived/guessed), or **`AMBIGUOUS`** (uncertain). This is what makes graph claims auditable — it maps directly onto the gAIOS "cite, don't invent" rule: trust `EXTRACTED`, verify `INFERRED`/`AMBIGUOUS` before acting on them.

## CLI commands

`graphify <command> [args] [flags]`. Outputs go to `graphify-out/` unless noted.

| Command | Purpose | Key flags |
|---|---|---|
| `install` | Install graphify's `/graphify` skill into a platform's global skills dir | `--platform claude\|codex` |
| `uninstall` | Remove the installed skill | `--purge` (also remove caches/config) |
| `update <path>` | Re-extract a path and rebuild the graph (code = local, no LLM) | `--force` (ignore cache), `--no-cluster` (skip community detection) |
| `cluster-only <path>` | Re-run community detection / clustering on an existing graph, no re-extract | `--no-viz` (skip `graph.html`) |
| `query "<q>"` | Natural-language question against the graph | `--dfs` (depth-first traversal), `--budget N` (node/expansion budget) |
| `path "A" "B"` | Shortest path between two nodes | — |
| `explain "X"` | Explain a node and its surrounding neighborhood | — |
| `add <url>` | Fetch a URL → `./raw`, then `update` to fold it into the graph | `--author`, `--contributor`, `--dir <dir>` |
| `watch <path>` | Watch a path and rebuild on change | — |
| `clone <github-url>` | Clone a GitHub repo and build its graph | — |
| `merge-graphs <g1> <g2>` | Merge two graphs into one | `--out <path>` |
| `diagnose multigraph` | Diagnose issues in a merged/multi-graph | — |
| `hook install\|uninstall\|status` | Manage the post-commit hook that auto-rebuilds the graph | — |
| `claude install\|uninstall` | Write/remove a graphify section in the project `CLAUDE.md` | — |
| `export obsidian` | Export the graph as an Obsidian vault | — |
| `export html` | Export the interactive HTML view | — |
| `export wiki` | Export a wiki-style set of pages | — |
| `export svg` | Export a static SVG of the graph | — |
| `export graphml` | Export GraphML (Gephi / yEd / network tools) | — |
| `export neo4j` | Export for import into Neo4j | — |
| `benchmark` | Run graphify's built-in benchmark | — |
| `extract <path>` | Headless extraction with an explicit backend (no IDE session) | `--backend gemini\|openai\|...` |

> Note on `extract --backend`: this is the one path that calls an external model for non-code text, and it bypasses the host-session model. Do **not** point it at anything in gAIOS scope without an explicit decision logged — the default, IDE-session extraction needs no third-party key.

## Slash usage (`/graphify`)

After `graphify install --platform claude|codex`, the global `/graphify` skill is available:

```
/graphify [path|github-url]            # build/refresh the graph for a path or repo
/graphify add <url>                    # fetch a URL into ./raw and fold it in
/graphify query "what depends on X?"   # ask the graph
/graphify path "A" "B"                 # shortest path between two nodes
/graphify explain "X"                  # explain a node + its neighborhood
```

Flags:

| Flag | Effect |
|---|---|
| `--mode deep` | Deeper extraction pass |
| `--update` | Re-extract / refresh an existing graph |
| `--watch` | Watch and rebuild on change |
| `--wiki` | Also emit the `wiki/` export |
| `--obsidian` | Also emit the `obsidian/` export |
| `--svg` | Also emit a static SVG |
| `--graphml` | Also emit GraphML |
| `--neo4j` | Also emit a Neo4j export |
| `--mcp` | Prep/serve for the MCP server |
| `--no-viz` | Skip building `graph.html` |
| `--directed` | Build a directed graph |

## Outputs (`graphify-out/`)

| Path | What it is |
|---|---|
| `graph.html` | Interactive graph you open in a browser |
| `graph.json` | The graph data — queried by CLI and the MCP server |
| `GRAPH_REPORT.md` | Human report: **God Nodes** (central hubs), **Surprising Connections**, **Suggested Questions** |
| `cost.json` | Token/cost accounting for the run |
| `cache/` | Extraction cache (speeds up re-runs; `update --force` ignores it) |
| `obsidian/` | Obsidian vault export — only when `--obsidian` / `export obsidian` is used |
| `wiki/` | Wiki-page export — only when `--wiki` / `export wiki` is used |

`graphify-out/` is a **derived artifact and is git-ignored** in gAIOS (see guardrails). Rebuild it; don't commit it.

## MCP server

Expose the built graph to an MCP client (e.g. Claude Desktop):

```bash
python3 -m graphify.serve graphify-out/graph.json
```

Tools exposed:

| Tool | Purpose |
|---|---|
| `query_graph` | Natural-language / structured query over the graph |
| `get_node` | Fetch a single node by id/name |
| `get_neighbors` | Neighbors of a node (its direct edges) |
| `get_community` | Members of a community/cluster |
| `god_nodes` | The high-centrality hub nodes |
| `graph_stats` | Summary stats (counts, density, etc.) |
| `shortest_path` | Shortest path between two nodes |

Claude Desktop config snippet (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "graphify": {
      "command": "python3",
      "args": ["-m", "graphify.serve", "graphify-out/graph.json"]
    }
  }
}
```

If you wire this, record it in `connections.md` as a `mcp` mechanism and point its reference back to this file.

## gAIOS guardrails (scope — HARD)

These constrain what graphify may touch inside gAIOS. They override default graphify behavior.

1. **Default graph scope = code + the committed `wiki/` ONLY.** That's the sanctioned input. The committed `wiki/` is safe to graph because it is already de-identified and non-confidential per the wiki admission policy (`references/sops/wiki-translate.md`).
2. **HARD-EXCLUDE `raw/`, `.env`, `.tmp/`, and any sensitive/secret paths.** Never point graphify's document extraction at `raw/` — it can hold raw PHI/PII/financials *before* de-identification. `.env` is secrets; `.tmp/` is disposable. graphify's auto-skip is a backstop, not the boundary — you set the boundary by what path you pass.
3. **`graphify-out/` is git-ignored.** It's derived; rebuild it, never commit it. (Code AST is local; non-code extraction over the de-identified `wiki/` uses the host session, which is acceptable for that scope.)
4. **Keep the gAIOS hard rules.** No secrets / PHI / confidential figures committed. **Cite, don't invent** — graphify's `EXTRACTED` / `INFERRED` / `AMBIGUOUS` trail supports this: lean on `EXTRACTED`, verify the rest before you rely on it. **Draft, never auto-send external** still applies to anything built off the graph.
5. **`extract --backend <provider>` is off-scope by default.** It calls an external model and bypasses the host session — don't run it against gAIOS paths without a logged decision in `decisions/log.md`.
