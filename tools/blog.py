#!/usr/bin/env python3
"""Small command hub for the blog workflow."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(args: list[str]) -> int:
    print("+ " + " ".join(args))
    return subprocess.call(args, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convenience commands for writing and publishing.")
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="Create a new draft post.")
    new.add_argument("title", nargs="+")
    new.add_argument("--categories", default=None)

    sub.add_parser("status", help="List all posts and publication metadata.")
    sub.add_parser("worklog", help="Sync WORKLOG.md with published posts (run after publishing).")
    sub.add_parser("fast-check", help="Run quick checks without executing code cells.")
    sub.add_parser("full-check", help="Run full checks including Python code cells.")
    sub.add_parser("preview", help="Start Quarto preview.")

    render = sub.add_parser("render", help="Render the site locally.")
    render.add_argument("--execute", action="store_true", help="Execute code cells during render.")

    args = parser.parse_args()

    if args.command == "new":
        cmd = [sys.executable, "tools/new_post.py", " ".join(args.title)]
        if args.categories:
            cmd.extend(["--categories", args.categories])
        return run(cmd)
    if args.command == "status":
        return run([sys.executable, "tools/posts_status.py"])
    if args.command == "worklog":
        return run([sys.executable, "tools/worklog.py"])
    if args.command == "fast-check":
        return run([sys.executable, "tools/check.py", "--fast"])
    if args.command == "full-check":
        return run([sys.executable, "tools/check.py"])
    if args.command == "preview":
        return run(["quarto", "preview"])
    if args.command == "render":
        cmd = ["quarto", "render", "--no-clean"]
        if not args.execute:
            cmd.append("--no-execute")
        return run(cmd)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
