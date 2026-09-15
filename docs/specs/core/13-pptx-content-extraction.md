---
spec_id: DF-13
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-05"]
depends_on: ["DF-12", "DF-17", "DF-20"]
---

# DF-13 — PPTX content extraction and unsupported-object inventory

**Goal:** Extract editable information from existing decks with a precise capability/loss report, without promising lossless reconstruction.

**Baseline mapping:** PR-05. **Dependencies:** [DF-12](12-markdown-intake.md), [DF-17](17-sandbox-security-and-privacy.md), [DF-20](20-windows-native-office-worker.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own PPTX package inspection and extraction to ContentBundle. Separate extraction from reconstructed-theme generation and preserved-template export. Do not render or execute source files in-process, enable macros, or silently flatten unsupported objects.

## 2. File ownership and integration boundary

- `packages/ingest/src/pptx/`
- `packages/ingest/tests/pptx/`
- `tests/fixtures/intake-pptx/`
- `packages/contracts/schemas/pptx-inventory.schema.json`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
extractPptx(input: ApprovedSourceHandle, policy: OfficeIntakePolicy): Promise<PptxExtractionResult>;
```
Return source hash, slide order/IDs, text runs, tables/merges, chart datasets where understood, notes, image references, relationship inventory and an object disposition list: extracted, preserved-reference, unsupported or rejected. Unknown objects remain identifiable by source slide/part/object ID.

## 4. Requirements


### DF-13.R01 — Archive safety

Enforce entry-count, expanded-size, compression-ratio, path and XML restrictions before expensive processing. Reject encrypted/unreadable packages, macros and initial unsupported executable/OLE content according to policy.


### DF-13.R02 — Reading order

Preserve source object identity and group hierarchy. Geometry can inform candidate reading order, but ambiguous ordering must be reported and reviewable.


### DF-13.R03 — Tables and charts

Extract actual cells/series/workbook values when supported; compare chart cache with workbook. Record mismatches rather than choosing an unexplained truth.


### DF-13.R04 — Notes and assets

Preserve speaker notes and slide associations; register embedded media using content hashes. Do not follow external relationships automatically.


### DF-13.R05 — Explicit losses

Inventory SmartArt, animations, embedded objects, unusual charts and unknown shapes. Their presence never becomes a claim that editable reconstruction is supported.


### DF-13.R06 — No roundtrip claim

Output is a content candidate. Rebuilding through DeckSpec may change layout; native template preservation is separately tested in DF-15.


### DF-13.R07 — Native inspection after admission

Keep bounded ZIP/XML extraction first. Use PowerPoint read-only inspection/render only after DF-17 admission and DF-20 session checks; it supplements extraction and never silently repairs an input into acceptance.

### DF-13.R08 — Office input inventory

Record hidden slides, notes, chart workbooks, groups, master/layout roles, unsupported animations/actions and protection status. Native save changes are a separate derived artifact, not a lossless import claim.

## 5. Implementation tasks

- [ ] **DF-13.T01 — Implement package preflight.** Use DF-17 bounded workers and trusted manifest exchange.
- [ ] **DF-13.T02 — Extract simple objects.** Start with native text, images, notes and real tables; preserve source coordinates as extraction metadata only, not public semantic placement.
- [ ] **DF-13.T03 — Extract supported charts.** Read values/labels and cross-check workbook/cache. Add unsupported-type records for all other chart cases.
- [ ] **DF-13.T04 — Build retention inventory.** Compare source counts and content IDs; produce a per-slide reconciliation report for the planner.
- [ ] **DF-13.T05 — Test malformed packages.** Include traversal, entity, decompression, relationship and unsupported-object fixtures.

- [ ] **DF-13.T06 — Reconcile parser and desktop views.** Compare synthetic parsed content against PowerPoint’s object inventory and rendered slides; report unsupported objects, divergent notes or repaired sources instead of guessing missing data.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `OFFICE_INPUT_REJECTED` | Stop extraction with a sanitized reason. |
| `OFFICE_OBJECT_UNSUPPORTED` | Retain an inventory entry and source locator. |
| `CHART_DATA_CONFLICT` | Require source-owner resolution. |
| `EXTRACTION_INCOMPLETE` | Do not mark the candidate content-complete. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-13.AC01 | Plain deck | Extract a synthetic deck containing text, table, bar chart, image and notes. | All understood content and associations are traceable. |
| DF-13.AC02 | Unknown object | Include a SmartArt or unsupported chart object. | Inventory labels it unsupported/preserved-reference; nothing disappears silently. |
| DF-13.AC03 | External relation | Include a remote relationship target. | No network access; relationship recorded and blocked by policy. |
| DF-13.AC04 | Cache conflict | Workbook and chart cache disagree. | Return a data-conflict finding requiring review. |
| DF-13.AC05 | Archive bomb | Supply an archive exceeding configured expansion limits. | Worker rejects/terminates within limits. |
| DF-13.AC06 | Bad ordering | Overlap grouped text with ambiguous reading order. | Flag ambiguity; keep object IDs and original content. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-13.AC07 | Protected source | A supplied deck enters Protected View or requires a password. | Stop for the approved user workflow; do not unblock, enable content or accept repairs automatically. |
| DF-13.AC08 | Chart embedding | A deck contains a macro-free embedded chart workbook and unrelated OLE. | Allow only the separately validated chart-data exception; reject unapproved embedded objects. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-13
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-13 in the sandboxed intake lane. Preserve every unsupported object in the report. Do not describe extraction as lossless import or use source render screenshots as editable reconstruction.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§9, 12; Development plan PR-05, §11 F12. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
