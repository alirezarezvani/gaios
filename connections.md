# Connections

Registry of every system the AIOS can reach. `/audit` checks this file for domain coverage and freshness. `last checked = —` means not yet wired. When you wire a tool, also save `references/{tool}-api.md` (endpoints, auth, common queries). To wire connectors, see `references/sops/wire-connections.md`.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | {{CRM / billing / finance model}} | `not yet connected` | — | — |
| 2 | Customer interactions | {{CRM / inbox}} | `not yet connected` | — | — |
| 3 | Calendar | {{Google / Outlook}} | `not yet connected` | — | — |
| 4 | Communication | {{email / Slack / Teams}} | `not yet connected` | — | — |
| 5 | Project / task tracking | {{Jira / Linear / Asana / Notion}} | `not yet connected` | — | — |
| 6 | Meeting intelligence | {{transcription tool}} | `not yet connected` | — | — |
| 7 | Knowledge / files | {{Drive / SharePoint / Confluence}} | `not yet connected` | — | — |
| 8 | Code | {{GitHub / GitLab}} | `not yet connected` | — | — |
| 9 | Knowledge graph | graphify | `script` (CLI) + optional `mcp` | none — local; in-IDE session | `tools/graphify_setup.py` · see `references/graphify-api.md` |

**Mechanism options:** `mcp` (MCP server), `script` (Python/Bash hitting an API, in `tools/`), `export` (CSV/JSON dump), `key+ref` (`.env` key + `references/{tool}-api.md`), `not yet connected`.

> Guardrail: keep confidential data and secrets out of this repo. Connections pull live at use time; they don't persist it here.
