# Medium Article Outline — Promoting gAIOS

> Working doc. An outline + talking points for an article that promotes gAIOS to anyone using Claude Code or Codex. Pick a headline, follow the arc, drop in your own voice and a screenshot or two.

---

## Headline options (pick one, A/B the rest as subtitles)

1. **"Stop Treating Claude Code Like a Coding Tool. Turn It Into Your AI Operating System."**
2. **"I Gave Claude Code a Second Brain and a Chief of Staff. Here's the Open-Source Blueprint."**
3. **"gAIOS: The Folder You Clone to Make Claude Code (or Codex) Actually Run Your Work."**
4. **"From Autocomplete to Operating System: A Free Skeleton That Makes Your AI Hold Your Context."**

**Subtitle:** A clone-and-go blueprint that turns Claude Code or Codex into a personal AI Operating System — one that knows your business, reaches your tools, runs reliable workflows, and drafts in your voice.

---

## The hook (first 150 words — earn the scroll)

- Open on the gap everyone feels: you use Claude Code or Codex daily, but every session starts from zero. It's brilliant *in the moment* and amnesiac *between moments*. You re-explain your role, your priorities, your tone, your stack — every single time.
- Reframe: the problem isn't the model. It's that you're using a general-purpose agent with **no operating system around it.** No memory of who you are. No standard way to do recurring work. No guardrails.
- The promise: **gAIOS is that operating system — as an open, MIT-licensed folder you clone.** Run one command (`/setup`), answer an interview, and your AI goes from reactive vending machine to proactive operator: a *second brain + Chief of Staff.*
- One line that sticks: *"Probabilistic AI reasons; deterministic code executes."* That split is why it's reliable, not just impressive.

---

## Section 1 — The mental shift: from "AI tool" to "AI Operating System"

Talking points:
- Most people prompt. Operators *build a system around* the prompt.
- Introduce the **Four Cs** — the spine of the whole thing:
  - **Context** — it knows your business (identity, team, voice, priorities).
  - **Connections** — it reaches your stuff (CRM, calendar, docs, chat — via MCPs or scripts).
  - **Capabilities** — it knows *how* to do the work (skills + agents).
  - **Cadence** — it runs without being asked (rituals, recurring workflows).
- The honest promise: this isn't "AI replaces you." It's "AI holds your context and runs the boring 60% so you keep judgment."
- Visual idea: a simple 4-quadrant graphic of the Four Cs.

## Section 2 — The operator's brain: the Three Ms

Talking points (this is the philosophy that makes readers trust it):
- **Mindset / Method / Machine** — how to *think*, how to *decide*, how to *build*.
- The killer principle: **"Boring is Beautiful."** Deterministic beats clever. Workflows beat agents. Default to the *lowest* autonomy that works.
- Quote the **Default Shift**: before doing any task the old way, ask *"to what extent could AI be leveraged here?"*
- The **60/30/10 rule**: ~60% fully automated, ~30% AI-assisted (human reviews), ~10% stays manual. "If someone promises 100%, they're selling you something."
- The **Bike Method** (training wheels → guided → watched → hands-off) — you don't go full-autonomy on day one. Roll out 10% of volume, watch a week, expand.
- Credit note: frameworks inspired by Nate Herk's "Three Ms / Four Cs" — gAIOS is an independent, working implementation. (Builds trust; shows intellectual honesty.)

## Section 3 — WAT: why this is reliable, not just a clever prompt

Talking points (the technical credibility beat):
- **W**orkflows · **A**gents · **T**ools.
- The math that lands: *if each step is 90% accurate, five chained steps land at ~59%.* So you offload execution to **boring, testable code** and keep the AI for orchestration and judgment.
- Workflows = the SOPs (skills + `references/sops/`). Agents = the decision-maker (your AI's role). Tools = deterministic operations (Python scripts *and* MCP servers both count).
- The self-improvement loop: on failure → read the error → fix the tool → verify → update the SOP. The system gets *more* reliable with use, not less.

## Section 4 — The capabilities tour (the "what can it actually do" payload)

Walk each skill with a one-line "what it is" + a vivid example. These are the real, shipped skills:

- **`/setup`** — guided first-run interview. Fills `CLAUDE.md`, `context/`, `voice.md`, `connections.md`. *Five minutes from clone to a system that knows you.*
- **`/structure`** — the front door. Turns any fuzzy input (a forwarded email thread, a vague Slack ask, "look into the X thing") into a clean brief: Context · Outcome · Goal · Owner · Next step · Decision needed. *Stop starting work without knowing what "done" looks like.*
- **`/wiki`** — a real second brain. Drop messy notes in `raw/`, get clean, cross-linked knowledge in `wiki/` — with a **lint gate that scans for leaked secrets/PII** before anything is committed.
- **`/workflow`** — dynamic, composable, self-verifying pipelines with a quality gate *per step.* Ships with example cards (daily triage, investor update).
- **`/experiment`** — an **autoresearch loop**: try → measure → keep-or-revert → log, on an isolated git branch, with a runnable forecast example. Hill-climb any measurable artifact.
- **`/level-up`** — the weekly ritual that finds *one* new automation and ships it, walking you through the Three Ms. "One interview = one shipped artifact."
- **`/audit`** — scores your setup against the Four Cs (out of 100) and hands you the top-3 highest-leverage fixes. Re-run weekly to watch the score climb.
- **`/exec-cockpit`** — a leadership-transition template: handoff doc, decision-rights map, open-loops tracker, recurring-report drafter.
- **The `tools/` layer** — deterministic Python you can trust: branded-HTML renderer, wiki leak-lint, experiment logger.

## Section 5 — Real-world use cases (the heart of the article — make it concrete per persona)

Frame each as: *the old way (painful) → the gAIOS way.* Cover every reader type:

1. **The founder / solo operator**
   - *Investor update:* `/workflow investor-update` pulls live figures, structures the narrative so every number traces to a source, renders an on-brand HTML draft — and **stops at the draft for you to send.** Figures never get committed to git.
   - *Monday focus:* "What should I focus on this week?" against your real priorities.

2. **The busy executive / team lead**
   - *Morning triage:* `/workflow daily-triage` produces one brief across email + chat + tasks + calendar, each item tagged urgent / waiting-on-you / FYI / delegate, with drafted replies queued for a one-tap send. The inbox stops being the bottleneck.
   - *Stepping into a new role:* `/exec-cockpit` so nothing drops during a transition.

3. **The software engineer (the core Claude Code / Codex user)**
   - *Reliable automation, not vibes:* the WAT split means your recurring chores become testable scripts orchestrated by the agent — not a 200-line prompt you pray works.
   - *Tuning loop:* `/experiment` to hill-climb a model/config/prompt against one objective metric, on a branch, with a logged trail you can defend in review.
   - *Self-documenting decisions:* every meaningful call lands in `decisions/log.md` — an append-only record of *why*.

4. **The consultant / agency**
   - A **forkable methodology you can hand a client.** Clone, `/setup` per engagement, on-brand outputs from the brand kit, guardrails tuned to their compliance regime (GDPR / HIPAA / SOC2).

5. **The knowledge worker / researcher**
   - *Second brain:* the `raw/` → `/wiki` loop turns scattered notes into a cross-linked knowledge base — with a gate that keeps secrets and PII *out* of what gets committed.
   - *Deep questions:* "What did I think about X three months ago?" answered from your own past thinking.

> Pro move for the article: pick ONE of these, run it for real, and screenshot the output. A real artifact beats any description.

## Section 6 — Built-in trust: guardrails and operating discipline

Talking points (this is what makes it *safe* to adopt — don't skip it):
- **Draft, never auto-send external.** The AI drafts customer/investor/public content; the human sends. Internal team comms it *may* send in your voice.
- **No secrets, no confidential figures, no PHI/PII in the repo.** Pull live at use time; never persist. The wiki lint is the enforcing gate.
- **The Intern Rule:** treat the AI like a day-one hire — own credentials, read-only by default, scoped permissions, full audit trail, never impersonates you.
- **The Kill Switch:** if an automation costs more to maintain than it saves, tear it down. Knowing when to *destroy* is as important as when to build.
- **Operating discipline baked into `CLAUDE.md`:** think-before-acting, simplicity first, surgical changes, verify-before-you-claim-done.

## Section 7 — Works with what you already use

Talking points:
- **Claude Code is first-class** (native slash skills). **Codex / Codex CLI is supported** via `AGENTS.md`, which mirrors the same rules and discovers the same skills.
- Other agents (Cursor, Gemini CLI, Copilot) work via instructions — ask for a workflow by name.
- One source of truth: `CLAUDE.md` is canonical; `AGENTS.md` mirrors it for other runtimes.
- It's **MIT-licensed and generic** — nothing tied to one business. Fork it for any role, company, or domain.

## Section 8 — Get started in 5 minutes (the CTA)

1. Clone the repo.
2. Open it in Claude Code or Codex, run **`/setup`**.
3. Answer the guided interview (identity, voice, priorities, stack, team, guardrails).
4. First prompt: *"What should I focus on this week?"*
5. Then run `/audit` to see your Four Cs score — and `/level-up` every Friday to ship one new automation.

- Link to the repo. Invite forks, issues, and contributions.
- Close on the compounding promise: *one small automation a day; six months later, hundreds. The system that holds your context gets more valuable every week you use it.*

---

## Tone & style notes for the draft
- Lead with the reader's pain, not the feature list. Features are Section 4; the *ache* is the hook.
- Use the memorable lines verbatim — they're quotable: "Boring is Beautiful," "probabilistic AI reasons, deterministic code executes," "if someone promises 100%, they're selling you something," "you wouldn't trust someone you just met with your bank account."
- One real screenshot of a `/structure` brief or a rendered investor-update beats three paragraphs.
- Keep the Nate Herk attribution — it reads as honest and disarms the "is this just repackaged?" skeptic.
- Length target: 1,400–2,000 words. Outline supports trimming Sections 6–7 if you need it shorter.
