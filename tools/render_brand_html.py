#!/usr/bin/env python3
"""
render_brand_html.py — WAT tool

Render an on-brand HTML document from a content JSON, styled deterministically
from brand-assets/brand-tokens.json (single source of truth). Stdlib only.

Usage:
    python tools/render_brand_html.py --content path/to/content.json [--out .tmp/doc.html] [--tokens brand-assets/brand-tokens.json]

Content JSON shape:
{
  "title": "Document title",
  "subtitle": "optional subtitle",
  "blocks": [
    {"type": "heading", "level": 2, "text": "Section"},
    {"type": "paragraph", "text": "Body text."},
    {"type": "kpis", "items": [
        {"value": "€ 48.2 K", "label": "MRR (sample)", "status": "positive", "statusLabel": "+2.4% MoM"}
    ]},
    {"type": "table", "caption": "optional", "columns": ["Metric", "Actual", "Budget", "Delta"],
     "numericCols": [1, 2, 3],
     "rows": [["EBIT", "-22.0", "-45.0", {"text": "+23.0", "tone": "positive"}]]},
    {"type": "callout", "variant": "information", "title": "Information.", "text": "..."}
  ],
  "footer": "optional footer line"
}

Guardrails: pass numbers in at runtime; this tool never stores them. Default output is .tmp/
(git-ignored). Do not commit rendered docs that contain confidential figures.
"""
import argparse
import html
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_TOKENS = REPO / "brand-assets" / "brand-tokens.json"
DEFAULT_OUT = REPO / ".tmp" / "render.html"

FONT_LINK = ('<link href="https://fonts.googleapis.com/css2?'
             'family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')


def esc(x) -> str:
    return html.escape(str(x), quote=True)


def load_tokens(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_css(c: dict) -> str:
    """Build the stylesheet from the color tokens so styling never drifts from the brand."""
    return f"""
    :root{{
      --primary:{c['primary']};--secondary:{c['secondary']};--ink:{c['ink']};
      --muted:{c['muted']};--on-primary:{c['on-primary']};--on-secondary:{c['on-secondary']};
      --canvas:{c['canvas']};--surface-card:{c['surface-card']};--surface-tint:{c['surface-tint']};
      --hairline:{c['hairline']};--primary-20:{c['primary-20']};--secondary-20:{c['secondary-20']};
      --positive:{c['positive']};--information:{c['information']};--warning:{c['warning']};--critical:{c['critical']};
      --ff:'Inter','Segoe UI',Helvetica,Arial,sans-serif;
    }}
    *{{box-sizing:border-box}}
    body{{font-family:var(--ff);color:var(--ink);background:var(--canvas);margin:0;line-height:1.4}}
    .wrap{{max-width:920px;margin:0 auto;padding:48px 24px 72px}}
    .eyebrow{{font-weight:700;font-size:12px;letter-spacing:.36px;text-transform:uppercase;color:var(--muted)}}
    h1.title{{font-weight:700;font-size:40px;line-height:1.15;letter-spacing:-.8px;margin:4px 0 4px}}
    .subtitle{{font-weight:500;font-size:20px;color:var(--muted);margin:0 0 24px}}
    h2{{font-weight:700;font-size:32px;line-height:1.2;letter-spacing:-.64px;color:var(--secondary);margin:40px 0 12px}}
    h3{{font-weight:700;font-size:20px;line-height:1.3;letter-spacing:-.4px;margin:28px 0 8px}}
    p{{font-weight:400;font-size:16px;line-height:1.4;margin:0 0 14px}}
    a{{color:var(--primary)}}
    .kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin:16px 0 24px}}
    .metric-card{{background:var(--surface-card);border:1px solid var(--hairline);border-radius:16px;padding:24px;box-shadow:0 1px 2px rgba(72,70,70,.04),0 4px 12px rgba(72,70,70,.08)}}
    .metric-card .value{{font-weight:700;font-size:48px;line-height:1.05;letter-spacing:-1px;color:var(--primary)}}
    .metric-card .lab{{font-size:14px;color:var(--muted);margin:4px 0 10px}}
    .pill{{display:inline-block;border-radius:9999px;font-size:12px;padding:4px 10px;font-weight:600}}
    .pill.positive{{background:var(--primary-20);color:var(--positive)}}
    .pill.information{{background:var(--secondary-20);color:var(--information)}}
    .pill.warning{{background:#FFF3DA;color:#9A6A00}}
    .pill.critical{{background:#FDE8E7;color:var(--critical)}}
    .callout{{border-radius:12px;padding:16px 20px;font-size:15px;border-left:4px solid var(--information);background:var(--secondary-20);margin:0 0 12px}}
    .callout.warning{{border-left-color:var(--warning);background:#FFF3DA}}
    .callout.critical{{border-left-color:var(--critical);background:#FDE8E7}}
    .callout.positive{{border-left-color:var(--positive);background:var(--primary-20)}}
    table{{border-collapse:collapse;width:100%;font-size:14px;margin:8px 0 24px}}
    caption{{text-align:left;font-size:12px;color:var(--muted);padding-bottom:8px}}
    th{{background:var(--secondary);color:var(--on-secondary);text-align:left;padding:10px 12px;font-weight:600}}
    td{{padding:10px 12px;border-bottom:1px solid var(--hairline)}}
    tr:nth-child(even) td{{background:var(--surface-tint)}}
    .num{{text-align:right;font-variant-numeric:tabular-nums}}
    .tone-positive{{color:var(--positive);font-weight:700}}
    .tone-critical{{color:var(--critical);font-weight:700}}
    footer{{font-size:12px;color:var(--muted);border-top:1px solid var(--hairline);padding-top:24px;margin-top:40px}}
    """


def render_block(b: dict) -> str:
    t = b.get("type")
    if t == "heading":
        lvl = int(b.get("level", 2))
        tag = "h2" if lvl <= 2 else "h3"
        return f"<{tag}>{esc(b.get('text',''))}</{tag}>"
    if t == "paragraph":
        return f"<p>{esc(b.get('text',''))}</p>"
    if t == "kpis":
        cards = []
        for it in b.get("items", []):
            pill = ""
            if it.get("statusLabel"):
                status = esc(it.get("status", "information"))
                pill = f'<span class="pill {status}">{esc(it["statusLabel"])}</span>'
            cards.append(
                f'<div class="metric-card"><div class="value">{esc(it.get("value",""))}</div>'
                f'<div class="lab">{esc(it.get("label",""))}</div>{pill}</div>'
            )
        return f'<div class="kpis">{"".join(cards)}</div>'
    if t == "callout":
        variant = esc(b.get("variant", "information"))
        title = f"<strong>{esc(b['title'])}</strong> " if b.get("title") else ""
        return f'<div class="callout {variant}">{title}{esc(b.get("text",""))}</div>'
    if t == "table":
        numeric = set(b.get("numericCols", []))
        head = "".join(
            f'<th class="{ "num" if i in numeric else "" }">{esc(col)}</th>'
            for i, col in enumerate(b.get("columns", []))
        )
        body = []
        for row in b.get("rows", []):
            cells = []
            for i, cell in enumerate(row):
                tone, text = "", cell
                if isinstance(cell, dict):
                    tone, text = cell.get("tone", ""), cell.get("text", "")
                classes = " ".join(filter(None, [
                    "num" if i in numeric else "",
                    f"tone-{tone}" if tone in ("positive", "critical") else "",
                ]))
                cls = f' class="{classes}"' if classes else ""
                cells.append(f"<td{cls}>{esc(text)}</td>")
            body.append(f"<tr>{''.join(cells)}</tr>")
        caption = f"<caption>{esc(b['caption'])}</caption>" if b.get("caption") else ""
        return (f"<table>{caption}<thead><tr>{head}</tr></thead>"
                f"<tbody>{''.join(body)}</tbody></table>")
    raise ValueError(f"Unknown block type: {t!r}")


def render(content: dict, tokens: dict) -> str:
    colors = tokens["color"]
    blocks = "".join(render_block(b) for b in content.get("blocks", []))
    subtitle = f'<p class="subtitle">{esc(content["subtitle"])}</p>' if content.get("subtitle") else ""
    footer = f"<footer>{esc(content['footer'])}</footer>" if content.get("footer") else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(content.get('title','Document'))}</title>
{FONT_LINK}
<style>{build_css(colors)}</style>
</head><body><div class="wrap">
<div class="eyebrow">{esc(content.get('brand',''))}</div>
<h1 class="title">{esc(content.get('title',''))}</h1>
{subtitle}
{blocks}
{footer}
</div></body></html>
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Render an on-brand HTML doc from a content JSON.")
    ap.add_argument("--content", required=True, help="path to content JSON")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output HTML path (default .tmp/render.html)")
    ap.add_argument("--tokens", default=str(DEFAULT_TOKENS), help="brand-tokens.json path")
    args = ap.parse_args(argv)

    try:
        tokens = load_tokens(Path(args.tokens))
        with open(args.content, encoding="utf-8") as f:
            content = json.load(f)
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render(content, tokens), encoding="utf-8")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"OK: wrote {out_path} ({out_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
