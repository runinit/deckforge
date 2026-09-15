---
spec_id: DF-S01
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03"]
depends_on: ["DF-06", "DF-07", "DF-08"]
---

# DF-S01 — Transformation bridge composition

**Goal:** Create a distinctive current → transition → target slide with editable business/technical labels and a strong directional visual.

**Baseline mapping:** PR-03. **Dependencies:** [DF-06](../core/06-structure-pack-sdk-and-registry.md), [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own `transformation-bridge` pack version 1.0.0. Two variants: `elevated-arc` and `split-panel-arrow`. Keep the recognizable bridge concept while re-layout uses presentation-readable labels, not scaled source coordinates.

## 2. File ownership and integration boundary

- `packs/core/transformation-bridge/`
- `tests/structures/transformation-bridge/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed semantic content:
```ts
interface BridgeContent {
  current: { id: string; title: string; items: LabeledItem[] };
  stages: Array<{ id: string; label: string; detail?: string }>;
  target: { id: string; title: string; items: LabeledItem[] };
  outcome?: { id: string; text: string; evidenceIds: string[] };
}
```
Capacity: 1–4 current items, 1–4 target items, 1–3 transition stages. A fourth item is allowed only if measured text passes. No metrics are mandatory. All factual content needs content IDs and appropriate evidence binding.

## 4. Requirements


### DF-S01.R01 — Visual structure

Allocate current and target panels on opposite sides; transition stages occupy the central path. Headline/takeaway remain outside the diagram region. Elevated arc uses a large restrained curve; split-panel uses a stronger horizontal arrow and staggered content.


### DF-S01.R02 — Native contract

All titles, item labels, stages and outcomes are native text. Panels and key direction primitives are native shapes/lines. A decorative arc/glow can be an approved image/SVG but cannot contain essential labels.


### DF-S01.R03 — Fit policy

Use measured content to size symmetric side regions while allowing asymmetric item counts. Do not copy the source’s tiny SVG labels; overflow proposes a variant or split, never hides items.


### DF-S01.R04 — Static state

Final labels and approved values are literal scene content from frame zero in the PPTX/static preview. No zero counters or opacity-zero essential elements.


### DF-S01.R05 — Meaning

Do not invent pain scores, savings, percentages or implied guaranteed outcomes. A transition metaphor does not imply a measured improvement unless evidence supplies it.


### DF-S01.R06 — Source treatment

Record Astra bridge file/commit as visual reference where applicable. Actual copied art/code requires eligibility through DF-18; an original composition may proceed independently.


### DF-S01.R07 — Native bridge fidelity

Render both bridge variants in PowerPoint with long-label/dense fixtures and approved Windows fonts. Keep headings, source/target states and transition labels native; inspect static exports so glow/arc artwork never hides essentials.

## 5. Implementation tasks

- [ ] **DF-S01.T01 — Implement three-slide showcase candidate.** Build the normal bridge first with both variants and the demo brand.
- [ ] **DF-S01.T02 — Define native/decorative layers.** Keep every semantic label separate from art; attach ID-to-element coverage.
- [ ] **DF-S01.T03 — Handle density.** Add minimal, dense and long-label fixtures with expected fit/alternate outcomes.
- [ ] **DF-S01.T04 — Review final output.** Compare real-content gallery and actual-PPTX render at presentation scale; record brand/designer preference separately from package checks.

- [ ] **DF-S01.T05 — Exercise the Windows native variants.** Edit a current-state label and a stage on a throwaway native deck, save/reopen and compare exported spacing; decoration stays separate.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `BRIDGE_CAPACITY` | Return supported variant/split options. |
| `BRIDGE_DIRECTION_UNCLEAR` | Fail visual review pending a specific composition change. |
| `ESSENTIAL_CONTENT_FLATTENED` | Fail native contract. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-S01.AC01 | Minimal | One item per side and one stage. | Intent is clear, whitespace deliberate, text editable. |
| DF-S01.AC02 | Normal | Three items per side and three stages. | Central path reads left-to-right without label collisions. |
| DF-S01.AC03 | Dense | Four long items per side plus outcome. | Either meets approved typography or proposes a split; no shrink below policy. |
| DF-S01.AC04 | Asymmetric | One current item and four target items. | Balanced regions without invented filler. |
| DF-S01.AC05 | Static | Disable scripts/motion. | All required labels and final values remain visible. |
| DF-S01.AC06 | Native audit | Inspect output and change a target label. | Label is a native object; decorative art contains no hidden duplicate data. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-S01.AC07 | Native variant edit/save | A bridge title is changed in PowerPoint and saved. | Text remains editable and readable; the original build and evidence remain unchanged. |
| DF-S01.AC08 | Static export on Windows | Render minimal, normal, dense and long-label fixtures through PowerPoint. | Both variants retain native essentials and readable content; record application/build/font and exact artifact hash. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-S01
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-S01 only with both variants. Use an original/permitted bridge treatment, readable native labels and no source sample metrics. Produce four density fixtures and actual-render evidence.
```

## 10. Source and decision traceability

This spec decomposes Architecture §8, source S02; Development plan PR-03. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
