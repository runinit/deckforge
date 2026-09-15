---
spec_id: DF-S04
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03"]
depends_on: ["DF-06", "DF-07", "DF-08", "DF-09"]
---

# DF-S04 — Comparison matrix and decision scorecard

**Goal:** Communicate option trade-offs using editable native cells and transparent evidence rather than invented rankings.

**Baseline mapping:** PR-03. **Dependencies:** [DF-06](../core/06-structure-pack-sdk-and-registry.md), [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md), [DF-09](../core/09-native-charts-tables-and-connectors.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own `comparison-matrix` pack 1.0.0. Variants: `decision-table` and `paired-scorecard`. Weighted scoring is explicit data behavior, not an automatic recommendation shortcut.

## 2. File ownership and integration boundary

- `packs/core/comparison-matrix/`
- `tests/structures/comparison-matrix/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Content defines 2–4 option IDs, 2–6 criterion IDs and a complete cell matrix. Each cell is a literal fact, approved qualitative rating or explicitly missing value. Optional weights/scores include scale, weight normalization rule, direction and evidence/assumption IDs.

`paired-scorecard` supports exactly two options and is a visually richer native-table treatment. `decision-table` supports all allowed option counts. Missing evidence is labeled unknown, never scored as zero or shown as a positive checkmark.

## 4. Requirements


### DF-S04.R01 — Native cells

Use real PowerPoint table cells for factual data. Header/title/callouts may be separate native text; do not substitute a collection of full-table screenshots.


### DF-S04.R02 — Comparison integrity

Preserve row/column order, units and qualifiers. Distinguish unsupported, not assessed and negative outcomes.


### DF-S04.R03 — Weights

Calculate totals only from explicitly provided valid scales and weights. Display method/assumptions in notes or a visible method label. Do not invent weights to force a preferred option.


### DF-S04.R04 — Visual emphasis

Highlight a recommended option only when an approved recommendation exists. Emphasis cannot hide unfavorable cells or missing evidence.


### DF-S04.R05 — Fit

Use measured columns, repeated headers for continuation, and row lineage. Overflow suggests a detail slide, not type shrink below the data policy.


### DF-S04.R06 — Native matrix editing

Validate actual PowerPoint table cells/merges and theme inheritance for both variants. Numeric score/weight edits remain data changes needing review, not cosmetic operations.

## 5. Implementation tasks

- [ ] **DF-S04.T01 — Implement table layout.** Allocate criterion column and equally/appropriately sized option columns based on approved variant rules.
- [ ] **DF-S04.T02 — Add comparison semantics.** Validate complete cell references and explicit unknown states.
- [ ] **DF-S04.T03 — Add optional scoring.** Implement pure numeric calculation with documented normalization and rounding.
- [ ] **DF-S04.T04 — Add readable continuation.** Paginate criterion rows through compiler split proposals and preserve evidence references.

- [ ] **DF-S04.T05 — Exercise the Windows native variants.** Edit one text cell and one scored cell on separate probe copies; preserve all other values/units, row/column identity and notes.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `MATRIX_INCOMPLETE` | Identify missing option/criterion pair. |
| `SCORING_INVALID` | Reject undefined scales/weights. |
| `TABLE_OVERFLOW` | Return a continuation proposal. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-S04.AC01 | Minimal | Two options and two criteria. | No empty filler rows; editable cells. |
| DF-S04.AC02 | Normal | Three options and five criteria. | Clear scanning and retained qualifiers. |
| DF-S04.AC03 | Dense | Four options with long text in six criteria. | Split proposed if needed; all rows preserved. |
| DF-S04.AC04 | Unknown evidence | Leave one fact unassessed. | Displayed as unknown, not zero or a checkmark. |
| DF-S04.AC05 | Weights | Provide weights not matching declared normalization. | Validation fails or requests explicit normalization approval. |
| DF-S04.AC06 | Manual edit | Change a factual cell in PowerPoint. | Actual table cell is editable; new export does not overwrite manual edits. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-S04.AC07 | Native variant edit/save | A factual table cell is edited and the deck reopened. | The cell is truly editable and persists; weighted totals are not silently recomputed into unsupported claims. |
| DF-S04.AC08 | Static export on Windows | Render minimal, normal, dense and long-label fixtures through PowerPoint. | Both variants retain native essentials and readable content; record application/build/font and exact artifact hash. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-S04
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-S04 with true native tables and explicit unknown/score semantics. Do not generate a favored recommendation or synthetic weights. Add row-continuation tests.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§8.3, 9; Development plan PR-03, F06. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
