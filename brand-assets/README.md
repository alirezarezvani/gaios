# Brand assets

Your CI/CD so the AIOS produces on-brand output (esp. `/exec-cockpit` HTML). **Ships with placeholders — replace them.**

## To make it yours
- [ ] **Logo** — drop your files here (SVG + PNG, light/dark/reversed)
- [ ] **Colors** — set the hex values in `brand-tokens.json` + `brand-identity.css`
- [ ] **Font** — set `typography.fontFamily` + the webfont link
- [ ] **Preview** — open `brand-preview.html` to check it renders
- [ ] **Email signature / footer** — add your legal/contact block (HTML)

## Files
- `DESIGN.md` — the design system (template)
- `brand-identity.css` / `brand-tokens.json` — consumable tokens (used by `tools/render_brand_html.py`)
- `brand-preview.html` — open in a browser to see the system rendered

## Rules
- No confidential figures or PHI/PII in committed templates — placeholders only.
- Secrets never belong here.
