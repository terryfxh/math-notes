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


def capture(args: list[str]) -> str:
    """Run a command and return its stdout (stripped); '' on failure."""
    try:
        out = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    except OSError:
        return ""
    return out.stdout.strip()


def actions_url() -> str:
    """Best-effort GitHub Actions URL for this repo, derived from the remote."""
    url = capture(["git", "remote", "get-url", "origin"])
    if not url:
        return ""
    if url.startswith("git@"):  # git@github.com:owner/repo.git
        url = "https://github.com/" + url.split(":", 1)[-1]
    if url.endswith(".git"):
        url = url[:-4]
    return url + "/actions"


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


def deploy(message: str, full: bool, dry_run: bool) -> int:
    """Check, commit every tracked change, push, and print the CI run URL.

    Turns the design->live loop into one step. Design-system scratch files are
    gitignored, so staging everything is safe; the file list is always printed
    so nothing slips in unseen. Use --dry-run to preview without committing.
    """
    check = [sys.executable, "tools/check.py"] + ([] if full else ["--fast"])
    if run(check) != 0:
        print("deploy: checks failed; nothing committed or pushed.")
        return 1

    pending = capture(["git", "status", "--short"])
    print("\nChanges to deploy:\n" + (pending or "  (working tree clean)"))

    if dry_run:
        print("\ndry-run: would `git add -A`, commit, and push to the upstream branch.")
        url = actions_url()
        if url:
            print(f"dry-run: CI would run at {url}")
        return 0

    if pending:
        if run(["git", "add", "-A"]) != 0:
            return 1
        # Only commit if something is actually staged.
        if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0:
            if run(["git", "commit", "-m", message]) != 0:
                return 1

    # Push the current branch to its upstream (fall back to origin HEAD).
    rc = run(["git", "push"])
    if rc != 0:
        rc = run(["git", "push", "origin", "HEAD"])
        if rc != 0:
            print("deploy: push failed (check your GitHub credentials and upstream).")
            return rc

    url = actions_url()
    if url:
        print(f"\nPushed. CI is rendering and publishing to gh-pages — watch it at:\n  {url}")
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

    dep = sub.add_parser(
        "deploy",
        help="Check, commit all changes, push to main, and print the CI run URL (design->live in one step).",
    )
    dep.add_argument("-m", "--message", required=True, help="Commit message.")
    dep.add_argument("--full", action="store_true", help="Run full-check (execute code cells) instead of fast-check.")
    dep.add_argument("--dry-run", action="store_true", help="Preview what would be committed/pushed without doing it.")

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
    if args.command == "deploy":
        return deploy(args.message, args.full, args.dry_run)
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
