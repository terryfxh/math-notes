# Migrate the blog repo out of OneDrive to a local, non-synced path.
# Safe by design: COPIES everything, never deletes the original.
# Usage (PowerShell):
#   cd "C:\Users\Terry\OneDrive\文档\Claude\Projects\Start a tech blog"
#   powershell -ExecutionPolicy Bypass -File tools\migrate-out-of-onedrive.ps1
#   # or with a custom destination:
#   powershell -ExecutionPolicy Bypass -File tools\migrate-out-of-onedrive.ps1 -Dest "D:\blog\math-notes"

param([string]$Dest = "E:\blog\math-notes")

$ErrorActionPreference = "Stop"
$Src = Split-Path -Parent $PSScriptRoot   # repo root (this script lives in tools/)

Write-Host "Source     : $Src"
Write-Host "Destination: $Dest"
Write-Host ""

# 0. Strongly recommend pausing OneDrive first so the copy reads stable files.
Write-Host "STEP 0  Make sure OneDrive is PAUSED (tray icon -> Pause syncing -> 2 hours)." -ForegroundColor Yellow
Read-Host  "        Press Enter when OneDrive is paused"

# 1. Clear a stale git lock if present (0-byte leftover blocks all git writes).
$lock = Join-Path $Src ".git\index.lock"
if (Test-Path $lock) {
    Remove-Item $lock -Force
    Write-Host "STEP 1  Removed stale .git\index.lock"
} else {
    Write-Host "STEP 1  No stale index.lock - good"
}

# 2. Copy everything except disposable build output.
#    /E recurse, /R:2 /W:2 quick retries, exit codes >= 8 mean failure.
Write-Host "STEP 2  Copying repo (excluding _site and .quarto)..."
robocopy $Src $Dest /E /XD "$Src\_site" "$Src\.quarto" /R:2 /W:2 /NFL /NDL /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }
Write-Host "        Copy complete (robocopy code $LASTEXITCODE)"

# 3. Verify the copied repo's integrity.
Write-Host "STEP 3  Verifying git integrity in the new location..."
Push-Location $Dest
git fsck --full
if ($LASTEXITCODE -ne 0) { Pop-Location; throw "git fsck reported problems - do NOT delete the original yet" }
git status --short
Pop-Location

Write-Host ""
Write-Host "DONE. Next steps:" -ForegroundColor Green
Write-Host "  1. In the Claude app, open this project's folder settings and replace"
Write-Host "     the old folder with: $Dest"
Write-Host "  2. Work from $Dest from now on (git, quarto preview, everything)."
Write-Host "  3. After a few days of trouble-free use, rename the old OneDrive copy to"
Write-Host "     'Start a tech blog (archived)' or delete it. Do NOT keep both active."
Write-Host "  4. Resume OneDrive syncing."
