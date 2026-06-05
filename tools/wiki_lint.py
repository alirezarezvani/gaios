#!/usr/bin/env python3
"""
wiki_lint.py — WAT tool (safety gate for the wiki)

Checks the committed wiki/ before a commit:
  ERRORS  (exit 1): broken relative links · IBANs · secrets/API keys
  WARNINGS (exit 0, or 1 with --strict): currency amounts (possible live financials),
                                          orphan pages, PHI-review markers

The leakage scan enforces the admission policy in references/sops/wiki-translate.md:
no PHI, no live financial figures, no secrets in committed wiki entries. It is a net,
not a guarantee — human judgement still applies.

Usage:
    python tools/wiki_lint.py [--path wiki] [--strict]
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# --- leakage patterns ---
RE_IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
RE_SECRET = re.compile(
    r"(?i)\b(api[_-]?key|secret|password|passwort|access[_-]?token|client[_-]?secret)\b\s*[:=]\s*\S+"
    r"|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}\b"
)
RE_CURRENCY = re.compile(r"(?:€|EUR|k€|T?EUR)\s?\d[\d.,]*|\b\d[\d.,]*\s?(?:€|EUR|k€|TEUR)\b")
RE_PHI = re.compile(
    r"(?i)\b(versichertennummer|sozialversicherungsnummer|patient(?:in|en)?|diagnose|geb\.?\s*am|date of birth|dob)\b"
)
# markdown link: [text](target)
RE_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
RE_INLINE_CODE = re.compile(r"`[^`]*`")  # strip so example links in backticks aren't treated as real


def is_local_md(target: str) -> bool:
    t = target.strip()
    if t.startswith(("http://", "https://", "mailto:", "#")):
        return False
    return True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Lint + leakage-scan the wiki before commit.")
    ap.add_argument("--path", default=str(REPO / "wiki"), help="wiki directory")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 1

    md_files = sorted(p for p in root.rglob("*.md"))
    errors, warnings = [], []
    referenced = set()

    for f in md_files:
        try:
            rel = f.relative_to(REPO)
        except ValueError:
            rel = f  # wiki being linted outside the repo
        lines = f.read_text(encoding="utf-8").splitlines()
        in_fence = False
        for n, line in enumerate(lines, 1):
            # links — skip fenced code blocks and inline code spans
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            elif not in_fence:
                for m in RE_LINK.finditer(RE_INLINE_CODE.sub("", line)):
                    target = m.group(1).strip()
                    if not is_local_md(target):
                        continue
                    tgt_path = (f.parent / target.split("#", 1)[0]).resolve()
                    referenced.add(tgt_path)
                    if not tgt_path.exists():  # check the real filesystem, not just wiki/
                        errors.append(f"{rel}:{n}  broken link → {target}")
            # leakage — scan every line, including code (secrets hide there)
            if RE_IBAN.search(line):
                errors.append(f"{rel}:{n}  IBAN detected — remove from committed wiki")
            if RE_SECRET.search(line):
                errors.append(f"{rel}:{n}  possible secret/key — secrets belong in .env only")
            if RE_CURRENCY.search(line):
                warnings.append(f"{rel}:{n}  currency amount — confirm not a live financial figure")
            if RE_PHI.search(line):
                warnings.append(f"{rel}:{n}  PHI-review marker — confirm no patient data")

    # orphans: entries never referenced and not an index
    for f in md_files:
        if f.name.lower() in ("_index.md", "readme.md"):
            continue
        if f.resolve() not in referenced:
            warnings.append(f"{f.relative_to(REPO)}  orphan — not linked from _index or any entry")

    print(f"wiki_lint: {len(md_files)} files · {len(errors)} errors · {len(warnings)} warnings")
    for e in errors:
        print(f"  ✖ {e}")
    for w in warnings:
        print(f"  ⚠ {w}")

    failed = bool(errors) or (args.strict and bool(warnings))
    if not failed:
        print("OK: wiki passes." if not warnings else "OK with warnings (review above).")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
