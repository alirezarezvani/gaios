# wf-daily-triage (example workflow)

Goal: a morning brief — what's urgent, what's waiting on **you**, today's meetings, open loops — so the inbox stops being the bottleneck.
Success criteria: one brief across email + chat + tasks + calendar, each item with a suggested action/owner; nothing urgent missed.
Trigger: every weekday morning *(phase 2 — `/schedule`; until then, on demand)*.
Autonomy: **auto** for the brief (internal, read-only); any reply it proposes is **drafted** — internal messages to the team may send, **nothing external without approval**.
Owner: you.

## Steps
1. **Pull** unread email + chat mentions + tasks assigned-to/waiting-on you + today's calendar.  `MCP`
   → branch: nothing urgent → short brief; lots → cluster by theme.
2. **Triage** each item → urgent / waiting-on-you / FYI / delegate.
   → run each fuzzy item through `/structure` (Context · Outcome · Owner · Next step).
3. **Route** — for each: suggest *delegate to <teammate>*, *draft a reply*, or *decide* (packaged for fast approval).
   → gate: anything external → mark **draft, needs your send/approval** (don't auto-act).
4. **Compose the brief** — top urgents, waiting-on-you (with decision packets), today's meetings + prep, open loops. In your voice.
5. **Verify** — every flagged-urgent item has a suggested next action + owner.
6. **Deliver** — post the brief to you; drafted internal replies queued for a one-tap send.

## Guardrails
#3 draft-never-send external · #4 internal ok in your voice · cite-don't-invent · route work, don't pool it.
