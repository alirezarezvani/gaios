# Wire connections

Dynamic workflows only hit full speed once the AIOS can pull live data. A fresh clone has **0 connections live**. This is the checklist to wire them. **Auth is interactive — you run these; the agent can't complete OAuth.**

## Order (highest leverage first)
1. **Email + calendar** (e.g. Google Workspace / Microsoft 365) — powers `wf-daily-triage` and most CoS work.
2. **Task / project tracker** (Jira / Linear / Asana / Notion).
3. **CRM** (HubSpot / Salesforce / …) — powers `wf-investor-update`.
Then: code host (GitHub/GitLab), finance/billing, knowledge/files.

## Steps per connector
1. Run the connector's auth (an MCP server, or a `tools/` script with an `.env` key). Complete any OAuth in the browser.
2. Confirm with a **read-only** probe first (e.g. "list my calendar", "show my boards") — no writes.
3. Update `connections.md`: set `mechanism`, `auth`, `last checked = <date>`.
4. Save `references/<tool>-api.md` capturing the useful calls (researched-once-saved-forever).

## Guardrails while wiring
- **Read-only first.** Prove retrieval before any write/post.
- Confirm **data residency** if your domain requires it.
- Keep sensitive/regulated data (PHI/PII) out of the AIOS — business/ops data only.
- Tokens in `.env` (and the connector's secure store) — never in the repo.

## Done = a workflow runs live
When email/calendar + tasks are live, `/workflow daily-triage` runs end-to-end. When the CRM is live, `/workflow investor-update` does too. That's when the speed payoff lands.
