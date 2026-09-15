# Windows and native Office execution contract

**Revision:** windows-office-1, 2026-09-15. **Authority:** current platform contract for every component spec, replacing the former Linux-first assumptions. All worker/product interfaces below are **TO IMPLEMENT**. The existing starter has no Office worker.

## 1. Target environment and application roles

The initial target is **Windows 11 x64**, with a signed-in, licensed desktop installation of **PowerPoint, Excel and Word**, a company-approved supported Office build, and locally available approved fonts. PowerShell 7 is the developer shell; an explicitly launched Windows PowerShell 5.1 x64 STA process is the first worker-host design. This is a project target, not a claim that a particular edition is installed. Record actual Office edition, executable file version, architecture and update channel when discoverable. Other bitness/ARM64 combinations require their own compatibility profiles.

| Component | Primary responsibility | Out of scope |
|---|---|---|
| Portable TypeScript/Node core | Story, schemas, brand, layout and native OOXML generation | COM or desktop state inside the compiler |
| PowerPoint desktop | Actual-file PNG/PDF rendering, object inspection, save/reopen and editability probes, admitted-template operations | General server-side rendering service; unrestricted scripted editing |
| Excel desktop | Embedded chart workbook probes; optional controlled workbook intake | Unapproved refresh, hidden recalculation, arbitrary workbook automation |
| Word desktop | Optional approved document intake and reference rendering | Word report generation, arbitrary lossless DOCX roundtrip |
| SVG/HTML renderer | Fast structure/design preview and optional web motion | Certification of PowerPoint appearance |
| LibreOffice | Explicit secondary portability comparison | Replacement for a required PowerPoint gate |
| Docker/WSL | Optional isolated parser or external-engine experiments | Hosting desktop Office/COM or sharing a live Office instance |

PowerPoint provides native image/PDF export and chart-workbook access through its object model. [W02–W07](WINDOWS_SOURCES.md). Word/Excel intake is owned by DF-21 and can be added after the PowerPoint-first slice; installing Office does not broaden v0.1 into general Office authoring.

## 2. Workstation execution boundary

One job at a time per signed-in desktop profile. Run the Office worker at normal user privilege in the **interactive session of the operator**. Do not run it as SYSTEM, a Windows service, a non-interactive scheduled task, an unattended web request, a container or a hosted CI worker. PowerShell remoting is not an equivalent desktop session. Microsoft documents the interactive-profile and non-interactive automation limitations. [W01](WINDOWS_SOURCES.md)

A development shell running in WSL may build portable artifacts, but Office operations must be initiated on Windows with Windows-native paths. The baseline uses native Windows Node/Python to avoid cross-filesystem/process ambiguity. Treat a locked/disconnected session, activation prompt or unexpected dialog as `OFFICE_INTERACTION_REQUIRED`; stop the batch for the operator. Do not silently resume because a timeout elapsed.

A **private attended acceptance workstation or VM** may run approved commits against fixtures. It is not an Office service. Public CI runs only the portable/no-Office suites; import workstation receipts for release. Do not execute untrusted pull-request code on a logged-in Office profile.

## 3. Windows storage and process contracts

Use a normal user-writable source directory, a separate upstream lab, and an external private job/brand root. Suggested setup uses `$env:USERPROFILE\04_Src` and `$env:LOCALAPPDATA\DeckforgePrivate`. These locations do not themselves guarantee access control, encryption or backup; validate ACLs and company policy. Do not treat Documents/Desktop as necessarily local: organization redirection or sync may apply.

Office input/output is staged in a short, local, fully hydrated job directory. No direct UNC, WebDAV, device-namespace, cloud-placeholder or `\\wsl$` paths reach COM in the initial implementation. Cloud inputs require explicit hydration/copy, source-hash confirmation and private local staging. No automatic upload/sync/deletion policy changes.

Logical IDs can retain colons; physical filenames cannot be raw IDs. Use reversible manifest mappings or safe hashed filenames. Reject reserved names, alternate data streams, trailing-dot/space aliases and case-folding collisions. Validate reparse points/junctions and final root confinement. Test paths with spaces and Unicode. [W18](WINDOWS_SOURCES.md)

Canonical JSON is UTF-8 without BOM and LF; accept a declared BOM/CRLF input through an explicit parsing normalization, preserving raw-source hashes. PowerShell 5.1 writers must select encoding explicitly. Pass arguments as arrays, never user-derived shell expressions. Atomic replacement is on the same volume with revision checks; handle Windows sharing violations without deleting or overwriting open files.

## 4. Worker transport and operations

DF-20 owns a reviewed allowlisted adapter. The first transport is **one local request file and one result file** launched by a Node parent. No listener, arbitrary expression evaluation, arbitrary COM member name, VBA macro or PowerShell source is accepted from a model. File transport must remain beneath the private job root and bind expected input hashes.

Proposed launch, after implementation only:

```powershell
& "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -NoLogo -NoProfile -STA -File .\scripts\windows\Invoke-OfficeWorker.ps1 -RequestFile $RequestFile -ResultFile $ResultFile
```

The worker is explicit STA; changing the developer shell is not relied on to set its apartment. [W16](WINDOWS_SOURCES.md). Do not add `-ExecutionPolicy Bypass`, change machine-wide policy, enable VBA or lower Trust Center settings. On a managed machine, use an approved/signed script distribution or report the policy blocker.

Initial operations: `doctor`, `render-powerpoint`, `inspect-powerpoint`, `probe-save-reopen`, `probe-chart-data`, `probe-connectors`. `compose-template` is admitted only through DF-15. `extract-word` and `extract-excel` are admitted only through DF-21. The dispatcher rejects every other operation, unknown field or unsupported protocol version.

```ts
interface OfficeRequest {
  protocolVersion: "1.0";
  requestId: string;
  operation: OfficeOperation;
  jobId: string;
  buildId?: string;
  input?: { artifactId: string; relativePath: string; sha256: string };
  outputRelativeDirectory: string;
  parameters: OfficeOperationParameters; // Closed discriminated union, not arbitrary JSON.
  policyDigest: string;
  deadlineMs: number;
}
interface OfficeResult {
  protocolVersion: "1.0";
  requestId: string;
  status: "PASS" | "FAIL" | "WARN" | "NOT_RUN";
  environmentId: string;
  inputSha256?: string;
  artifacts: Array<{ id: string; relativePath: string; sha256: string; mediaType: string }>;
  checks: OfficeCheck[];
  diagnostics: Diagnostic[];
  cleanup: { status: "complete" | "operator-required"; ownedProcessesRemaining: number };
}
```

Normal results never expose customer file paths in public logs. Environment details and raw HRESULT/error text stay private; publish a redacted diagnostic. No operation returns a blanket `officeCompatible: true`.

## 5. Ownership, timeouts and cleanup

The baseline worker must refuse an Office operation when the relevant application is already in use by the operator. A requested `New-Object -ComObject` is **not proof of a fresh isolated process**. Track session/process identity and startup time, opened document identity, and owned references. If ownership cannot be established, return `OFFICE_OWNERSHIP_UNCERTAIN` without calling Application.Quit or changing global settings.

Recheck ownership throughout the job. The operator must not open personal documents in the worker's session during acceptance. A race or new unrelated document causes a pause; shared desktop isolation cannot be proved from a PID snapshot alone. Prefer a dedicated acceptance profile for repeatable probes, with no unrelated files open.

Release child COM references deterministically, close only job-owned documents/workbooks, restore settings changed by the worker, and quit only an exclusively owned application. No blanket `taskkill /IM POWERPNT.EXE`, `Stop-Process -Name EXCEL`, or killing all Office processes. Cleanup failure is recorded, not hidden by a pass result.

The parent enforces a configurable wall-clock deadline and one-job mutex. A timed-out COM call cannot be reliably interrupted inside the same call: cancel the worker safely, leave unknown/shared Office processes alone and request operator cleanup. Retry only explicitly idempotent rejected read operations with a bounded retry count; never blindly retry a mutating save/insert or reset the repair budget. Default project budgets: 180 seconds per small-fixture operation, 600 seconds for an explicitly approved full-deck render, at most three read retries. These are tuneable project defaults, not Office guarantees.

## 6. Admission and security

Parse archives and validate content **before** opening Office. Read-only is not a security sandbox. Initial macro-free allowlist: `.pptx`, approved `.potx`, `.docx` and `.xlsx`. Detect content type/signature mismatch, reject encrypted/password-protected input unless an explicit later workflow handles it, and reject macros, executable actions, ActiveX, external linked objects and unapproved OLE. Native chart `.xlsx` parts are a narrow validated exception to generic embedded-object rejection; scan their package/links/formulas too.

Use `msoAutomationSecurityForceDisable` immediately before programmatic open, preserve/restore the original setting on owned instances, and do not rely on DisplayAlerts to handle security. Excel's security flag does not disable Excel 4.0 macros, so package admission must reject them. [W08, W12](WINDOWS_SOURCES.md)

Do not auto-dismiss Protected View, strip Mark of the Web, bulk-unblock inputs, disable Defender, add trusted locations or disable document-label policy. Mark of the Web is provenance: preserve it or carry its trust decision into staged copies; copying bytes must not silently launder an untrusted source. A blocked or sensitivity-labeled file is referred to its owner through normal approved Office workflow, not opened through a bypass.

DF-17 separates isolated untrusted parsing from the attended Office lane. Stronger isolation requires a company-provisioned disposable Windows VM/user environment with approved licensed Office, not a child process advertised as a sandbox. Exported PNG/PDF/screenshots inherit confidentiality; raster output is not automatically label/encryption protected. Any conversion that cannot enforce required protection is blocked for that recipient scope. Explicit offline policy must account for Office connected experiences/add-ins/cloud fonts as well as model requests; network isolation is configured on the acceptance environment, not assumed from a local COM call.

## 7. Native render, measurements and fixtures

Use `Presentations.Open` on an immutable, admitted staged copy. Render every applicable slide with `Slide.Export(path, "PNG", widthPx, heightPx)` at an aspect-ratio-preserving target (1920×1080 for the 16:9 demo). Generate PDF through `ExportAsFixedFormat` with documented, explicit options. No Poppler dependency is needed for PNGs produced directly by PowerPoint. [W02–W04](WINDOWS_SOURCES.md)

Hidden-slide policy and canonical static-state policy are explicit. PNG/PDF export is a static artifact test, not a slideshow/transition validation. Native animations remain a separate capability; protected data/text cannot disappear from static delivery. All output pages bind slide IDs, input PPTX hash, dimensions, Office executable build, locale, font profile and export settings.

Inspect recursive groups, text frames/runs, notes, tables/cells, charts and relationships. Read TextRange2 bounds in points where supported, compare with frame margins, rotation/wrapping and geometry. BoundHeight alone is not a universal overflow detector, nor does a requested font name prove the exact fallback file used. Unresolved font identity is a diagnostic and fails a font-strict release. [W05](WINDOWS_SOURCES.md)

An optional PowerPoint measurement calibration provider can enrich DF-07's cached font/run metrics. It must not make thousands of per-label COM launches or become a hidden requirement for schema/unit tests. Final application evidence remains independent from compiler estimates.

## 8. Save/reopen and real editability

Probe on throwaway copies. `SaveCopyAs` creates a separate artifact; close/reopen that copy and reconcile essential content, notes, cells, datasets and intended native objects. PowerPoint may rewrite package metadata/IDs; compare semantic/object mappings rather than requiring identical ZIP bytes. [W07](WINDOWS_SOURCES.md)

For chart data, call `ChartData.Activate` before accessing `Workbook`; inspect source cells and, on a probe copy, change a declared test value, save and reopen. Reconcile the changed value, unchanged other cells, chart cache and refreshed chart rendering. Opening a workbook or counting a chart is insufficient. Protect Excel process/workbook ownership throughout. [W06](WINDOWS_SOURCES.md)

For connectors, inspect endpoints and actual connection sites; move a node on a probe copy, save and reopen, and confirm the logical connection is retained. BeginConnect/EndConnect can attach shapes in the object model, but the reference writer may still lack this feature. The probe must not repair its output before claiming that writer supports anchoring. [W09](WINDOWS_SOURCES.md)

Record separately: native rendering, object inspection, save/reopen, chart data edit, connector movement, template behavior, and a human review of the real UI. COM open success is not proof that no repair dialog or warning ever appeared. A witnessed repair warning is a failure; lack of observation is NOT_RUN for that specific check. Human acceptance still covers presentation-scale readability, Edit Data usability, chart/table changes and new-slide layout behavior.

## 9. One final writer and artifact freshness

Default output backend remains `pptxgenjs`. PowerPoint is the primary application validator; opening/exporting it does not make it the package writer. Probe-copy mutations never change the submitted build.

DF-15 may select a separate `powerpoint-template` backend which owns assembly from an admitted template and final PowerPoint save. `pptx-automizer` remains an optional portable template backend with its own profile. Do not silently post-process a PptxGenJS artifact to add missing groups/connectors and then credit the original backend with those capabilities.

If a native-save/normalization stage is deliberately part of production, it is named in the plan. Its saved output is a new final artifact: hash it, re-inspect/re-render it, and bind release receipts to those bytes. An old receipt cannot approve a newer Office save or user edit. Final-byte render is read-only; no unrecorded final save after review.

## 10. Required receipts and degradation

For the default Windows client-handoff release profile, require PowerPoint rendering, package/content checks, save/reopen, human review, and feature-specific chart/table/template/connector evidence when used. Excel is a prerequisite of workbook-edit probes; Word is needed only for native Word intake. A missing application yields NOT_RUN and blocks the relevant required gate; the draft can still be generated.

`office-free-draft` is an explicit portable profile. LibreOffice/SVG results cannot upgrade it to a Windows-approved release. An unavailable optional Word feature does not block a deck with no Word input. Office updates, font changes, locale changes or changed export settings invalidate affected application/visual evidence; do not disable corporate security updates to preserve goldens.

Additional Windows acceptance fixtures W-F01–W-F12 are specified in [implementation order](IMPLEMENTATION_ORDER.md) and [DF-20](core/20-windows-native-office-worker.md). DF-21 adds Word/Excel source fixtures. Every original component retains its IDs and adds platform-specific requirements; there is no second incompatible deck model.
