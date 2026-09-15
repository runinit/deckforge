---
spec_id: DF-X1
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-X1"]
depends_on: ["DF-07", "DF-08", "DF-09", "DF-11"]
---

# DF-X1 — PPTKit scene adapter and promotion experiment

**Goal:** Test whether PPTKit improves authoring/layout/export quality while satisfying the same DeckSpec and native-editability contract.

**Baseline mapping:** PR-X1. **Dependencies:** [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md), [DF-09](../core/09-native-charts-tables-and-connectors.md), [DF-11](../core/11-qa-receipts-and-release-gates.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own an explicit subset adapter, pinned experiment environment and comparison report. Acquisition/build experiments can start earlier from the baseline; promotion requires these dependencies. Do not replace DeckSpec with PPTKit IR or implement a universal bidirectional converter.

## 2. File ownership and integration boundary

- `packages/adapters/pptkit/`
- `tests/experiments/pptkit/`
- `docs/experiments/pptkit/`
- `config/experiments/pptkit.json`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Input: the same frozen ResolvedScene/RenderPlan used by the reference backend. Output: a separate ArtifactBundle plus element/capability coverage and comparison report.

Use the baseline recorded source commit `72715ca460ce649f553848393de922c52f19cd34` or a deliberately audited new pin. A separately installed npm package must have its own exact version/lock; do not assume it equals that source commit.

## 4. Requirements


### DF-X1.R01 — Subset adapter

Implement text, shapes, images, notes and data/edge/group features one at a time. Reject unsupported scene fields rather than dropping them.


### DF-X1.R02 — Fidelity evidence

Compare exported PPTX and native objects, not only the toolkit’s SVG preview. Font fit, chart workbooks, tables and anchored edges require independent probes.


### DF-X1.R03 — Reproducibility

Record source/package version, package-manager lock, runtime and fonts. Upstream checks are recorded as executed PASS/FAIL/NOT_RUN, not inferred from documentation.


### DF-X1.R04 — No import promise

Export success does not establish original-template import or arbitrary edit roundtrip. Keep those capabilities unsupported until independently implemented.


### DF-X1.R05 — Promotion rule

Promote only if all mandatory reference fixtures pass and a concrete improvement is recorded in fidelity, implementation complexity, authoring ergonomics or maintenance. A beta label is neither a rejection nor a guarantee.


## 5. Implementation tasks

- [ ] **DF-X1.T01 — Reproduce upstream example.** Run the exact selected package/source build in the external lab and capture environment/results.
- [ ] **DF-X1.T02 — Map core elements.** Implement the smallest scene subset with source-object mappings and explicit unsupported diagnostics.
- [ ] **DF-X1.T03 — Run F01–F09 and F14.** Check actual native data and Office behavior alongside final renders.
- [ ] **DF-X1.T04 — Compare and decide.** Document keep-experimental/promote/fork-fix decision with fixture evidence and bounded upstream patch candidates.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `EXPERIMENT_CAPABILITY_GAP` | Keep the candidate experimental. |
| `EXPERIMENT_PIN_MISMATCH` | Record actual input environment and stop comparison until clarified. |
| `PROMOTION_BLOCKED` | Retain the reference backend. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-X1.AC01 | Field unsupported | Supply a scene feature outside the adapter subset. | Explicit capability failure, not silent omission. |
| DF-X1.AC02 | Chart editability | Export the same data fixture as reference. | Native chart/workbook values match and editing test is recorded separately. |
| DF-X1.AC03 | Preview mismatch | Toolkit SVG differs from exported PPTX. | Report the discrepancy using final output as the Office truth. |
| DF-X1.AC04 | Pin mismatch | Run published package differing from audited source. | Report identifies its actual version, not the source pin. |
| DF-X1.AC05 | Promotion | Compare all mandatory fixtures. | A promotion record names evidence and improvement; any required failure prevents promotion. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-X1
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-X1 in a separate adapter and lab. Keep canonical contracts unchanged. Prove a bounded feature subset and report failures; do not silently swap the default writer.
```

## 10. Source and decision traceability

This spec decomposes Architecture §10; source S04 retained in baseline; Development plan §8.1, PR-X1. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
