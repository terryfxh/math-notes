#!/usr/bin/env python3
"""Small command hub for the blog workflow."""
from __future__ import annotations

import argparse
import re
import shutil
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
    if url.startswith("git@"):
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
        pass
    print(f"Installed pre-commit hook at {hook.relative_to(ROOT).as_posix()}")
    print("Each commit now refreshes WORKLOG.md and runs `check.py --fast` first.")
    return 0


def deploy(message: str, full: bool, dry_run: bool) -> int:
    """Check, commit every tracked change, push, and print the CI run URL."""
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
        if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0:
            if run(["git", "commit", "-m", message]) != 0:
                return 1

    rc = run(["git", "push"])
    if rc != 0:
        rc = run(["git", "push", "origin", "HEAD"])
        if rc != 0:
            print("deploy: push failed (check your GitHub credentials and upstream).")
            return rc

    url = actions_url()
    if url:
        print(f"\nPushed. CI is rendering -- watch it at:\n  {url}")
    return 0


def unpublish(slug_or_title: str) -> int:
    """Set a post to draft=true, strip its freeze cache and _site output.

    Source files under posts/ are NOT touched. Run `blog.py deploy` to push live.
    """
    posts_dir = ROOT / "posts"

    candidate = posts_dir / slug_or_title
    if not candidate.is_dir():
        needle = slug_or_title.lower()
        matches = [d for d in posts_dir.iterdir() if d.is_dir() and needle in d.name.lower()]
        if not matches:
            print(f"unpublish: no post found matching '{slug_or_title}'")
            return 1
        if len(matches) > 1:
            names = ", ".join(d.name for d in matches)
            print(f"unpublish: ambiguous -- matched: {names}")
            print("Re-run with the exact slug.")
            return 1
        candidate = matches[0]

    qmd = candidate / "index.qmd"
    if not qmd.exists():
        print(f"unpublish: {candidate.name}/index.qmd not found")
        return 1

    text = qmd.read_text(encoding="utf-8")
    if "draft: true" in text:
        print(f"unpublish: {candidate.name} already draft=true")
    else:
        new_text = re.sub(r"draft:\s*false", "draft: true", text)
        if new_text == text:
            new_text = re.sub(r"(\n---\n)", r"\ndraft: true\1", text, count=1)
        qmd.write_text(new_text, encoding="utf-8")
        print(f"  set draft=true : {qmd.relative_to(ROOT).as_posix()}")

    freeze = ROOT / "_freeze" / "posts" / candidate.name
    if freeze.exists():
        shutil.rmtree(freeze)
        print(f"  removed freeze  : {freeze.relative_to(ROOT).as_posix()}/")

    site_page = ROOT / "_site" / "posts" / candidate.name
    if site_page.exists():
        try:
            shutil.rmtree(site_page)
            print(f"  removed _site   : {site_page.relative_to(ROOT).as_posix()}/")
        except OSError:
            print(f"  _site not removed (CI will clean it on next deploy): {site_page.relative_to(ROOT).as_posix()}/")


    print(f"\nPost '{candidate.name}' unpublished locally.")
    print("Next: python tools/blog.py deploy -m 'unpublish: <title>'")
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
    pre = sub.add_parser("preflight", help="One-step pre-publish: run checks, then sync WORKLOG.md.")
    pre.add_argument("--fast", action="store_true", help="Skip code execution (fast-check).")
    sub.add_parser("install-hooks", help="Install a git pre-commit hook (worklog + fast-check).")
    sub.add_parser("preview", help="Start Quarto preview.")

    dep = sub.add_parser(
        "deploy",
        help="Check, commit all changes, push to main, and print the CI run URL.",
    )
    dep.add_argument("-m", "--message", required=True, help="Commit message.")
    dep.add_argument("--full", action="store_true", help="Run full-check instead of fast-check.")
    dep.add_argument("--dry-run", action="store_true", help="Preview without committing/pushing.")

    render = sub.add_parser("render", help="Render the site locally.")
    render.add_argument("--execute", action="store_true", help="Execute code cells during render.")

    unpub = sub.add_parser(
        "unpublish",
        help="Hide a post: set draft=true, clear freeze cache, remove _site output.",
    )
    unpub.add_argument(
        "slug",
        help="Exact post directory slug or a substring (e.g. 'quidditch').",
    )

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
    if args.command == "unpublish":
        return unpublish(args.slug)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
