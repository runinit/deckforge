---
spec_id: DF-08
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-01"]
depends_on: ["DF-01", "DF-07"]
---

# DF-08 — Reference PPTX writer and capability negotiation

**Goal:** Export the resolved scene through one explicit PptxGenJS package writer while preserving native editable essentials.

**Baseline mapping:** PR-01. **Dependencies:** [DF-01](01-semantic-contracts-and-migrations.md), [DF-07](07-layout-text-and-scene-compiler.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own backend capability declarations, scene dispatch, units, themes, object identity and final artifact manifests. DF-09 supplies native chart/table/edge handlers. Do not invent per-slide writer mixing or accept arbitrary exporter options from a model.

## 2. File ownership and integration boundary

- `packages/renderer-pptx/src/backend.ts`
- `packages/renderer-pptx/src/text.ts`
- `packages/renderer-pptx/src/shapes.ts`
- `packages/renderer-pptx/src/images.ts`
- `packages/renderer-pptx/tests/`
- `tests/fixtures/export/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed interface:
```ts
interface PptxBackend {
  readonly id: string;
  readonly version: string;
  probe(plan: RenderPlan): CapabilityReport;
  render(plan: RenderPlan, scene: ResolvedScene): Promise<ArtifactBundle>;
}
```
Reference ID is `pptxgenjs`. Rendering writes to a new build directory and returns artifact paths/hashes, source-to-object mappings, backend/package versions and actual capability outcomes. No backend may independently rewrite scene content.

## 4. Requirements


### DF-08.R01 — One writer

RenderPlan selects one final package writer for the complete deck. Multiple composition providers can supply scenes, but foreign PPTX fragments are not silently merged.


### DF-08.R02 — Native essentials

Use native text, supported shapes, tables, charts and notes. Rasterized essential content is forbidden unless the user explicitly changes the contract in an approved new revision.


### DF-08.R03 — Probe before write

Every required capability must be supported with a test fixture reference. Unsupported or unverified native behavior fails before export, not after a partial silent downgrade.


### DF-08.R04 — Coordinate boundary

Convert point geometry to adapter units exactly once. Preserve font sizes and line spacing semantics; do not activate global shrink-to-fit to conceal a compiler defect.


### DF-08.R05 — Object mappings

Write stable semantic object names where supported and keep a sidecar mapping to package object IDs. Record generated IDs without promising they survive every external Office edit.


### DF-08.R06 — Honest branding

A generated theme is a reconstructed theme, not preservation of a corporate master. DF-15 owns original-template preservation claims.


### DF-08.R07 — Writer versus Office validator

Keep pptxgenjs as the reference final writer and PowerPoint as the primary Windows validator. Read-only native rendering is not a second writer; any production Office-save stage is explicitly named and produces a new final artifact with fresh gates.

### DF-08.R08 — No native repair camouflage

Application probes may detect writer gaps but must not add missing groups/connectors or rewrite charts before crediting the reference writer with those capabilities.

## 5. Implementation tasks

- [ ] **DF-08.T01 — Implement adapter shell.** Dispatch validated scene kinds to explicit handlers and reject unknown payloads.
- [ ] **DF-08.T02 — Port simple fixture emission.** Emit cover, bridge, hub and layers through resolved geometry instead of reading the old smoke schema directly.
- [ ] **DF-08.T03 — Define native-feature extension seam.** Add explicit handler registration and fail-closed capability probes. DF-08 is complete with text/shapes/images/notes; data/edge/group capabilities stay unsupported until DF-09 implements and verifies their handlers. Do not create a circular dependency by requiring DF-09 to finish DF-08.
- [ ] **DF-08.T04 — Emit immutable bundle.** Write deck.pptx, source-object-map.json, capability-report.json and build manifest atomically through DF-02.
- [ ] **DF-08.T05 — Add package assertions.** Check notes/text counts, identifiers and absence of unexpected picture substitution; actual visual QA remains DF-11.

- [ ] **DF-08.T06 — Add native artifact mapping.** Expose stable semantic IDs and actual shape/object mappings for DF-20 inspection; preserve native data and notes across observed PowerPoint save/reopen without relying on ZIP byte identity.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `BACKEND_UNSUPPORTED` | List capability IDs and failing slide IDs. |
| `EXPORT_FAILED` | Preserve logs and failed build separately from the last successful artifact. |
| `ARTIFACT_MODIFIED` | Leave existing user file unchanged. |
| `SCENE_INVALID` | Reject before package creation. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-08.AC01 | Editable title | Export and inspect native title text. | The text exists as native content and is editable in a recorded Office probe when available. |
| DF-08.AC02 | Unsupported element | Provide an unrecognized scene element. | Fails with an explicit diagnostic, no omission. |
| DF-08.AC03 | Strict-native chart | Backend probe lacks required native chart capability. | Build fails; no image fallback. |
| DF-08.AC04 | Writer selection | A scene proposes a second final PPTX engine. | RenderPlan validation rejects it. |
| DF-08.AC05 | Corrupt output path | Destination conflicts with a user-modified artifact. | Writer refuses to overwrite it. |
| DF-08.AC06 | Notes | Export notes for every intended slide. | Notes remain associated with the correct slide after reorder. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-08.AC07 | Probe discovers bad edge | PowerPoint inspector sees an unanchored line. | Capability remains unsupported; probe does not silently attach it. |
| DF-08.AC08 | Save changes package | A declared Office finalization saves new bytes. | New hash and re-render/inspection are required before release. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-08
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-08 as a pure scene-to-PPTX adapter. Keep PptxGenJS pin changes separate. Do not add Presenton, PPTKit, arbitrary OOXML merging or direct model-generated JavaScript.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§5–6, 9; Development plan PR-01. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
