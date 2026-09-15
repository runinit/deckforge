---
spec_id: DF-09
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-01", "PR-04"]
depends_on: ["DF-08"]
---

# DF-09 — Native charts, tables, groups and connector behavior

**Goal:** Make editable data and diagram behavior explicit capabilities rather than assumptions inferred from attractive screenshots.

**Baseline mapping:** PR-01, PR-04. **Dependencies:** [DF-08](08-reference-pptx-writer.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own specialized export handlers and capability probes for charts/workbooks, tables/merges, native grouping and anchored edges. Layout placement remains DF-07. No capability is reported supported merely because a method name exists upstream.

## 2. File ownership and integration boundary

- `packages/renderer-pptx/src/charts.ts`
- `packages/renderer-pptx/src/tables.ts`
- `packages/renderer-pptx/src/edges.ts`
- `packages/renderer-pptx/src/groups.ts`
- `packages/renderer-pptx/tests/native/`
- `tests/fixtures/native/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Initial data contracts support bar, line and pie chart requests; each is enabled only after its own probe. Dataset cells are finite numbers or explicit null; null is not zero. Keep category order, series IDs, units and evidence binding.

Tables carry row/column IDs, literal cell values, headers and validated non-overlapping merge ranges. Edges name semantic endpoint/port IDs plus requested behavior: `native-line` or `anchored`. Group membership is explicit and acyclic.

## 4. Requirements


### DF-09.R01 — Native chart data

Write an editable native chart and embedded workbook with equal values/labels. Inspect cached chart data and workbook cells; test PowerPoint Edit Data separately.


### DF-09.R02 — Correct data semantics

Allow supported negative bar/line values; reject invalid pie values and all-null series. Do not inherit the smoke fixture’s 0–100 limit as a product rule. Axis truncation and normalization require explicit metadata and review.


### DF-09.R03 — Table structure

Keep real cells, headers and merges. Paginate before export with repeated headers and source-row lineage; do not let an exporter create untracked extra slides.


### DF-09.R04 — Formula safety

Treat imported table/chart labels as literal text. Prevent formula-like labels from becoming executable spreadsheet formulas in embedded workbooks.


### DF-09.R05 — Connectors

A visible line is only `connector.native-line`. `connector.anchored` requires real endpoint references and a move/save/reopen test. If not demonstrated, return unsupported rather than advertising anchoring.


### DF-09.R06 — Groups

Declare native grouping only when objects actually form an editable group. Containment in scene geometry is not itself a PowerPoint group.


## 5. Implementation tasks

- [ ] **DF-09.T01 — Create fixture probes.** Build positive and negative chart/table/edge/group fixtures using only synthetic data.
- [ ] **DF-09.T02 — Implement chart handler.** Map supported types, axis policies and datasets; inspect the resulting workbook and cache values.
- [ ] **DF-09.T03 — Implement table handler.** Handle literal strings, row heights, merge validation and approved continuation slides.
- [ ] **DF-09.T04 — Test diagrams in Office.** Move a node, edit a chart value and table cell, ungroup/regroup where supported, save and reopen. Record unavailable checks as NOT_RUN.
- [ ] **DF-09.T05 — Publish capability matrix.** Bind each supported declaration to backend version, fixture hash, environment and test result.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `DATASET_INVALID` | Name the offending cell/series and expected semantics. |
| `TABLE_MERGE_INVALID` | Reject intersecting/out-of-range merges. |
| `ANCHOR_UNVERIFIED` | Block anchored requirement; offer an explicit user-approved native-line change. |
| `NATIVE_DATA_MISMATCH` | Fail content/Office gate. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-09.AC01 | Negative values | Export a bar series containing -5, 0 and 10. | Dataset semantics preserved; no clamp to smoke limits. |
| DF-09.AC02 | Missing data | Export a series with null and zero. | They remain distinct or the capability fails explicitly. |
| DF-09.AC03 | Workbook tampering | Alter one embedded workbook value without changing chart cache. | QA detects the inconsistency. |
| DF-09.AC04 | Unsafe labels | Use a category beginning with `=` or another spreadsheet formula prefix. | It remains literal text and is not a formula. |
| DF-09.AC05 | Overlapping merges | Submit intersecting table merge ranges. | Rejected before export. |
| DF-09.AC06 | Move node | Move an edge endpoint node in PowerPoint, save and reopen. | Anchored capability passes only if the edge stays connected; otherwise unsupported. |
| DF-09.AC07 | Native grouping | Select a declared group in PowerPoint. | Objects behave as a group, or group.native remains unsupported. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-09
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-09 capability by capability. Start with the proven smoke bar/table path, then probe additional chart types and diagram behavior. Do not mark PowerPoint editing tests as passed without application evidence.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§6.5, 9, 11; Development plan §11 F05–F07. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
