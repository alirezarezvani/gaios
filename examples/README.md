# Examples — find your starting *direction*

**These are directions, not data.** Their only job: if you open gAIOS and the `{{ }}`
placeholders leave you unsure *what good looks like*, pick the closest role below and see the
*shape* of a well-filled AIOS. Then run **`/setup`** and write your own — your gAIOS will look
nothing like these, and that's the point.

> Nothing here is copied into your repo. Your real content lives in `CLAUDE.md` and `context/`
> after `/setup`. Copy the **thinking**, never the words.

## Pick the closest

| If you're a… | Guide | Guardrail regime it shows |
|---|---|---|
| Early-stage founder / CEO | [`founder-ceo.md`](founder-ceo.md) | Investor comms draft-not-send · no confidential financials |
| Operations leader (scale-up) | [`head-of-operations.md`](head-of-operations.md) | GDPR · SOC 2 · vendor data |
| Regulated health / medtech (RA·QM) | [`medtech-ra-qm.md`](medtech-ra-qm.md) | PHI/PII · MDR · ISO 13485 (the strict one) |
| Solo creator / YouTuber | [`creator-youtube.md`](creator-youtube.md) | Brand voice · sponsorship disclosure |
| Enterprise sales leader | [`sales-leader.md`](sales-leader.md) | CRM/PII · deal confidentiality |

None fits exactly? Use the nearest — every guide maps to the **same fill-points**, so the
*direction* transfers even if your role doesn't.

## How each guide maps to your repo

Every guide walks the same fields, each tagged with the file it lives in:

- **One paragraph about you** → `CLAUDE.md` (intro) + `context/about-me.md`
- **Knowledge base** (what you do · who you serve · this quarter) → `CLAUDE.md` + `context/about-business.md`
- **What eats your week / deepest pain** → `context/about-me.md`
- **Priorities (next ~90 days)** → `context/priorities.md`
- **Guardrails — your sensitive-data line** → `CLAUDE.md` (the field most worth customizing)
- **Voice fingerprint** → `references/voice.md`
- **Likely connections** → `connections.md`

## The one rule these all model

Notice what the guides **don't** do: they never paste real numbers, customer names, or secrets.
They *reference* sensitive things and describe the *direction*. Do the same in your own files —
that's the gAIOS guardrail in action (`CLAUDE.md` → Guardrails).
