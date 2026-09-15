---
spec_id: DF-10
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03", "PR-07"]
depends_on: ["DF-06", "DF-07"]
---

# DF-10 — SVG/HTML preview, structure gallery and optional motion

**Goal:** Show attractive structure choices using the user’s actual content while distinguishing design previews from final PowerPoint fidelity.

**Baseline mapping:** PR-03, PR-07. **Dependencies:** [DF-06](06-structure-pack-sdk-and-registry.md), [DF-07](07-layout-text-and-scene-compiler.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own scene-to-SVG/HTML projection, preview metadata, variant contact sheets and deterministic static/motion states. Do not build the full review app here, execute original untrusted Astra HTML, or claim preview pixels equal PowerPoint output.

## 2. File ownership and integration boundary

- `packages/preview/src/`
- `packages/preview/tests/`
- `examples/gallery/`
- `tests/fixtures/preview/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
renderScenePreview(scene: ResolvedScene, assets: ResolvedAssetIndex): PreviewBundle;
renderGallery(candidates: CompiledCandidate[], options: GalleryOptions): GalleryBundle;
```
Each candidate displays structure/variant ID, content/scene/brand hashes, native capability warnings and any split proposal. The default is a static SVG with viewBox equal to the scene canvas. Browser motion is an optional projection over that same semantic content.

## 4. Requirements


### DF-10.R01 — Actual content

Compare variants using identical content, brand and canvas. Never improve a candidate score by silently shortening content or substituting a different dataset.


### DF-10.R02 — Preview honesty

Label scene previews as design previews. Show final-PPTX rendered images separately, with backend and renderer versions.


### DF-10.R03 — Offline assets

Resolve images/fonts from approved local assets. No CDN font, image, script or telemetry dependency is allowed in the offline gallery.


### DF-10.R04 — Safe rendering

Escape text, sanitize approved SVG assets and disallow embedded script, foreign object execution, event handlers and uncontrolled URLs. Rendering legacy source HTML requires DF-17 isolation.


### DF-10.R05 — Static first

All values and intended labels are visible in static mode. Freeze final state by explicit static-state rules rather than taking a random animation timestamp.


### DF-10.R06 — Motion contract

Optional reveals respect a reduced-motion/static setting. No PPTX animation translation is promised; native output remains the final static composition or explicitly approved progressive slides.


## 5. Implementation tasks

- [ ] **DF-10.T01 — Project core scene kinds.** Render native text/shapes/edges/image placements and faithful chart/table previews; emit warnings where browser approximation differs.
- [ ] **DF-10.T02 — Implement candidate gallery.** Show source content, variant name, content capacity and editability warnings beside each preview.
- [ ] **DF-10.T03 — Implement static export.** Produce portable HTML/contact sheets with controlled assets and no network dependency.
- [ ] **DF-10.T04 — Add optional motion.** Apply a bounded reveal layer to trusted scene elements; verify static state, screenshots and reduced-motion behavior.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `PREVIEW_ASSET_UNSAFE` | Reject the unsafe asset rather than execute it. |
| `PREVIEW_APPROXIMATION` | Show a warning tied to the element. |
| `STATIC_STATE_INCOMPLETE` | Fail gallery fixture approval. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-10.AC01 | Same facts | Render three candidates for the same comparison. | All contain identical labels/numbers/evidence and disclose any split. |
| DF-10.AC02 | No network | Open gallery with network denied. | No missing essential assets or external requests. |
| DF-10.AC03 | Hidden animation | Render static state for a reveal-based composition. | Every intended label/value is visible. |
| DF-10.AC04 | Script injection | Use text containing script tags and an SVG with an event handler. | Text is escaped and unsafe SVG is rejected/sanitized according to policy. |
| DF-10.AC05 | Different output types | Show scene preview and LibreOffice render together. | The UI identifies which is which; one does not mark the other verified. |
| DF-10.AC06 | Motion disabled | Disable motion and inspect the final frame. | Meaning and full content remain accessible. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-10
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-10 as a read-only scene/gallery renderer. Use original/permitted static assets. Keep actual-PPTX preview separate and do not add a new mutable document model.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§8.2–8.4, 11; Development plan PR-03, PR-07. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
