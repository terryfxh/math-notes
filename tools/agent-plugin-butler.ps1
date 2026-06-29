<#
.SYNOPSIS
Tiny butler for installing, uninstalling, and verifying Claude/Codex plugins
and GitHub-hosted skills.

.EXAMPLES
pwsh tools/agent-plugin-butler.ps1 test-ponytail
pwsh tools/agent-plugin-butler.ps1 install -Url https://github.com/DietrichGebert/ponytail
pwsh tools/agent-plugin-butler.ps1 verify -Url https://github.com/DietrichGebert/ponytail
pwsh tools/agent-plugin-butler.ps1 uninstall -Url https://github.com/DietrichGebert/ponytail
pwsh tools/agent-plugin-butler.ps1 install -Kind skill -Url https://github.com/owner/repo/tree/main/skills/my-skill
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("install", "uninstall", "verify", "test-ponytail")]
    [string]$Action = "install",

    [Parameter(Position = 1)]
    [string]$Url,

    [ValidateSet("auto", "plugin", "skill")]
    [string]$Kind = "auto",

    [ValidateSet("codex", "claude")]
    [string[]]$Targets = @("codex", "claude"),

    [string]$Name,
    [string]$Marketplace,
    [string]$SkillPath,
    [string]$Ref = "main",
    [switch]$KeepData
)

$ErrorActionPreference = "Stop"

function Say {
    param([string]$Message)
    Write-Host "[butler] $Message"
}

function Die {
    param([string]$Message)
    throw "[butler] $Message"
}

function Invoke-AgentCommand {
    param(
        [Parameter(Mandatory = $true)][string]$File,
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [switch]$AllowFail
    )

    $shownArgs = ($Arguments | ForEach-Object {
        if ($_ -match "\s") { '"' + $_ + '"' } else { $_ }
    }) -join " "

    Say "> $File $shownArgs"
    $output = & $File @Arguments 2>&1
    $code = $LASTEXITCODE
    $text = ($output | Out-String).TrimEnd()

    if ($text) {
        Write-Host $text
    }

    if (-not $AllowFail -and $code -ne 0) {
        Die "command failed with exit code $code"
    }

    [pscustomobject]@{
        Code = $code
        Text = $text
    }
}

function Get-CommandSource {
    param([string]$Command)
    $cmd = Get-Command $Command -ErrorAction SilentlyContinue
    if ($null -eq $cmd) { return $null }
    return $cmd.Source
}

function Get-CodexPath {
    $appServerCodex = Join-Path $env:USERPROFILE ".codex\plugins\.plugin-appserver\codex.exe"
    if (Test-Path -LiteralPath $appServerCodex) {
        return $appServerCodex
    }

    $codex = Get-CommandSource "codex"
    if ($codex) { return $codex }
    return $null
}

function Get-Tools {
    $tools = [ordered]@{
        Codex  = Get-CodexPath
        Claude = Get-CommandSource "claude"
        Python = Get-CommandSource "python"
        Node   = Get-CommandSource "node"
        Git    = Get-CommandSource "git"
    }

    if ($Targets -contains "codex" -and -not $tools.Codex) {
        Die "codex CLI was not found. The butler cannot find the front door."
    }

    if ($Targets -contains "claude" -and -not $tools.Claude) {
        Die "claude CLI was not found. The butler is wearing the wrong badge."
    }

    if ($Kind -ne "skill" -and -not $tools.Node) {
        Die "node is not on PATH. Many plugin hooks need it."
    }

    return [pscustomobject]$tools
}

function ConvertTo-Slug {
    param([string]$Value)
    return (($Value.ToLowerInvariant() -replace "[^a-z0-9_.-]+", "-").Trim("-"))
}

function Parse-GitHubLocation {
    param([string]$Location)

    if ($Location -match "^git@github\.com:([^/]+)/(.+?)(?:\.git)?$") {
        $repoName = $Matches[2] -replace "\.git$", ""
        return [pscustomobject]@{
            Owner = $Matches[1]
            Repo  = $repoName
            OwnerRepo = "$($Matches[1])/$repoName"
            Path  = $null
        }
    }

    try {
        $uri = [Uri]$Location
    }
    catch {
        if ($Location -match "^[^/]+/[^/]+$") {
            $parts = $Location.Split("/")
            $repoName = $parts[1] -replace "\.git$", ""
            return [pscustomobject]@{
                Owner = $parts[0]
                Repo  = $repoName
                OwnerRepo = "$($parts[0])/$repoName"
                Path  = $null
            }
        }

        Die "not a GitHub URL or owner/repo: $Location"
    }

    if ($uri.Host -ne "github.com") {
        Die "only github.com URLs are supported for one-step installs right now"
    }

    $segments = $uri.AbsolutePath.Trim("/").Split("/")
    if ($segments.Count -lt 2) {
        Die "GitHub URL must include owner/repo"
    }

    $owner = $segments[0]
    $repo = $segments[1] -replace "\.git$", ""
    $path = $null

    if ($segments.Count -ge 5 -and $segments[2] -eq "tree") {
        $script:Ref = $segments[3]
        $path = ($segments[4..($segments.Count - 1)] -join "/")
    }

    [pscustomobject]@{
        Owner = $owner
        Repo  = $repo
        OwnerRepo = "$owner/$repo"
        Path  = $path
    }
}

function Get-PluginIdentity {
    param([object]$Location)

    $pluginName = if ($Name) { $Name } else { $Location.Repo }
    $marketplaceName = if ($Marketplace) { $Marketplace } else { ConvertTo-Slug $Location.Repo }

    [pscustomobject]@{
        Plugin = $pluginName
        Marketplace = $marketplaceName
        Selector = "$pluginName@$marketplaceName"
    }
}

function Assert-CodexPlugin {
    param([object]$Tools, [string]$PluginName, [string]$MarketplaceName)
    $list = Invoke-AgentCommand $Tools.Codex @("plugin", "list", "--marketplace", $MarketplaceName)
    $selector = "$PluginName@$MarketplaceName"
    if ($list.Text -notmatch [regex]::Escape($selector) -or $list.Text -notmatch "installed, enabled") {
        Die "Codex does not report $selector as installed and enabled."
    }
    Say "Codex says $selector is installed and enabled."
}

function Assert-ClaudePlugin {
    param([object]$Tools, [string]$PluginName, [string]$MarketplaceName)
    $selector = "$PluginName@$MarketplaceName"
    $list = Invoke-AgentCommand $Tools.Claude @("plugin", "list")
    if ($list.Text -notmatch [regex]::Escape($selector) -or $list.Text -notmatch "enabled") {
        Die "Claude does not report $selector as enabled."
    }
    Invoke-AgentCommand $Tools.Claude @("plugin", "details", $PluginName) | Out-Null
    Say "Claude says $selector is enabled and has readable details."
}

function Install-Plugin {
    param([object]$Tools, [object]$Location)

    $identity = Get-PluginIdentity $Location
    $marketplaceFromCodex = $null

    if ($Targets -contains "codex") {
        $add = Invoke-AgentCommand $Tools.Codex @("plugin", "marketplace", "add", $Location.OwnerRepo, "--json") -AllowFail
        if ($add.Code -eq 0) {
            try {
                $marketplaceFromCodex = ($add.Text | ConvertFrom-Json).marketplaceName
            }
            catch {
                $marketplaceFromCodex = $null
            }
        }
        elseif ($add.Text -notmatch "already|exists|configured") {
            Die "Codex marketplace add failed."
        }

        if ($marketplaceFromCodex) {
            $identity.Marketplace = $marketplaceFromCodex
            $identity.Selector = "$($identity.Plugin)@$($identity.Marketplace)"
        }

        $available = Invoke-AgentCommand $Tools.Codex @("plugin", "list", "--marketplace", $identity.Marketplace)
        if (-not $Name) {
            $pattern = "(?m)^\s*([^\s@]+)@$([regex]::Escape($identity.Marketplace))\s+"
            if ($available.Text -match $pattern) {
                $identity.Plugin = $Matches[1]
                $identity.Selector = "$($identity.Plugin)@$($identity.Marketplace)"
            }
        }

        if ($available.Text -notmatch ([regex]::Escape($identity.Selector) + ".*installed, enabled")) {
            Invoke-AgentCommand $Tools.Codex @("plugin", "add", $identity.Selector, "--json") | Out-Null
        }
        else {
            Say "Codex already has $($identity.Selector). No confetti cannon required."
        }

        Assert-CodexPlugin $Tools $identity.Plugin $identity.Marketplace
    }

    if ($Targets -contains "claude") {
        $addArgs = @("plugin", "marketplace", "add", $Location.OwnerRepo, "--scope", "user")
        $add = Invoke-AgentCommand $Tools.Claude $addArgs -AllowFail
        if ($add.Code -ne 0 -and $add.Text -notmatch "already|exists|configured") {
            Die "Claude marketplace add failed."
        }

        $selector = "$($identity.Plugin)@$($identity.Marketplace)"
        $list = Invoke-AgentCommand $Tools.Claude @("plugin", "list")
        if ($list.Text -notmatch [regex]::Escape($selector)) {
            Invoke-AgentCommand $Tools.Claude @("plugin", "install", $selector, "--scope", "user") | Out-Null
        }
        else {
            Say "Claude already has $selector. The butler polishes the handle anyway."
        }

        Assert-ClaudePlugin $Tools $identity.Plugin $identity.Marketplace
    }

    Say "Plugin install complete. Start a new Claude/Codex session so hooks wake up fresh."
    Say "Codex may still ask you to review/trust hooks in /hooks; that is a safety checkpoint, not a script bug."
}

function Uninstall-Plugin {
    param([object]$Tools, [object]$Location)
    $identity = Get-PluginIdentity $Location

    if ($Targets -contains "codex") {
        Invoke-AgentCommand $Tools.Codex @("plugin", "remove", $identity.Selector, "--json") -AllowFail | Out-Null
        $list = Invoke-AgentCommand $Tools.Codex @("plugin", "list", "--marketplace", $identity.Marketplace) -AllowFail
        if ($list.Text -match ([regex]::Escape($identity.Selector) + ".*installed")) {
            Die "Codex still reports $($identity.Selector) as installed."
        }
        Say "Codex plugin removed or was already absent: $($identity.Selector)"
    }

    if ($Targets -contains "claude") {
        $args = @("plugin", "uninstall", $identity.Selector, "--scope", "user", "-y")
        if ($KeepData) { $args += "--keep-data" }
        Invoke-AgentCommand $Tools.Claude $args -AllowFail | Out-Null
        $list = Invoke-AgentCommand $Tools.Claude @("plugin", "list")
        if ($list.Text -match [regex]::Escape($identity.Selector)) {
            Die "Claude still reports $($identity.Selector) as installed."
        }
        Say "Claude plugin removed or was already absent: $($identity.Selector)"
    }
}

function Get-SkillIdentity {
    param([object]$Location)
    $path = if ($SkillPath) { $SkillPath } else { $Location.Path }
    $skillName = if ($Name) {
        $Name
    }
    elseif ($path) {
        Split-Path $path -Leaf
    }
    else {
        $Location.Repo
    }

    [pscustomobject]@{
        Name = $skillName
        Path = $path
    }
}

function Get-SkillRoot {
    param([string]$Target)
    if ($Target -eq "codex") { return (Join-Path $env:USERPROFILE ".codex\skills") }
    return (Join-Path $env:USERPROFILE ".claude\skills")
}

function Assert-SafeChildPath {
    param([string]$Root, [string]$Child)
    $rootFull = [System.IO.Path]::GetFullPath($Root)
    $childFull = [System.IO.Path]::GetFullPath($Child)
    if (-not $childFull.StartsWith($rootFull + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        Die "refusing to touch path outside skill root: $childFull"
    }
}

function Assert-Skill {
    param([string]$Target, [string]$SkillName)
    $root = Get-SkillRoot $Target
    $skillDir = Join-Path $root $SkillName
    $skillFile = Join-Path $skillDir "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile)) {
        Die "$Target skill verification failed: missing $skillFile"
    }
    Say "$Target skill verified: $skillFile"
}

function Install-Skill {
    param([object]$Tools, [object]$Location)

    if (-not $Tools.Python) {
        Die "python was not found; cannot run the Codex skill installer helper."
    }

    $helper = Join-Path $env:USERPROFILE ".codex\skills\.system\skill-installer\scripts\install-skill-from-github.py"
    if (-not (Test-Path -LiteralPath $helper)) {
        Die "missing skill installer helper: $helper"
    }

    $identity = Get-SkillIdentity $Location

    foreach ($target in $Targets) {
        $root = Get-SkillRoot $target
        New-Item -ItemType Directory -Force -Path $root | Out-Null

        $skillDir = Join-Path $root $identity.Name
        if (Test-Path -LiteralPath $skillDir) {
            Say "$target already has skill $($identity.Name). Skipping install."
            Assert-Skill $target $identity.Name
            continue
        }

        $args = @($helper, "--dest", $root)
        if ($identity.Path) {
            $args += @("--repo", $Location.OwnerRepo, "--path", $identity.Path, "--ref", $Ref)
        }
        else {
            $args += @("--repo", $Location.OwnerRepo, "--path", ".", "--ref", $Ref, "--name", $identity.Name)
        }

        if ($Name) {
            $args += @("--name", $identity.Name)
        }

        Invoke-AgentCommand $Tools.Python $args | Out-Null
        Assert-Skill $target $identity.Name
    }

    Say "Skill install complete. Restart Claude/Codex so the new skill joins the seating chart."
}

function Uninstall-Skill {
    param([object]$Location)
    $identity = Get-SkillIdentity $Location

    foreach ($target in $Targets) {
        $root = Get-SkillRoot $target
        $skillDir = Join-Path $root $identity.Name
        Assert-SafeChildPath $root $skillDir

        if (Test-Path -LiteralPath $skillDir) {
            Remove-Item -LiteralPath $skillDir -Recurse -Force
            Say "$target skill removed: $skillDir"
        }
        else {
            Say "$target skill already absent: $skillDir"
        }
    }
}

function Verify-Skill {
    param([object]$Location)
    $identity = Get-SkillIdentity $Location
    foreach ($target in $Targets) {
        Assert-Skill $target $identity.Name
    }
}

function Test-Ponytail {
    $oldKind = $script:Kind
    $script:Kind = "plugin"
    $tools = Get-Tools
    $script:Kind = $oldKind

    if ($Targets -contains "claude") {
        $details = Invoke-AgentCommand $tools.Claude @("plugin", "details", "ponytail")
        if ($details.Text -notmatch "Skills \(6\)" -or $details.Text -notmatch "Hooks \(2\)") {
            Die "Claude sees Ponytail, but skills/hooks inventory did not match expectations."
        }
        Assert-ClaudePlugin $tools "ponytail" "ponytail"
    }

    if ($Targets -contains "codex") {
        Assert-CodexPlugin $tools "ponytail" "ponytail"
        $manifest = Join-Path $env:USERPROFILE ".codex\plugins\cache\ponytail\ponytail\4.7.0\.codex-plugin\plugin.json"
        if (-not (Test-Path -LiteralPath $manifest)) {
            Die "Codex Ponytail manifest missing: $manifest"
        }
        Say "Codex Ponytail manifest exists: $manifest"
    }

    Say "Ponytail is awake. It is judging abstractions silently."
}

if ($Action -eq "test-ponytail") {
    Test-Ponytail
    exit 0
}

if (-not $Url) {
    Die "-Url is required for $Action."
}

$location = Parse-GitHubLocation $Url
$tools = Get-Tools

if ($Kind -eq "auto") {
    if ($location.Path -or $SkillPath) {
        $Kind = "skill"
    }
    else {
        $Kind = "plugin"
    }
}

switch ($Action) {
    "install" {
        if ($Kind -eq "plugin") { Install-Plugin $tools $location }
        else { Install-Skill $tools $location }
    }
    "uninstall" {
        if ($Kind -eq "plugin") { Uninstall-Plugin $tools $location }
        else { Uninstall-Skill $location }
    }
    "verify" {
        if ($Kind -eq "plugin") {
            $identity = Get-PluginIdentity $location
            if ($Targets -contains "codex") { Assert-CodexPlugin $tools $identity.Plugin $identity.Marketplace }
            if ($Targets -contains "claude") { Assert-ClaudePlugin $tools $identity.Plugin $identity.Marketplace }
        }
        else {
            Verify-Skill $location
        }
    }
}
