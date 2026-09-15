---
spec_id: DF-07
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-01", "PR-04"]
depends_on: ["DF-01", "DF-02", "DF-06"]
---

# DF-07 — Layout, font measurement and resolved-scene compiler

**Goal:** Compile semantic compositions into deterministic, measured geometry with readable text and explicit fit failures.

**Baseline mapping:** PR-01, PR-04. **Dependencies:** [DF-01](01-semantic-contracts-and-migrations.md), [DF-02](02-job-store-evidence-and-assets.md), [DF-06](06-structure-pack-sdk-and-registry.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own point-based geometry, actual font resolution, text measurement, region layout, edge routing, collisions and scene generation. Do not alter approved words/data or rely on exporter autofit as the layout algorithm.

## 2. File ownership and integration boundary

- `packages/compiler/src/`
- `packages/compiler/tests/`
- `packages/compiler/fixtures/`
- `packages/contracts/schemas/scene.schema.json`
- `packages/contracts/schemas/render-plan.schema.json`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
compileDeck(input: CompileInput): CompileResult;
measureText(request: TextMeasureRequest, fonts: FontResolver): TextMeasurement;
resolveLayout(draft: LayoutDraft, metrics: MetricsIndex): ResolvedSlide;
planCapabilities(scene: ResolvedScene, backend: BackendDescriptor): RenderPlan;
```
All geometry uses points. Convert only at an adapter boundary. Text measurements contain resolved font/weight hashes, lines/runs, baseline metrics, padding, line spacing and the measurement engine fingerprint. Text content IDs survive segmentation into multiple lines.

## 4. Requirements


### DF-07.R01 — Units

Default demo canvas is 960×540 points; one inch is 72 points. No mixing CSS pixels, EMUs or inches inside the compiler. SVG viewBox uses the scene’s point numbers.


### DF-07.R02 — Actual fonts

Resolve the installed font/weight and record its fingerprint. Missing required faces fail; approved fallback changes the scene/cache key. Do not synthesize a font binary or silently use system defaults.


### DF-07.R03 — Fit policy

Choose an approved variant, allocate regions, wrap measured text and check constraints. Overflow yields an alternate layout or split proposal; shortening protected text requires an approved rewrite.


### DF-07.R04 — Measured text

Handle mixed weight, CJK, punctuation, long unbreakable identifiers, explicit line breaks and padding. Character count is an early content limit, not proof of fitting.


### DF-07.R05 — Collision semantics

Allow only declared containment, decoration and connector contact. Diagnose unintended sibling overlap, clipped critical elements and connector labels crossing unrelated nodes.


### DF-07.R06 — Reproducibility

Cache by content, brand, intent, pack, compiler, metrics and asset hashes. Fixed inputs produce equal canonical scenes; absent metrics cannot be presented as measured.


### DF-07.R07 — PowerPoint text calibration

Keep point-based deterministic compilation. Use a separately cached optional native measurement provider through DF-20 for font/run calibration and actual-file text bounds; do not infer perfect fitting from BoundHeight alone. See W05 in WINDOWS_SOURCES.

### DF-07.R08 — Windows rendering environment

Bind metrics to requested/resolved font evidence, Office build when applicable, locale, DPI/export settings and measurement-provider version. Font or Office changes invalidate only appropriate caches/receipts; no hidden text shrink or content edit is allowed.

## 5. Implementation tasks

- [ ] **DF-07.T01 — Implement metric abstraction.** Start with an explicit provider and fixtures; donor utilities may be ported only after their dependency and fit behavior are tested.
- [ ] **DF-07.T02 — Implement scene primitives.** Support text, shapes, edges, charts, tables and images with stable IDs, z-order and provenance.
- [ ] **DF-07.T03 — Implement bounded solver.** Separate region allocation, measurement, wrap and collision detection; impose candidate/iteration limits and deterministic tie-breaking.
- [ ] **DF-07.T04 — Add semantic retention check.** Require every essential content ID to map to scene content; ensure no data or text is lost during splitting.
- [ ] **DF-07.T05 — Calibrate against exported renders.** Compare the same text fixtures through the reference backend and actual PPTX render; record discrepancies rather than claiming browser metrics guarantee Office fidelity.

- [ ] **DF-07.T06 — Compare measured and native text.** Test Windows fonts, CJK, mixed weight, margins, rotated text and 100/150/200-percent desktop scaling with fixed export dimensions. Record unknown fallback identity instead of claiming a match.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `TEXT_OVERFLOW` | Return offending content/region and permitted next actions. |
| `FONT_UNRESOLVED` | Stop affected scene generation. |
| `GEOMETRY_COLLISION` | Name both elements and intersection type. |
| `CAPABILITY_REQUIRED` | Stop before writing PPTX. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-07.AC01 | Point conversion | Roundtrip a known point box through exporter unit conversion. | Scene remains equal within documented numeric tolerance. |
| DF-07.AC02 | Long technical ID | Render a long hostname without spaces. | A deterministic policy wraps, re-lays out or returns a fit failure; no clipping or hidden deletion. |
| DF-07.AC03 | CJK and weight | Use mixed CJK/Latin text with normal and bold runs. | Metrics reflect resolved fonts; final render discrepancies are flagged. |
| DF-07.AC04 | Approved containment | Place native text within a panel. | No false unintended-overlap failure. |
| DF-07.AC05 | Unintended collision | Place two independent labels in the same region. | A diagnostic names both stable IDs. |
| DF-07.AC06 | Repeat compile | Compile twice with identical inputs and font manifest. | Canonical scene digests match. |
| DF-07.AC07 | Unsupported request | Request anchored connectors from a backend without demonstrated support. | Render plan fails; a plain line is not substituted. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-07.AC08 | Native overflow | Compiler predicts fit but a PowerPoint text frame clips. | The actual-artifact check fails and proposes re-layout/split without deleting words. |
| DF-07.AC09 | Office update | Re-run calibration with a changed Office build. | Affected measurement/application cache keys differ; old receipts are not reused. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-07
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-07 in bounded steps: units, fonts/measurement, scene resolution, then collisions and fit alternatives. Do not modify wording or add a custom animation engine. Preserve semantic IDs and the synthetic baseline.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§6.4–6.5, 9; Development plan PR-01, PR-04. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
