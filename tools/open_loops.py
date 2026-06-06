#!/usr/bin/env python3
"""
open_loops.py — WAT tool (commitment / open-loops tracker)

Deterministic tracking of open loops (commitments owed by/to you) so the
Chief-of-Staff cadence skills don't have to hold them in the model's head.
Surfaced by `/daily` (needs a nudge) and `/weekly` (carrying forward).

Storage is a tab-separated file (default `open-loops.tsv`, git-ignored) — open
loops can name people and commitments, so they stay LOCAL, never committed.

Usage:
    python tools/open_loops.py add "Send the vendor the redlines" --owner me --due 2026-06-10
    python tools/open_loops.py list [--all]
    python tools/open_loops.py overdue [--today 2026-06-06]
    python tools/open_loops.py done 3
    python tools/open_loops.py [--path open-loops.tsv] <command> ...
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

COLUMNS = ["id", "status", "created", "due", "owner", "text"]
DEFAULT_PATH = "open-loops.tsv"


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if parts == COLUMNS:  # header
            continue
        row = dict(zip(COLUMNS, parts + [""] * (len(COLUMNS) - len(parts))))
        rows.append(row)
    return rows


def _write(path: Path, rows: list[dict]) -> None:
    lines = ["\t".join(COLUMNS)]
    for r in rows:
        lines.append("\t".join(str(r.get(c, "")).replace("\t", " ") for c in COLUMNS))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _next_id(rows: list[dict]) -> int:
    ids = [int(r["id"]) for r in rows if r.get("id", "").isdigit()]
    return (max(ids) + 1) if ids else 1


def _today(s: str | None) -> str:
    if s:
        return s
    return dt.date.today().isoformat()


def _fmt(rows: list[dict]) -> str:
    if not rows:
        return "(no open loops)"
    out = []
    for r in rows:
        due = f" due {r['due']}" if r.get("due") else ""
        owner = f" [{r['owner']}]" if r.get("owner") else ""
        out.append(f"  #{r['id']} {r['status']:<4}{owner}{due}  {r['text']}")
    return "\n".join(out)


def cmd_add(args, rows, path):
    new = {
        "id": str(_next_id(rows)),
        "status": "open",
        "created": _today(None),
        "due": args.due or "",
        "owner": args.owner or "",
        "text": args.text.strip(),
    }
    rows.append(new)
    _write(path, rows)
    print(f"added #{new['id']}: {new['text']}")
    return 0


def cmd_list(args, rows, path):
    shown = rows if args.all else [r for r in rows if r.get("status") == "open"]
    print(f"open-loops ({len(shown)} shown):")
    print(_fmt(shown))
    return 0


def cmd_overdue(args, rows, path):
    today = _today(args.today)
    due = [
        r for r in rows
        if r.get("status") == "open" and r.get("due") and r["due"] < today
    ]
    print(f"overdue as of {today} ({len(due)}):")
    print(_fmt(due))
    return 1 if due else 0


def cmd_done(args, rows, path):
    for r in rows:
        if r.get("id") == str(args.id):
            r["status"] = "done"
            _write(path, rows)
            print(f"closed #{args.id}: {r['text']}")
            return 0
    print(f"ERROR: no open loop with id {args.id}")
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Track open loops (commitments).")
    ap.add_argument("--path", default=DEFAULT_PATH, help="TSV store (git-ignored)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add an open loop")
    a.add_argument("text")
    a.add_argument("--owner", default="")
    a.add_argument("--due", default="", help="YYYY-MM-DD")
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("list", help="list open loops")
    ls.add_argument("--all", action="store_true", help="include closed")
    ls.set_defaults(func=cmd_list)

    ov = sub.add_parser("overdue", help="list overdue open loops (exit 1 if any)")
    ov.add_argument("--today", default=None, help="override today (YYYY-MM-DD)")
    ov.set_defaults(func=cmd_overdue)

    dn = sub.add_parser("done", help="mark a loop closed")
    dn.add_argument("id", type=int)
    dn.set_defaults(func=cmd_done)

    args = ap.parse_args(argv)
    path = Path(args.path)
    rows = _read(path)
    return args.func(args, rows, path)


if __name__ == "__main__":
    raise SystemExit(main())
