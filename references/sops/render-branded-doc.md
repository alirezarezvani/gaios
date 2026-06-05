# Render a branded document

**Objective:** Produce a polished, on-brand HTML document (report, handoff doc, recurring update) without the model hand-building markup — deterministic rendering from the brand tokens.

**Trigger:** Any time a deliverable should look on-brand: `/exec-cockpit` outputs, a report, a stakeholder update.

**Inputs:**
- A **content JSON** describing the document (title, subtitle, blocks: headings, paragraphs, KPI cards, tables, callouts). The agent assembles this from context / live data.
- `brand-assets/brand-tokens.json` (styling — automatic).

**Tools:** `tools/render_brand_html.py` (deterministic renderer). MCP tools may supply the live numbers.

**Steps:**
1. Gather content. For confidential figures, pull **live** from the source at draft time — never from a stored copy.
2. Write the content JSON to `.tmp/` (git-ignored).
3. Run: `python tools/render_brand_html.py --content .tmp/<name>.json --out .tmp/<name>.html`.
4. Review the HTML; iterate the content JSON if needed.
5. **Deliver:** external/stakeholder docs → **draft only**, hand to the user to send (guardrail). Internal docs → publish to your sanctioned cloud.

**Output:** A self-contained branded `.html` in `.tmp/`. **Never committed to git if it contains confidential figures.**

**Edge cases & learnings** *(append as discovered — don't overwrite without asking):*
- Email clients ignore `<style>` blocks — for email, inline the styles rather than using this web/PDF output as-is.
- Table cells can carry tone: `{"text": "+23.0", "tone": "positive"}` → green; `"tone": "critical"` → red. Don't auto-color by sign (the meaning depends on the metric).

**Guardrails:** no confidential figures committed to git; cite-don't-invent; draft-never-send external; secrets in `.env`.
