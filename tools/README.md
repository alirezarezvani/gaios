# tools/ — the WAT execution layer

Deterministic Python scripts. They do the actual work — file ops, transforms, rendering, API calls — so the agent stays on orchestration. Each tool is consistent, testable, and fast.

## Conventions
- **One job per script.** Clear name (`render_brand_html.py`, not `utils.py`).
- **CLI-first.** Take args (`argparse`), print a clear result, exit non-zero on failure.
- **Stdlib by default.** Add a dependency only when it earns its place; record it in `requirements.txt`.
- **No secrets in code.** Read from `.env`. Never hardcode keys, tokens, or confidential data.
- **No confidential output to git.** Write deliverables/intermediates to `.tmp/` (git-ignored) or push to the your sanctioned cloud. Numbers (financial figures, etc.) are passed in at runtime, never baked into a tool.
- **Testable.** Each tool should run from a tiny sample input with no side effects beyond its `--out` path.

## MCPs are tools too
Not every tool is a Python script. MS365 / Atlassian / HubSpot MCP calls are also the "Tools" layer — `connections.md` records which system uses which mechanism. Prefer an existing MCP over writing a script when one covers the task.

## Inventory
| Tool | Does | Input | Output |
|---|---|---|---|
| `render_brand_html.py` | Renders an on-brand HTML doc from a content JSON, styled from `brand-assets/brand-tokens.json` | `--content <json>` | branded `.html` (default `.tmp/`) |
| `wiki_lint.py` | Safety gate for `wiki/`: broken-link + orphan checks, leakage scan (IBAN/secrets = error, currency/PHI markers = warning) | `--path wiki [--strict]` | report; exit 1 on errors |
| `experiment_log.py` | Generic experiment trail (autoresearch loop): init/add/show/best on a `results.tsv` | `init\|add\|show\|best <path>` | TSV trail |

See `references/sops/` for the workflow each tool serves.
