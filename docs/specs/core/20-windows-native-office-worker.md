---
spec_id: DF-20
status: proposed
implementation_status: not_implemented_by_this_delivery
platform_revision: windows-office-1
primary_platform: windows-native-office
source_prs: ["PR-00", "PR-04"]
depends_on: ["DF-01", "DF-02", "DF-17"]
---

# DF-20 — Windows desktop Office worker and application acceptance

**Goal:** Provide one bounded Windows desktop bridge for native PowerPoint rendering and real Office behavior checks.

**Dependencies:** [DF-01](01-semantic-contracts-and-migrations.md), [DF-02](02-job-store-evidence-and-assets.md), [DF-17](17-sandbox-security-and-privacy.md).

**Read first:** [shared contracts](../CONTRACTS.md), [Windows execution contract](../WINDOWS_OFFICE.md), [PowerShell setup](../WINDOWS_SETUP.md) and [command availability](../COMMANDS.md). All product behavior in this spec is TO IMPLEMENT; no Office runtime is supplied.

## 1. Scope and non-goals

Provide one bounded Windows desktop bridge for native PowerPoint rendering and real Office behavior checks.

Own environment discovery, serial session/COM lifecycle, immutable staged copies, native PNG/PDF export, object inspection, save/reopen and feature probes. The first slice operates only on trusted synthetic fixtures after the platform/security contract exists. DF-15 supplies admitted template composition; DF-21 supplies Word/Excel extraction using this host.

Do not implement a Windows service, unrestricted macro executor, remote Office server, headless Docker renderer, arbitrary PowerPoint editor, automatic prompt-clicker or shared-session process killer. Direct Win32/COM automation is a client-workstation choice, not a scalability plan.

## 2. File ownership and integration boundary

- `packages/office-host/src/`
- `packages/contracts/schemas/office-request.schema.json`
- `packages/contracts/schemas/office-result.schema.json`
- `packages/contracts/schemas/office-environment.schema.json`
- `scripts/windows/Invoke-OfficeWorker.ps1 (to implement)`
- `scripts/windows/OfficeOperations/ (to implement)`
- `tests/office-host/unit/`
- `tests/office-host/native/`
- `docs/office-compatibility/`

These are ownership targets, not pre-existing application modules. DF-01 owns shared schemas; DF-20 alone owns COM lifecycle and allowlisted dispatch. Feature adapters cannot create independent Office sessions or reset the global job/repair budget.

## 3. Inputs, outputs and interface

Use OfficeRequest/OfficeResult from WINDOWS_OFFICE and a closed discriminated operation union. A Node parent validates the request, grants a single local job lease, verifies paths/hashes, and launches a reviewed Windows PowerShell 5.1 x64 STA child with request/result file arguments. The child has no HTTP listener and no model-generated code.

Separate optional passive inventory from explicitly requested application activation. Environment manifest includes OS build/architecture, user-session state, PowerShell/worker versions, Office product/executable builds, update channel when known, locale, export parameters, font profile and policy digest. Registration/version unknowns are reported as unknown, not fabricated.

Artifacts use stable generated filenames mapped to logical slide/object IDs. PNG output comes directly from PowerPoint; PDF is optional additional native reference. Every receipt identifies actual input bytes. COM references never enter JSON. Human review is a separate signed/attributed receipt, not an automatically filled field.

## 4. Requirements

### DF-20.R01 — Interactive session eligibility

Require the interactive signed-in user session at normal privilege, policy-approved scripts and no relevant preexisting Office use. Refuse SYSTEM/non-interactive execution. Application activation, profile configuration and licensing prompts belong to the operator. W01/W16 support the underlying platform constraints.

### DF-20.R02 — Closed protocol

Validate all request fields, operation-specific limits and exact staged-input hash. Accept only registered operations and root-confined file identities. No Invoke-Expression, Run macro, shell string, arbitrary dispatch path or executable code in documents.

### DF-20.R03 — Ownership and serial lifecycle

Acquire one per-profile lease and track owned document/workbook/application identities. New COM activation is not isolation proof. Recheck for unrelated documents; close/release only owned objects and Quit only an exclusively owned instance. Uncertain ownership fails safely.

### DF-20.R04 — Read-only render path

Open admitted immutable staged copies with explicit read-only/window flags. Use Slide.Export at fixed aspect-correct dimensions and ExportAsFixedFormat with explicit options. Record hidden-slide/static-state choice and page coverage. Rendering must not save the input. W02–W04.

### DF-20.R05 — Application geometry

Inspect native text/table/chart/group/edge/notes objects recursively and collect text bounds where supported. Record missing/substituted/unresolved fonts. Keep frame bounds, text bounds and rotated/wrapped text distinct. Return coverage diagnostics for unsupported objects. W05.

### DF-20.R06 — Probe copy discipline

Save/reopen and mutation tests always use separate disposable copies. Compare semantics/object coverage before/after, not raw ZIP identity. Verify source hash remains unchanged and save-copy output can be reopened. W07.

### DF-20.R07 — Feature-specific native checks

Probe table cell edits and merges, group selection, chart workbook activation/value edits and connector movement on copies. Require workbook/cache/render consistency and owned Excel cleanup. Never repair an unanchored reference-writer edge to manufacture support. W06/W09.

### DF-20.R08 — Security on open

Apply DF-17 admission and macro policy before Office; set ForceDisable on owned instances and restore prior state safely. Never auto-dismiss security/repair/label prompts or strip MOTW. Embedded chart workbooks receive their own admission scan. W08/W12.

### DF-20.R09 — Watchdog and errors

Use a parent deadline, cancellation record and bounded retry only for explicitly idempotent reads. Return OFFICE_INTERACTION_REQUIRED/OWNERSHIP_UNCERTAIN/BUSY/TIMEOUT as appropriate. Do not kill unrelated Office apps; cleanup debt prevents a clean completion claim.

### DF-20.R10 — Receipt accuracy

Distinguish render/object/save/feature/human checks. Office build/font changes invalidate relevant results. A repaired/opened file is not proof of no warning; human observation cannot be synthesized. Native result tests begin NOT_RUN until executed.

## 5. Implementation tasks

- [ ] **DF-20.T01 — Implement contracts and mock host.** Create the closed request/result schema, environment/result validation, serial lease, state machine and no-Office mock tests before COM activation.
- [ ] **DF-20.T02 — Add an attended doctor.** Implement passive inventory and explicit launch probe separately. Check session/ownership; record uncertain edition/channel/font details rather than reading unrelated user files.
- [ ] **DF-20.T03 — Export the original fixture.** Implement native read-only PowerPoint PNG/PDF rendering with page mapping, unchanged-input verification, timeout and reference cleanup. Compare the historical and separate Windows-font fixtures.
- [ ] **DF-20.T04 — Add inspect/save probes.** Capture text bounds/native objects/notes; save/reopen a copy and reconcile required content. Keep human no-repair observation separate.
- [ ] **DF-20.T05 — Add data and diagram probes.** Implement chart workbook, table/group and connector-movement operations one by one. Prove user Excel/PowerPoint work is never closed or changed.
- [ ] **DF-20.T06 — Integrate callers and evidence.** Connect DF-11/DF-14/DF-15 through reviewed operations, add redacted receipt import and a documented attended acceptance runbook. Do not export a network service.

## 6. Failure behavior

Map missing/blocked applications to NOT_RUN for unmet prerequisites and a specific diagnostic; missing required gates block release. Report source rejection, unsupported operations and ownership uncertainty before opening a document. A native exception or timeout fails the operation and retains diagnostic metadata plus any partial artifacts as unapproved. No silent fallback to LibreOffice, no blanket taskkill, no user-document overwrite, no globally changed security settings. Process cleanup needing an operator is explicitly recorded.

## 7. Acceptance tests

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-20.AC01 | Read-only native export | Render the six-slide admitted fixture. | Six mapped PNGs and requested PDF exist, input hash is unchanged and only observed checks pass. |
| DF-20.AC02 | No PowerPoint | Execute with PowerPoint unavailable. | Return NOT_RUN/prerequisite diagnostic; approved Windows export blocks. |
| DF-20.AC03 | Non-interactive session | Launch in a service/SYSTEM context. | Refuse before COM activation. |
| DF-20.AC04 | Existing user document | Open a personal unsaved PowerPoint deck first. | Worker refuses the operation and leaves it untouched. |
| DF-20.AC05 | Ownership race | An unrelated document appears after initial ownership check. | Do not Quit or terminate the shared application; report operator action. |
| DF-20.AC06 | Dialog/timeout | A policy or activation dialog blocks an operation. | Deadline/interaction handling stops the job without auto-clicking or killing unrelated processes. |
| DF-20.AC07 | Chart edit persistence | Activate and edit one synthetic chart cell on a copy. | Workbook data, chart cache and native render agree after reopen; original stays unchanged. |
| DF-20.AC08 | Connector movement | Move an attached node on a copy. | Actual anchoring persists or feature gate fails without repairing the reference output. |
| DF-20.AC09 | Font/profile drift | Change a required font or Office build. | Relevant native receipts/calibrations invalidate. |
| DF-20.AC10 | Unsafe file/request | Submit spoofed macro content or an arbitrary operation. | Preflight rejects it before Office; no code runs from input. |
| DF-20.AC11 | Save/reopen identity | SaveCopyAs creates new package bytes. | Probe hashes are separate, semantic comparison records real differences and original remains intact. |
| DF-20.AC12 | Cleanup regression | Run repeated admitted probes, then a controlled failure. | No owned documents leak on normal completion; uncertain processes are reported, never indiscriminately killed. |

## 8. Verification commands and evidence

Available baseline tests, run separately from native acceptance:

```powershell
node --test .\tests\validate.test.mjs
py -3 .\docs\specs\tools\validate_specs.py
```

**TO IMPLEMENT**, after DF-00 test dispatch and this component's suite exist:

```powershell
npm.cmd run test:spec -- DF-20
```

Unit/mock tests run without Office. Native acceptance runs only on the approved attended Windows profile with admitted fixtures. Record exact commit, request/input hashes, Office/worker/font environment, result and cleanup. An unavailable native test is NOT_RUN; no mock or documentation check substitutes for it.

## 9. Definition of done and handoff

Requirements and acceptance scenarios have explicit evidence, failures preserve user inputs and desktop state, no arbitrary code execution crosses the transport, and original smoke tests remain intact. Release claims bind the exact artifact and environment. New native behavior is not complete merely because a COM ProgID exists.

**Focused coding-agent assignment:**

```text
Implement DF-20 in bounded slices. Start with validated request/result files, no-Office mock tests and an attended doctor. Then render the existing trusted smoke PPTX read-only in PowerPoint with hashes and cleanup. Add mutation probes only after ownership tests pass. Do not build a Windows service, bypass Trust Center or claim Windows execution from Linux tests.
```

## 10. Source and decision traceability

This spec is added by the user’s Windows/native-Office platform decision. [Windows contract](../WINDOWS_OFFICE.md) supplies common execution and security rules; [Microsoft source register](../WINDOWS_SOURCES.md) distinguishes actual API facts from proposed project behavior. It extends the active [architecture](../references/ARCHITECTURE.md) and [development plan](../references/DEVELOPMENT_PLAN.md). No Windows or Office test result is asserted by this document.
