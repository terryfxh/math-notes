# Claude Code + skills (gstack & notebooklm) — setup record

**Status: ✅ COMPLETED on 2026-06-08** (native Windows, user `Terry`).
Keep this file as a reference for re-installing on another machine, and for the
NotebookLM first-time login that still needs to be done once.

Both **gstack** and **notebooklm-skill** are *Claude Code skills*: folders under
`~/.claude/skills/` that only run inside **Claude Code** (the terminal AI), not the
Claude desktop app. So Claude Code must be installed first, then the skills placed.

> On Windows, `~` = `C:\Users\Terry`. Claude Code requires a paid plan
> (Pro / Max / Team / Enterprise) — the free plan does not include it.

---

## What is installed (verified)

| Component    | Version / location                          | Status |
|--------------|---------------------------------------------|:------:|
| Git          | 2.54.0                                       | ✅ |
| Node.js      | v24.16.0                                     | ✅ |
| Bun          | 1.3.14                                       | ✅ |
| Claude Code  | 2.1.168 — `C:\Users\Terry\.local\bin\claude.exe` | ✅ |
| notebooklm   | `C:\Users\Terry\.claude\skills\notebooklm`  | ✅ |
| gstack       | `C:\Users\Terry\.claude\skills\gstack` (34 sub-skills) | ✅ |

Both confirmed via `What are my skills?` inside Claude Code. Use them with
`/notebooklm`, `/gstack`, or gstack sub-skills like `/browse`, `/qa`, `/review`, `/ship`.

Note: gstack also created a **global** `C:\Users\Terry\.claude\CLAUDE.md` that routes all
web browsing through `/browse` instead of the built-in chrome tools. This is separate
from the blog project's own `CLAUDE.md`; both apply (and stack) when working in the project.

---

## ▶ Next step still to do: NotebookLM first-time login (one time)

The skill is installed but not yet authenticated. Do this once, inside Claude Code:

1. Build a knowledge base at [notebooklm.google.com](https://notebooklm.google.com):
   create a notebook, upload your sources (PDFs, papers, textbooks, lecture notes),
   then **Share → Anyone with the link → Copy link**.
2. In Claude Code, say: `Set up NotebookLM authentication`
   - First run auto-creates a Python venv and installs Chrome (takes a minute).
   - A Chrome window opens → log in with Google. **Use a dedicated/secondary Google
     account** (browser automation may get flagged by Google).
3. Add your notebook: `Add this NotebookLM to my library: <your-link>`
4. Ask away: `Ask my notebook about <topic>` — answers come back source-grounded
   and citation-backed, with far fewer hallucinations.

For the math blog this is the high-value skill: drop references/textbooks into a
NotebookLM, then query it while drafting posts to get grounded, cited answers.

---

## How it was installed (reference for a fresh machine)

Use **PowerShell** (prompt starts with `PS C:\Users\Terry>`), not CMD.
Close and reopen the terminal after each install so PATH updates.

```powershell
# 1. Prerequisites
winget install Git.Git -e
winget install OpenJS.NodeJS.LTS -e
irm bun.sh/install.ps1 | iex
# verify: git --version ; node --version ; bun --version

# 2. Claude Code
irm https://claude.ai/install.ps1 | iex
# If "claude" is not found after reopening, add its folder to PATH:
$bin = "$env:USERPROFILE\.local\bin"
$u = [Environment]::GetEnvironmentVariable("Path","User")
if ($u -notlike "*$bin*") { [Environment]::SetEnvironmentVariable("Path", "$u;$bin", "User") }
# reopen terminal, then: claude --version  ->  claude  (log in via browser)
```

```text
# 3. Inside Claude Code, paste these as chat messages:

#   notebooklm:
git clone https://github.com/PleasePrompto/notebooklm-skill "C:\Users\Terry\.claude\skills\notebooklm"

#   gstack (let Claude Code run it; uses Git Bash + Bun):
Install gstack: run `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` then add a "gstack" section to my CLAUDE.md.

# 4. Verify: ask "What are my skills?" — both should appear.
```

---

## Which skill needs what

| Skill       | Claude Code | Git | Node + Bun | Python      |
|-------------|:-----------:|:---:|:----------:|:-----------:|
| notebooklm  | yes         | yes | no         | yes (auto)  |
| gstack      | yes         | yes | yes        | no          |
