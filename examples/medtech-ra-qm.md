# Direction: Regulated health / medtech — Regulatory Affairs & Quality

> **Direction, not data.** This shows the *shape* of a filled gAIOS for a regulated environment —
> the strictest guardrail case. Write your own via `/setup`. Copy the thinking, not the words.

**Closest if:** you work in medical devices, diagnostics, digital health, or pharma, where what
you handle is regulated (PHI/PII) and audited.

## One paragraph about you · `CLAUDE.md` intro + `context/about-me.md`
*Direction:* your RA/QM remit and what you're accountable for under which regulations.
> *Illustrative:* "Head of Regulatory Affairs & Quality at a medical-device company. I own the
> QMS, technical documentation, CE marking, and audit readiness. Accountable for compliance with
> MDR and ISO 13485."

## Knowledge base · `CLAUDE.md` + `context/about-business.md`
*Direction:* what the device/product does, its classification, the regulatory surface.
> *Illustrative:* "We make a <class IIa> device for <clinical use>. Regulatory surface: EU MDR,
> ISO 13485, ISO 14971 (risk), GDPR. Notified body: <reference, not named here>."

## What eats your week / deepest pain · `context/about-me.md`
*Direction:* the documentation/audit drudgery and the structure that's missing.
> *Illustrative:* "Keeping technical files current, CAPA tracking, and prepping audits. Deepest
> pain: traceability — finding which document/decision supports which requirement."

## Priorities — next ~90 days · `context/priorities.md`
*Direction:* dated compliance outcomes.
> *Illustrative:* "1) Close open CAPAs before the surveillance audit. 2) Update the risk file for
> <change>. 3) Finalize the clinical evaluation report."

## Guardrails — your sensitive-data line · `CLAUDE.md` ← read this one closely
*Direction:* this is the regime gAIOS is most careful about. Be absolute.
> *Illustrative:* "**No PHI/PII, ever** — no patient data, no clinical identifiers in prompts,
> logs, or this repo. Reference clinical/regulatory specifics; never transcribe them. Every
> regulatory/clinical claim **cites a source or is flagged** — never fabricated. All
> external/regulatory submissions are **drafts I review and send**."

## Voice fingerprint · `references/voice.md`
*Direction:* paste real samples; regulated writing is precise and sourced.
> *Illustrative:* "Formal, precise, traceable. References clause/standard numbers. No hedging, no
> unsupported claims."

## Likely connections · `connections.md`
*Direction:* the regulated stack — most things read-only.
> *Illustrative:* eQMS (read-only) · document control · Jira (CAPA/issues) · SharePoint/Confluence ·
> calendar. Keep clinical systems out of the repo entirely.

## First prompts to try
- "Draft a CAPA summary from these findings — cite the relevant ISO 13485 clauses or flag gaps."
- "What's missing in this technical file against MDR Annex II? Cite or flag."
- "Prep me for the surveillance audit: open items, owners, evidence locations."
