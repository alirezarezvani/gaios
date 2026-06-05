# {{BRAND}} — Design System (template)

The canonical brand identity. Source of truth for any on-brand artifact the AIOS renders (e.g. `/exec-cockpit` HTML). Machine-readable tokens live in `brand-identity.css` and `brand-tokens.json`. **This ships with placeholder values — replace them with your brand.**

> Tip: extract your real colors/type from your brand sheet, drop your logo files here, and update `brand-tokens.json` + `brand-identity.css`. The renderer and `brand-preview.html` pick them up automatically.

## 1. Logo
Drop your lockups here (SVG preferred + PNG fallback): horizontal, stacked, and a reversed/on-color version. Document: clear space, min size, allowed backgrounds, and the don'ts (no recolor/stretch/shadow).

## 2. Color
Fill the token groups in `brand-tokens.json` → `color`:
- **Primary** (your signature color + tints) · **Secondary** · **Text** (ink/subtitle/muted, on-primary, on-secondary) · **System** (positive/information/warning/critical) · **Surface** (canvas/card/soft/tint) · **Neutrals/hairlines**.
- Note the text color to use **on** each background (`on-primary`, `on-secondary`).

## 3. Typography
Set `typography.fontFamily` + the webfont link. Define a scale (headline / title / body / label / link). Pick weights you'll actually load.

## 4. Applying it (HTML / email)
- Load `brand-identity.css` (or inline the variables — email clients need inline styles).
- Page background `canvas`; body text `ink`; accents + CTAs in `primary` with `on-primary` labels.
- Tables: header `secondary` + `on-secondary`; zebra rows `surface-tint`.

## 5. Accessibility
Check every text/background pair against **WCAG AA (4.5:1)**. Never encode meaning by color alone (pair status with a word/sign).

## 6. Asset inventory
Replace the placeholders: logo SVGs, favicon, real palette, real font, and (if you send email) your signature/footer HTML.
