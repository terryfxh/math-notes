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


def install_hooks() -> int:
    """Install a git pre-commit hook that keeps WORKLOG.md in sync and fast-checks."""
    hooks_dir = ROOT / ".git" / "hooks"
    if not hooks_dir.exists():
        print("error: .git/hooks not found (is this a git repo?)")
        return 1
    hook = hooks_dir / "pre-commit"
    hook.write_text(
        "#!/bin/sh\n"
        "# Auto-installed by tools/blog.py install-hooks.\n"
        "# Refresh the work log, stage it, then run fast checks before each commit.\n"
        "python tools/worklog.py || exit 1\n"
        "git add WORKLOG.md\n"
        "python tools/check.py --fast || exit 1\n",
        encoding="utf-8",
    )
    try:
        hook.chmod(0o755)
    except OSError:
        pass  # Windows ignores the bit; Git for Windows runs the hook via sh regardless.
    print(f"Installed pre-commit hook at {hook.relative_to(ROOT).as_posix()}")
    print("Each commit now refreshes WORKLOG.md and runs `check.py --fast` first.")
    return 0


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
    pre = sub.add_parser(
        "preflight",
        help="One-step pre-publish: run checks, then sync WORKLOG.md.",
    )
    pre.add_argument("--fast", action="store_true", help="Skip code execution (fast-check).")
    sub.add_parser("install-hooks", help="Install a git pre-commit hook (worklog + fast-check).")
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
    if args.command == "preflight":
        check = [sys.executable, "tools/check.py"]
        if args.fast:
            check.append("--fast")
        rc = run(check)
        if rc != 0:
            print("preflight: checks failed; not updating WORKLOG.md.")
            return rc
        return run([sys.executable, "tools/worklog.py"])
    if args.command == "install-hooks":
        return install_hooks()
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
