# Command availability on Windows

**Platform revision:** windows-office-1. Use PowerShell 7 with native Windows Node/Python. A command described as planned is not installed by this documentation pack. See [Windows setup](WINDOWS_SETUP.md) for guarded extraction, tool installation and manual native checks.

## Available in the unchanged starter

Run from the project root. Each command is independent; stop on a nonzero exit code.

```powershell
node --version
npm.cmd --version
py -3 --version
git --version
npm.cmd install
node --test .\tests\validate.test.mjs
node .\scripts\build-smoke.mjs .\examples\smoke-deck.json .\out\smoke
py -3 .\scripts\inspect-pptx.py .\out\smoke\deck.pptx
py -3 .\docs\specs\tools\validate_specs.py
```

The first successful online dependency installation creates the real lockfile; subsequent installs use `npm.cmd ci`. No Windows install was executed for this revision. The inspector is specific to the six-slide fixture, not a general Office validator. The Node validator test file can execute without Office.

The current `npm run inspect` and `npm run check` scripts call `python3`; `npm run preview` also requires LibreOffice/Poppler. **Those npm chains have not been ported.** Use the explicit commands above for baseline work. DF-00 owns launcher portability; DF-20 owns the future native PowerPoint preview. Do not relabel the existing LibreOffice helper as native Office.

The original fixture requests Liberation Sans. Record availability/substitution before judging native appearance. DF-00 adds a separate approved Windows-font fixture without silently modifying the historical baseline. This pack contains no fonts.

```powershell
py -3 .\scripts\fetch-upstreams.py --help
py -3 .\scripts\start-presenton-lab.py
```

The Presenton helper is print-only without `--start`; actual execution is optional, requires Docker and an explicit operator decision, and remains an external-engine experiment. Its Linux container does not host Office.

## Native checks available manually now

Open the generated PPTX with desktop PowerPoint. Record Office/font versions, render appearance, a heading edit, table edit, chart **Edit Data**, save and reopen on a copy. Preserve the generated original and the user’s own documents. The step-by-step copy/open commands are in [Windows setup](WINDOWS_SETUP.md).

An API registration check does not prove application activation, policy compliance or successful editing. A manual result is an observation with exact file/environment identity, not fabricated machine evidence.

## Proposed product commands: TO IMPLEMENT

These commands are interface contracts for the listed specs. There is no `deck` executable in the current starter.

| Command contract | Owner | Result / gate |
|---|---|---|
| `deck init --job <private-directory>` | DF-02, DF-14 | Root-confined Windows job, immutable revision store |
| `deck doctor --profile windows-office` | DF-00, DF-20 | Environment eligibility and application diagnostics; not automatic acceptance |
| `deck brand capture --inputs <directory> --out <pack>` | DF-03 | Candidate rules and native font/template inventory, pending human approval |
| `deck ingest <file.docx> --engine word-desktop --job <job>` | DF-21 | Admitted read-only document extraction and revision policy |
| `deck ingest <file.xlsx> --engine excel-desktop --job <job>` | DF-21 | Admitted typed data extraction; no refresh/recalculation by default |
| `deck plan --brief <file> --brand <pack> --out <deck.json>` | DF-14 | Reviewable story, evidence and proposed slide structures |
| `deck validate <deck.json>` | DF-01 | Schema, identity and semantic-reference diagnostics |
| `deck gallery --deck <deck.json> --structures bridge,roadmap` | DF-10 | Actual-content alternatives; preview engine identified |
| `deck build <deck.json> --backend pptxgenjs --out <build>` | DF-08, DF-14 | Complete native package; one final writer |
| `deck build <deck.json> --backend powerpoint-template --out <build>` | DF-15, DF-20 | Admitted template composition with PowerPoint as final owner |
| `deck qa <build> --render powerpoint --profile windows-office` | DF-11, DF-20 | Native PNG/PDF, object and edit/save receipts; human checks remain separate |
| `deck office probe <build> --checks save-reopen,chart-data,connectors` | DF-09, DF-20 | Non-destructive probes on copies, per-capability results |
| `deck review <job>` | DF-16 | Story/native-preview/evidence review and targeted revisions |
| `deck export <job> --require-approved` | DF-11, DF-14 | Exact approved artifact and release manifest, or blocked export |
| `npm.cmd run test:spec -- DF-20` | DF-00, DF-20 | Future component dispatcher; not currently an npm script |

`office-free-draft` is an explicitly selected draft profile, not a fallback that fulfills `windows-office`. LibreOffice remains an optional comparison engine. Missing PowerPoint/Excel gates must stay NOT_RUN where required.

## Proposed worker command: TO IMPLEMENT

The future allowlisted worker is started in an attended desktop session. `$RequestFile` and `$ResultFile` must be resolved and validated private job paths, not untrusted shell fragments.

```powershell
& "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -NoLogo -NoProfile -STA -File .\scripts\windows\Invoke-OfficeWorker.ps1 -RequestFile $RequestFile -ResultFile $ResultFile
```

The script is **not supplied**. Do not bypass execution policy, run as SYSTEM, expose it as a web service, or evaluate model-produced PowerShell. The [Office execution contract](WINDOWS_OFFICE.md) governs request schemas, ownership, timeouts and cleanup.

## Result semantics

Exit codes for the proposed public CLI: 0 success; 2 invalid input/revision conflict; 3 unsupported required capability; 4 rendering/QA failure; 5 missing approval/dependency or policy denial. Each native check records PASS, FAIL, WARN or NOT_RUN. Required FAIL/NOT_RUN blocks approved export; a build can remain a draft. Documentation validation uses ordinary 0/1 and never certifies Office behavior.
