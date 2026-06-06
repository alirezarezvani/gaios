#!/usr/bin/env python3
"""
graphify_setup.py — WAT tool (graphify installer/checker)

Sets up **graphify** (the knowledge-graph builder) so gAIOS's /graph skills work
in both Claude Code and Codex. graphify ships its own /graphify skill; this tool
installs the CLI and copies that skill into each platform's global skills dir, so
the gAIOS graph workflows can call it.

What it does NOT do: it never points graphify at data, never reads secrets, and
never runs anything destructive. Graph *scope* (CODE + committed wiki/ only;
hard-exclude raw/, .env, .tmp/) is enforced by the /graph skills, not here.

Subcommands:
    check    (default) — is the `graphify` CLI available + importable? exit 0/1.
    install            — install graphifyy if missing, then `graphify install
                         --platform <p>` for each requested platform (idempotent).

Usage:
    python tools/graphify_setup.py                       # check (default)
    python tools/graphify_setup.py check
    python tools/graphify_setup.py install               # platforms: claude,codex
    python tools/graphify_setup.py install --platforms claude
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import subprocess
import sys

CLI = "graphify"
MODULE = "graphify"
DEFAULT_PLATFORMS = ["claude", "codex"]

# Install strategies, tried in order. List args only — never shell=True.
INSTALL_STRATEGIES: list[tuple[str, list[str]]] = [
    ("uv tool install graphifyy", ["uv", "tool", "install", "graphifyy"]),
    ("pipx install graphifyy", ["pipx", "install", "graphifyy"]),
    ("pip install --user graphifyy", [sys.executable, "-m", "pip", "install", "--user", "graphifyy"]),
]


def cli_on_path() -> str | None:
    """Absolute path to the graphify CLI, or None if not on PATH."""
    return shutil.which(CLI)


def module_importable() -> bool:
    """True if the graphify Python module can be found."""
    return importlib.util.find_spec(MODULE) is not None


def run(cmd: list[str]) -> tuple[int, str]:
    """Run a command (list args, no shell); return (returncode, combined output)."""
    try:
        proc = subprocess.run(  # noqa: S603 - list args, shell=False, no user-controlled binary
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 127, f"not found: {cmd[0]}"
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def cli_help_works() -> bool:
    """Verify the installed CLI actually runs."""
    if cli_on_path() is None:
        return False
    code, _ = run([CLI, "--help"])
    return code == 0


def cmd_check() -> int:
    """Report whether graphify is usable. Exit 0 if present, 1 if not."""
    path = cli_on_path()
    importable = module_importable()
    if path is not None:
        print(f"OK: graphify CLI found at {path}")
        print(f"    module importable: {'yes' if importable else 'no'}")
        if not cli_help_works():
            print("WARN: `graphify --help` did not exit cleanly — try `install` to repair.")
        return 0
    print("MISSING: graphify CLI not on PATH.")
    print(f"    module importable: {'yes' if importable else 'no'}")
    print("    Fix: python tools/graphify_setup.py install")
    return 1


def install_graphify() -> bool:
    """Install graphifyy via the first available strategy. Return True on success."""
    for label, cmd in INSTALL_STRATEGIES:
        if shutil.which(cmd[0]) is None and cmd[0] != sys.executable:
            print(f"  skip ({label}): {cmd[0]} not available")
            continue
        print(f"  trying: {label}")
        code, out = run(cmd)
        if code == 0 and cli_on_path() is not None:
            print(f"  installed via {label}")
            return True
        tail = out.strip().splitlines()[-1] if out.strip() else f"exit {code}"
        print(f"  failed ({label}): {tail}")
    return False


def install_platform_skill(platform: str) -> bool:
    """Copy graphify's /graphify skill into one platform's global skills dir. Idempotent."""
    print(f"  graphify install --platform {platform}")
    code, out = run([CLI, "install", "--platform", platform])
    if code == 0:
        print(f"    ok ({platform})")
        return True
    tail = out.strip().splitlines()[-1] if out.strip() else f"exit {code}"
    print(f"    FAILED ({platform}): {tail}")
    return False


def cmd_install(platforms: list[str]) -> int:
    """Install graphify if missing, then wire each platform. Exit non-zero if unusable."""
    if cli_on_path() is None:
        print("graphify CLI missing — installing graphifyy...")
        if not install_graphify():
            print("ERROR: could not install graphify. Install manually, then re-run:")
            print("    uv tool install graphifyy   # or: pipx install graphifyy")
            return 1
    else:
        print(f"graphify already installed at {cli_on_path()}")

    if not cli_help_works():
        print("ERROR: graphify is installed but `graphify --help` failed.")
        return 1

    print("Wiring platforms...")
    results = [install_platform_skill(p) for p in platforms]

    if cli_on_path() is None:
        print("ERROR: graphify still unavailable after install.")
        return 1

    print("")
    print("Next steps:")
    print("  - In Claude Code or Codex, run the gAIOS graph skill: /graph")
    print("  - Default graph scope is CODE + the committed wiki/ ONLY.")
    print("    Never point graphify at raw/, .env, or .tmp/ (may hold un-de-identified data).")
    print("  - Outputs land in graphify-out/ (git-ignored): graph.html, GRAPH_REPORT.md, graph.json")

    return 0 if all(results) else 1


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="graphify_setup.py",
        description="Check or install graphify so gAIOS's /graph skills work in Claude Code + Codex.",
    )
    sub = ap.add_subparsers(dest="command")
    sub.add_parser("check", help="report whether graphify is available (default)")
    p_install = sub.add_parser("install", help="install graphify and wire platform skills")
    p_install.add_argument(
        "--platforms",
        default=",".join(DEFAULT_PLATFORMS),
        help="comma-separated platforms to wire (default: claude,codex)",
    )
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    command = args.command or "check"

    if command == "install":
        platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]
        if not platforms:
            print("ERROR: no platforms given to --platforms", file=sys.stderr)
            return 2
        return cmd_install(platforms)

    return cmd_check()


if __name__ == "__main__":
    raise SystemExit(main())
