---
spec_id: DF-21
status: proposed
implementation_status: not_implemented_by_this_delivery
platform_revision: windows-office-1
primary_platform: windows-native-office
source_prs: ["PR-05"]
depends_on: ["DF-12", "DF-17", "DF-20"]
---

# DF-21 — Native Word and Excel source intake

**Goal:** Use installed Word and Excel to read explicitly selected, admitted source material for a PowerPoint deck.

**Dependencies:** [DF-12](12-markdown-intake.md), [DF-17](17-sandbox-security-and-privacy.md), [DF-20](20-windows-native-office-worker.md).

**Read first:** [shared contracts](../CONTRACTS.md), [Windows execution contract](../WINDOWS_OFFICE.md), [PowerShell setup](../WINDOWS_SETUP.md) and [command availability](../COMMANDS.md). All product behavior in this spec is TO IMPLEMENT; no Office runtime is supplied.

## 1. Scope and non-goals

Use installed Word and Excel to read explicitly selected, admitted source material for a PowerPoint deck.

Preserve document/workbook facts, source locations, qualifications, values and review choices. This is an optional intake extension after the first PowerPoint path; missing Word does not block a deck built from Markdown. Use native applications only through DF-20. Do not generate Word reports or Excel models, accept arbitrary legacy/macro formats, run external refresh, accept tracked changes, recalculate financial results silently, or promise lossless file roundtrip.

## 2. File ownership and integration boundary

- `packages/ingest/src/word-desktop/`
- `packages/ingest/src/excel-desktop/`
- `packages/contracts/schemas/office-source-manifest.schema.json`
- `scripts/windows/OfficeOperations/Extract-Word.ps1 (to implement)`
- `scripts/windows/OfficeOperations/Extract-Excel.ps1 (to implement)`
- `tests/ingest/word/`
- `tests/ingest/excel/`
- `examples/office-intake/ (synthetic fixtures only)`

These are ownership targets, not pre-existing application modules. DF-01 owns shared schemas; DF-20 alone owns COM lifecycle and allowlisted dispatch. Feature adapters cannot create independent Office sessions or reset the global job/repair budget.

## 3. Inputs, outputs and interface

Inputs: immutable admitted .docx/.xlsx, source manifest, explicit selection scope, revision/markup policy for Word, range/table/sheet and value/formula policy for Excel. Optional native reference rendering has its own rights/protection check.

Outputs: extracted-source.json, safe source locators, content/retention report, unsupported-object inventory, original-source hash and Office environment receipt. The director receives normalized semantic records with provenance, not COM objects. Word locators include story/section/paragraph/table-cell identifiers and optional page location bound to a render build; Excel locators include workbook/sheet/table/range coordinates and original cell lexemes/types.

The default is read-only facts/values extraction from selected content. Complex revision and calculation decisions produce reviewable alternatives; they do not silently choose a different source meaning. Open with normal security and explicit read-only behavior. Excel UpdateLinks=0 and read-only options are documented, but data connections/external formulas still require admission policy. W11/W14.

## 4. Requirements

### DF-21.R01 — Explicit scope and admission

Accept only sources explicitly supplied/selected for this job. Preflight ZIP/XML/security/rights before opening Word/Excel through DF-20. No global Documents/OneDrive/email enumeration or inferred confidential sample corpus.

### DF-21.R02 — Word meaning preservation

Extract paragraphs, tables, headings, footnotes/endnotes and supported text containers with an inventory of omissions. Keep quotations, hyperlinks and numeric qualifiers. Do not treat visually positioned text as unstructured filler or silently drop it.

### DF-21.R03 — Word review state

Inventory tracked revisions/comments and identify original/current/proposed text states. Do not accept/reject revisions or export comments into public speaker notes by default. Ambiguous approved wording requires a source-owner decision. W14.

### DF-21.R04 — Excel value fidelity

Preserve sheet/range/table identity, cell types, raw values, display strings, formulas when authorized, number formats, date-system context, units and error/null states. Range.Value2 is not a formatted text extractor; do not turn a date serial or formatted percentage into the wrong fact. W13.

### DF-21.R05 — No hidden workbook calculation

Disable external link update on open and reject unapproved connections/external references. Extract declared cached/current values and mark uncertainty/staleness. Any explicit recalculation is a separate approved operation/copy with environment and before/after diff, never part of silent ingestion.

### DF-21.R06 — Limited embedded data

Do not copy whole sensitive workbooks into a chart simply to preserve one selected range. Build a sanitized minimal chart dataset/workbook from approved values, excluding hidden sheets, comments, formulas/links and unrelated cells unless explicitly required and reviewed.

### DF-21.R07 — Non-destructive native reads

All native operations are read-only or on documented probe/reference-render copies; source hashes must remain unchanged. Do not attach to a user’s active Word document or Excel workbook. Labels/protection and current company policy may block derived exports.

### DF-21.R08 — Traceable comparison

Reconcile normalized output to source selections and object counts, marking unsupported content as unresolved. Native PDF reference export is optional and does not replace semantic extraction. Page locations depend on the recorded font/layout/app environment.

## 5. Implementation tasks

- [ ] **DF-21.T01 — Implement source selection contracts.** Define Word revision/markup and Excel sheet/range/value policies, locator schema and fake extraction fixtures before using Office.
- [ ] **DF-21.T02 — Add Word extraction.** Read admitted documents through DF-20 with explicit revision inventory, heading/table/footnote handling and unsupported-shape report. Prove input and review state are unchanged.
- [ ] **DF-21.T03 — Add Excel extraction.** Read only selected tables/ranges, preserve typed values and formulas/display distinctions, and detect external/hidden content. Reject implicit refresh/recalculation.
- [ ] **DF-21.T04 — Connect provenance and review.** Map approved source spans/datasets to DeckSpec and show retention/ambiguity decisions in the director. Redact source-private paths and review comments from outputs.
- [ ] **DF-21.T05 — Verify source-to-slide fixtures.** Use synthetic Word/Excel files, then explicitly approved private samples on the attended workstation. Record extraction/native render outcomes separately from slide design approval.

## 6. Failure behavior

Return explicit source-review-required for tracked-change ambiguity, formula/value conflicts, missing fonts affecting page locators or stale linked data. Reject unsupported macro/legacy/encrypted content through admission; do not auto-convert it to bypass policy. Missing Word/Excel marks only the selected native-input lane unavailable. Preserve sources and unrelated running Office sessions; do not replace omitted content with model knowledge.

## 7. Acceptance tests

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-21.AC01 | Word qualification | A recommendation has a caveat in a footnote. | Extraction and resulting slide/notes preserve the caveat with source binding. |
| DF-21.AC02 | Tracked deletion | A value is changed through tracked edits. | Both states/review status are represented; no silent acceptance. |
| DF-21.AC03 | Source comments | Reviewer comments contain a client-private note. | Comments stay private and are excluded from public notes by default. |
| DF-21.AC04 | Excel formatting | Selected cells include dates, percentages, nulls and errors. | Raw/display/type semantics reconcile without date/zero/unit corruption. |
| DF-21.AC05 | External workbook link | Workbook depends on an external file or data connection. | No refresh occurs; policy rejects or reports approved stale-value semantics. |
| DF-21.AC06 | Hidden data leak | Workbook includes unrelated hidden sheets and a selected visible chart range. | Only approved range-derived values enter the generated chart workbook. |
| DF-21.AC07 | Locked personal workbook | A personal Excel workbook is already open. | Worker does not attach/alter/close it; an eligible clean session is requested. |
| DF-21.AC08 | Missing Word | Select native Word intake on a host without Word. | Lane is NOT_RUN; existing Markdown/PowerPoint draft operations remain usable. |
| DF-21.AC09 | Read-only source | Extract and optionally render an admitted source. | Original bytes and tracked-review/calculation state are unchanged. |
| DF-21.AC10 | Windows source paths | Use spaces/Unicode names and a rejected junction escape. | Valid local source maps correctly; escape is blocked before opening Office. |

## 8. Verification commands and evidence

Available baseline tests, run separately from native acceptance:

```powershell
node --test .\tests\validate.test.mjs
py -3 .\docs\specs\tools\validate_specs.py
```

**TO IMPLEMENT**, after DF-00 test dispatch and this component's suite exist:

```powershell
npm.cmd run test:spec -- DF-21
```

Unit/mock tests run without Office. Native acceptance runs only on the approved attended Windows profile with admitted fixtures. Record exact commit, request/input hashes, Office/worker/font environment, result and cleanup. An unavailable native test is NOT_RUN; no mock or documentation check substitutes for it.

## 9. Definition of done and handoff

Requirements and acceptance scenarios have explicit evidence, failures preserve user inputs and desktop state, no arbitrary code execution crosses the transport, and original smoke tests remain intact. Release claims bind the exact artifact and environment. New native behavior is not complete merely because a COM ProgID exists.

**Focused coding-agent assignment:**

```text
Implement DF-21 as optional read-only source intake through the existing DF-20 worker. Start with Word revision-aware paragraphs/tables and Excel selected-range values. Keep all qualifiers/types/locators and detect external data. Do not create separate COM sessions, refresh spreadsheets, accept tracked changes or build Word/Excel output renderers.
```

## 10. Source and decision traceability

This spec is added by the user’s Windows/native-Office platform decision. [Windows contract](../WINDOWS_OFFICE.md) supplies common execution and security rules; [Microsoft source register](../WINDOWS_SOURCES.md) distinguishes actual API facts from proposed project behavior. It extends the active [architecture](../references/ARCHITECTURE.md) and [development plan](../references/DEVELOPMENT_PLAN.md). No Windows or Office test result is asserted by this document.
