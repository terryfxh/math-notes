# Agent Plugin Butler

Small workflow for Claude/Codex plugin and skill installs.

## Quick Start

Test Ponytail:

```powershell
pwsh tools/agent-plugin-butler.ps1 test-ponytail
```

Install a Claude/Codex plugin marketplace from GitHub and verify it:

```powershell
pwsh tools/agent-plugin-butler.ps1 install -Url https://github.com/DietrichGebert/ponytail
```

Verify an installed plugin:

```powershell
pwsh tools/agent-plugin-butler.ps1 verify -Url https://github.com/DietrichGebert/ponytail
```

Uninstall a plugin:

```powershell
pwsh tools/agent-plugin-butler.ps1 uninstall -Url https://github.com/DietrichGebert/ponytail
```

Install a GitHub skill folder into both Codex and Claude skill roots:

```powershell
pwsh tools/agent-plugin-butler.ps1 install -Kind skill -Url https://github.com/owner/repo/tree/main/skills/my-skill
```

Install only to Codex:

```powershell
pwsh tools/agent-plugin-butler.ps1 install -Url https://github.com/owner/repo -Targets codex
```

## Behavior

- `auto` mode treats a repo root URL as a plugin marketplace.
- `auto` mode treats a GitHub `/tree/...` URL as a skill folder.
- Plugin installs call the official `claude plugin` and `codex plugin` commands.
- Skill installs reuse Codex's built-in `skill-installer` helper and verify `SKILL.md`.
- Commands fail closed when verification cannot prove the requested install.
- Codex hook trust is deliberately not bypassed. If Codex asks for `/hooks` review, approve it in the UI after reading the hook list.
