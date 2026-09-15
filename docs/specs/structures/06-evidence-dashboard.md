---
spec_id: DF-S06
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03"]
depends_on: ["DF-06", "DF-07", "DF-08", "DF-09"]
---

# DF-S06 — Evidence dashboard and KPI composition

**Goal:** Create a visually strong data-led slide whose metrics and charts remain editable and whose claims remain tied to actual evidence.

**Baseline mapping:** PR-03. **Dependencies:** [DF-06](../core/06-structure-pack-sdk-and-registry.md), [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md), [DF-09](../core/09-native-charts-tables-and-connectors.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own `evidence-dashboard` pack 1.0.0. Variants: `lead-metric` and `analytic-grid`. Do not confuse a decorative gauge or radar illustration with a native data chart.

## 2. File ownership and integration boundary

- `packs/core/evidence-dashboard/`
- `tests/structures/evidence-dashboard/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Content contains 1–4 metric records with ID, label, value/unit, period, evidence IDs and optional comparison baseline. Include 0–2 supported chart references to DeckSpec datasets. A comparison delta needs current and baseline values with matched units/period meaning.

`lead-metric` gives one primary metric a dominant region plus supporting chart or evidence. `analytic-grid` uses aligned regions for several metrics and one/two charts; it is not an arbitrary card grid.

## 4. Requirements


### DF-S06.R01 — Data preservation

Show values/units/timeframes exactly as approved. Rounding and abbreviated units are explicit display formats with originals in source/notes, not changed facts.


### DF-S06.R02 — Metric meaning

Never infer that an increase is good. Delta color/direction follows explicit beneficial-direction metadata and approved brand contrast.


### DF-S06.R03 — Native charts

Use only supported native chart types and editable workbook data. Unsupported chart requests return a capability failure, not a picture fallback.


### DF-S06.R04 — Evidence visibility

Distinguish synthetic, assumption, unverified and supported metrics. Source-display policy controls what is visible; private source paths never appear in notes.


### DF-S06.R05 — Composition

Lead metric creates hierarchy; supporting regions align to a shared grid. Decoration cannot compete with chart axes/labels or imply false numeric area.


### DF-S06.R06 — Density

More than four metrics/two charts proposes a second slide. Chart axes and labels must meet the data-readable policy.


### DF-S06.R07 — Native dashboard evidence

Require PowerPoint plus Excel chart-data probes for declared native charts. Verify metrics, unit labels and caches against frozen datasets after save/reopen; final images retain all source/assumption qualifications.

## 5. Implementation tasks

- [ ] **DF-S06.T01 — Implement lead metric first.** Use a dominant value with unit/period and one evidence-rich chart region.
- [ ] **DF-S06.T02 — Implement analytic grid.** Measure all data labels, legend/axes and callouts before arranging regions.
- [ ] **DF-S06.T03 — Add delta validation.** Check baseline/units/period, division by zero and beneficial direction.
- [ ] **DF-S06.T04 — Add native-data probes.** Compare workbook/cache to source datasets and inspect final renders for axis clipping.

- [ ] **DF-S06.T05 — Exercise the Windows native variants.** Change a synthetic embedded workbook value on a copy; verify chart refresh, direct metric labels and native-data evidence without touching the release candidate.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `METRIC_CONTEXT_MISSING` | Require units/period or an explicit not-applicable value. |
| `DELTA_UNDEFINED` | Do not display an invented result. |
| `CHART_CAPABILITY_REQUIRED` | Fail unsupported native request. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-S06.AC01 | Minimal | One supported metric and no chart. | Strong hierarchy without decorative invented data. |
| DF-S06.AC02 | Normal | Three metrics plus a native bar chart. | Editable metrics and native workbook-backed chart. |
| DF-S06.AC03 | Dense | Four long-label metrics and two charts. | Readable fit or explicit split. |
| DF-S06.AC04 | Bad delta | Baseline is zero for a percentage-change request. | Explicit undefined/change-method warning; no infinity or invented percentage. |
| DF-S06.AC05 | Negative trend | Metric is cost and it rises. | Color meaning follows explicit metadata, not an automatic green up-arrow. |
| DF-S06.AC06 | Data equality | Inspect native chart workbook. | Category/series values equal approved dataset, including zeros/negatives/missing policy. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-S06.AC07 | Native variant edit/save | A chart-data probe edits a value through Excel. | Workbook and visual chart agree after reopening; native editability has evidence beyond a chart count. |
| DF-S06.AC08 | Static export on Windows | Render minimal, normal, dense and long-label fixtures through PowerPoint. | Both variants retain native essentials and readable content; record application/build/font and exact artifact hash. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-S06
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-S06 with native metric text and real charts. Keep value, unit, period and evidence together. No decorative synthetic numbers or screenshot charts.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§8.3, 9; Development plan PR-03, F04–F05. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
