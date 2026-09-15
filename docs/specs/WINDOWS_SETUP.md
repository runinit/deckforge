# Windows workstation setup

**Target:** native Windows 11 x64, PowerShell 7, Node 24.x as the chosen project line, Python 3.13.x as the chosen helper line, Git, and installed desktop PowerPoint/Excel/Word. These are project targets; exact installed versions must be recorded. Do not replace managed software or an existing version-manager installation without reviewing it.

**Status:** setup instructions and proposed implementation work. No Windows install, PowerShell run or Office test was performed for this revision. The unchanged starter can build the synthetic PPTX; the native Office worker remains DF-20 work.

## 1. Inventory before installing

Open PowerShell in Windows Terminal as your normal user. Office should be deployed and licensed through the company's normal process; do not reinstall it through this guide.

```powershell
$PSVersionTable
Get-Command node, npm.cmd, py, git, winget -ErrorAction SilentlyContinue
node --version
npm.cmd --version
py -3 --version
git --version
```

A missing executable is a prerequisite to resolve, not a reason to run the rest of an unattended setup script. PowerShell cmdlet error preferences do not automatically turn every native process's nonzero exit into a terminating error; check `$LASTEXITCODE` in setup scripts.

When allowed by company policy, these commands discover/install tools. Review version/source prompts. PowerShell installation and WinGet's exact/version flags are documented by Microsoft. [W15, W17](WINDOWS_SOURCES.md)

```powershell
winget show --id Microsoft.PowerShell --exact --source winget
winget install --id Microsoft.PowerShell --exact --source winget
winget show --id Git.Git --exact --source winget
winget install --id Git.Git --exact --source winget
winget show --id Python.Python.3.13 --exact --source winget
winget install --id Python.Python.3.13 --exact --source winget
winget show --id OpenJS.NodeJS.LTS --exact --source winget --versions
```

Select an approved **24.x** Node version from the returned list instead of assuming a moving LTS alias still resolves to that line:

```powershell
$NodeVersion = Read-Host 'Enter the approved 24.x.y version listed by WinGet'
if ($NodeVersion -notmatch '^24\.\d+\.\d+$') { throw 'Use an explicitly reviewed Node 24.x.y version.' }
winget install --id OpenJS.NodeJS.LTS --exact --source winget --version $NodeVersion
if ($LASTEXITCODE -ne 0) { throw 'Node installation failed; inspect the package/version result.' }
```

Use a fresh terminal after installation so PATH is current. Record the exact tool versions and real `package-lock.json`. Optional Docker Desktop/WSL, pnpm, Bun and GitHub CLI are **not** baseline dependencies. No preview-release installer, global execution-policy change, blanket Unblock-File or administrative Office process is required.

## 2. Extract the complete bundle to a new directory

Download `deckforge-windows-complete.zip` to Downloads. This ZIP contains one `deckforge/` directory. Do not extract over existing source.

```powershell
$SourceRoot = Join-Path $env:USERPROFILE '04_Src'
$Project = Join-Path $SourceRoot 'deckforge'
$Archive = Join-Path $env:USERPROFILE 'Downloads\deckforge-windows-complete.zip'
if (-not (Test-Path -LiteralPath $Archive -PathType Leaf)) { throw 'Download archive is missing.' }
if (Test-Path -LiteralPath $Project) { throw 'Project exists. Extract elsewhere and merge reviewed changes.' }
New-Item -ItemType Directory -Path $SourceRoot -Force | Out-Null
Expand-Archive -LiteralPath $Archive -DestinationPath $SourceRoot
Set-Location -LiteralPath $Project
```

For an existing checkout, use `deckforge-windows-update.zip` in a **staging directory**. It contains the revised Markdown, spec manifest and documentation validator, not an application implementation. Review differences on a Git branch; do not blind-copy over local changes. `docs/specs/` is complete in both ZIPs, including the 33 component specs.

## 3. Establish separate private roots

```powershell
$Lab = Join-Path $env:USERPROFILE '04_Src\deckforge-lab'
$PrivateRoot = Join-Path $env:LOCALAPPDATA 'DeckforgePrivate'
New-Item -ItemType Directory -Path $Lab -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $PrivateRoot 'brands') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $PrivateRoot 'jobs') -Force | Out-Null
Get-Acl -LiteralPath $PrivateRoot | Format-List Owner, Access
```

Verify the private directory is local, not shared with unrelated accounts or automatically published. Set retention, backup and encryption through company policy. A path under LocalAppData is a default location, not a security certification. Corporate template/fonts/voice/customer material stays outside public source.

## 4. Run the unchanged fixture with Windows-safe commands

The package pins PptxGenJS 4.0.0 as the historical fixture dependency, not as the latest version. Use the existing lockfile when it is real and reviewed; otherwise install once and commit the resulting lock.

```powershell
if (Test-Path -LiteralPath '.\package-lock.json') {
    npm.cmd ci
} else {
    npm.cmd install
}
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
node --test .\tests\validate.test.mjs
if ($LASTEXITCODE -ne 0) { throw 'Baseline tests failed.' }
node .\scripts\build-smoke.mjs .\examples\smoke-deck.json .\out\smoke
if ($LASTEXITCODE -ne 0) { throw 'Fixture generation failed.' }
py -3 .\scripts\inspect-pptx.py .\out\smoke\deck.pptx
if ($LASTEXITCODE -ne 0) { throw 'Fixture inspection failed.' }
py -3 .\docs\specs\tools\validate_specs.py
if ($LASTEXITCODE -ne 0) { throw 'Specification integrity check failed.' }
```

Use `npm.cmd` in PowerShell rather than changing script execution policy to run npm.ps1. The explicit test filename also avoids depending on shell glob expansion.

**Important existing limitations:** the legacy `npm run inspect/check/preview` chains invoke `python3`; `preview` invokes LibreOffice/Poppler. They have **not** been silently converted into native Windows/PowerPoint commands. DF-00 must add a tested cross-platform Python launcher, and DF-20 must add the Office worker. Until then, use the explicit commands above and manual Office review below. The old `doctor.py` is a Unix-oriented inventory and does not validate Office installation.

The fixture hardcodes **Liberation Sans**. Confirm it is installed locally or record substitution; do not assume it is an Office font. Do not edit the historical fixture merely to hide a mismatch. DF-00 will add a separately identified Windows-font fixture with an explicitly approved local font while preserving the original regression case. No font binaries are supplied.

## 5. Verify desktop Office manually now

Open PowerPoint, Excel and Word once through the Start menu. Complete normal licensing, first-run and organization-policy prompts yourself. Record PowerPoint’s File → Account/About build and architecture, and equivalent Excel/Word information. Do not paste product keys or tenant identifiers into public reports.

A passive registration inventory can be run without starting Office:

```powershell
'PowerPoint.Application', 'Excel.Application', 'Word.Application' | ForEach-Object {
    $type = [Type]::GetTypeFromProgID($_, $false)
    [pscustomobject]@{ ProgId = $_; Registered = ($null -ne $type) }
}
```

Registration is not activation, licensing or export verification. Installed-font inventory is also only a hint; the application-render test determines the actual result:

```powershell
Add-Type -AssemblyName System.Drawing
$Fonts = New-Object System.Drawing.Text.InstalledFontCollection
try { $Fonts.Families.Name | Sort-Object } finally { $Fonts.Dispose() }
```

Create a throwaway copy and open it in **desktop PowerPoint**, not only a web viewer:

```powershell
$Probe = '.\out\smoke\manual-edit-probe.pptx'
if (Test-Path -LiteralPath $Probe) { throw 'Probe exists; choose a new filename.' }
Copy-Item -LiteralPath '.\out\smoke\deck.pptx' -Destination $Probe
Start-Process -FilePath (Resolve-Path -LiteralPath $Probe).Path
```

In PowerPoint, verify all six slides, edit a heading/table cell, use **Edit Data** on the chart, save, close and reopen. Record any repair/security/font warnings. Export the original generated deck to PDF and/or PNG through PowerPoint’s UI, and review every page. The historical smoke connectors are line primitives; do not expect them to remain anchored when moving a node.

Keep test edits on the probe copy. The original build is not approved simply because the altered probe opens. Record observed checks separately; Windows and Office results begin at NOT_RUN until performed.

## 6. Native Office commands after implementation — TO IMPLEMENT

The following commands do not exist in the unchanged starter:

```text
deck doctor --profile windows-office
deck qa <build-directory> --render powerpoint --profile windows-office
deck office probe <build-directory> --checks save-reopen,chart-data,connectors
deck build <deck.json> --backend powerpoint-template --out <new-build-directory>
deck ingest <source.docx> --engine word-desktop --job <private-job-directory>
deck ingest <source.xlsx> --engine excel-desktop --job <private-job-directory>
```

DF-20 supplies native PNG/PDF export, Office object inspection and safe probe copies; DF-15 supplies template composition; DF-21 supplies Word/Excel input. See [the execution contract](WINDOWS_OFFICE.md). The product remains PowerPoint-first.

## 7. Coding-agent setup without symlink privileges

Copy the thin development skill into the project-scoped host directory you actually use. This does not install the upstream skills or create a finished `/deck` CLI.

```powershell
# Choose '.agents' for Codex or '.claude' for Claude Code.
$AgentFolder = '.agents'
$SkillsRoot = Join-Path $Project ($AgentFolder + '\skills')
$Destination = Join-Path $SkillsRoot 'deckforge'
if (Test-Path -LiteralPath $Destination) { throw 'Skill already exists; inspect before replacing.' }
New-Item -ItemType Directory -Path $SkillsRoot -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $Project 'skills\deckforge') -Destination $Destination -Recurse
```

Record the copy's source digest and refresh deliberately when the tracked skill changes. No Administrator session, symlink privilege or Developer Mode is required for this copy-based path. Consult the prior audit's host references when upgrading host integrations; they were not re-audited in this platform revision.

The Impeccable adapter must select its documented Windows launcher when available. Do not invoke a shell-script entrypoint as though it were a Windows executable. Company brand authority remains above generic style advice.

## 8. Upstream lab and first implementation assignment

Existing acquisition helper, requires network, does not run upstream code:

```powershell
py -3 .\scripts\fetch-upstreams.py --root $Lab --only astra presentation-skill impeccable pptkit
```

Each upstream gets its own environment and an exact source/package lock. Linux-only upstream commands may run in an explicitly separate WSL lab, never as a substitute for native Windows core/Office validation. Presenton remains an optional Docker Desktop experiment with loopback binding and synthetic input; no Office binary, user profile or COM object is exposed to it.

Start DF-00 for Windows bootstrap/portable scripts, then DF-01/DF-02. Implement DF-17's admission/session policy and DF-20's first trusted-fixture render slice early, alongside compiler/visual work. Keep bridge + architecture layers + editorial hero as the first design milestone. Native Office availability should improve evidence and template fidelity, not postpone visual quality.
