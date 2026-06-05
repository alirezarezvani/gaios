#!/usr/bin/env python3
"""
experiment_log.py — WAT tool (generic, blueprint-safe)

Manage an experiment trail for the autoresearch-style loop (references/sops/experiment-loop.md).
Domain-agnostic: works for any experiment with a single numeric metric. Stdlib only.

TSV columns (tab-separated; commas are allowed in notes):
    id    metric    status    note
  - id:     short run id / git short-hash
  - metric: the objective metric value (float); use 0 for crashes
  - status: keep | discard | crash
  - note:   one-line description of what the experiment tried

Usage:
    python tools/experiment_log.py init  <results.tsv>
    python tools/experiment_log.py add   <results.tsv> --id a1b2c3 --metric 0.1234 --status keep --note "seasonal+trend"
    python tools/experiment_log.py show  <results.tsv>
    python tools/experiment_log.py best  <results.tsv> [--maximize]
"""
import argparse
import sys
from pathlib import Path

HEADER = "id\tmetric\tstatus\tnote"


def init(path: Path) -> int:
    if path.exists():
        print(f"exists, leaving as-is: {path}")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEADER + "\n", encoding="utf-8")
    print(f"OK: created {path}")
    return 0


def add(path: Path, run_id: str, metric: float, status: str, note: str) -> int:
    if status not in ("keep", "discard", "crash"):
        print(f"ERROR: status must be keep|discard|crash, got {status!r}", file=sys.stderr)
        return 1
    if not path.exists():
        init(path)
    note = note.replace("\t", " ").replace("\n", " ")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{run_id}\t{metric:.6f}\t{status}\t{note}\n")
    print(f"OK: logged {run_id}  metric={metric:.6f}  {status}")
    return 0


def _rows(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        if line.strip():
            parts = line.split("\t")
            if len(parts) >= 4:
                yield parts[0], parts[1], parts[2], "\t".join(parts[3:])


def show(path: Path) -> int:
    if not path.exists():
        print(f"ERROR: no such file: {path}", file=sys.stderr)
        return 1
    rows = list(_rows(path))
    print(f"{'id':<10} {'metric':>12} {'status':<8} note")
    print("-" * 60)
    for rid, metric, status, note in rows:
        print(f"{rid:<10} {metric:>12} {status:<8} {note}")
    print(f"\n{len(rows)} experiments")
    return 0


def best(path: Path, maximize: bool) -> int:
    if not path.exists():
        print(f"ERROR: no such file: {path}", file=sys.stderr)
        return 1
    kept = [(rid, float(m), note) for rid, m, status, note in _rows(path) if status == "keep"]
    if not kept:
        print("no kept experiments yet")
        return 0
    winner = (max if maximize else min)(kept, key=lambda r: r[1])
    print(f"best ({'max' if maximize else 'min'}): {winner[0]}  metric={winner[1]:.6f}  — {winner[2]}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Manage an experiment results trail (TSV).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "show"):
        sp = sub.add_parser(name)
        sp.add_argument("path")
    sp = sub.add_parser("add")
    sp.add_argument("path")
    sp.add_argument("--id", required=True, dest="run_id")
    sp.add_argument("--metric", required=True, type=float)
    sp.add_argument("--status", required=True)
    sp.add_argument("--note", default="")
    sp = sub.add_parser("best")
    sp.add_argument("path")
    sp.add_argument("--maximize", action="store_true", help="higher metric is better (default: lower)")
    args = ap.parse_args(argv)

    path = Path(args.path)
    if args.cmd == "init":
        return init(path)
    if args.cmd == "add":
        return add(path, args.run_id, args.metric, args.status, args.note)
    if args.cmd == "show":
        return show(path)
    if args.cmd == "best":
        return best(path, args.maximize)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
