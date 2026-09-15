---
spec_id: DF-S08
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03"]
depends_on: ["DF-06", "DF-07", "DF-08"]
---

# DF-S08 — Editorial hero and high-impact thesis composition

**Goal:** Create the high-impact visual slide that makes the system feel designed, while keeping the thesis readable, native and factually controlled.

**Baseline mapping:** PR-03. **Dependencies:** [DF-06](../core/06-structure-pack-sdk-and-registry.md), [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own `editorial-hero` pack 1.0.0. Variants: `type-led` and `image-led`. It can serve a cover, section opener or executive thesis; it does not require an AI-generated image.

## 2. File ownership and integration boundary

- `packs/core/editorial-hero/`
- `tests/structures/editorial-hero/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Content includes a native headline, optional eyebrow/takeaway/attribution, optional approved assetId, and role (`cover`, `section`, `thesis`). Brand-protected logo/disclaimer placements come from resolved policy, not arbitrary content overrides.

`type-led` uses oversized editorial typography, restrained graphic emphasis and deliberate negative space. `image-led` reserves a large approved illustration/photo region with a separate readable text region or tested text-safe overlay.

## 4. Requirements


### DF-S08.R01 — Native thesis

The headline and takeaway are always native text, even when most of the slide is visual. Do not use image generation to draw the factual headline.


### DF-S08.R02 — Readability

Measure line breaks at display sizes and inspect final output. Never crop key words to create a visual effect. Mandatory marks/disclaimers remain visible.


### DF-S08.R03 — Image eligibility

Use only approved local assets with alt text, provenance and crop/focal metadata. External generation is optional, separately authorized and never called by the composer.


### DF-S08.R04 — Brand expression

Apply approved editorial/keynote treatment without replacing corporate identity. Strong scale, asymmetry and composition are allowed within protected rules.


### DF-S08.R05 — Contrast

Text over imagery needs a verified readable zone/treatment. If contrast cannot be established, use a separate text panel or type-led variant.


### DF-S08.R06 — Claims

An unsupported tagline cannot be promoted to an absolute promise to make the opening more dramatic.


### DF-S08.R07 — Native editorial typography

Review the actual PowerPoint hero with approved fonts, crops and aspect ratio. Large type, SVG artwork/transparency and fallback appearance need native renders; Windows display scaling must not hide a cropped heading.

## 5. Implementation tasks

- [ ] **DF-S08.T01 — Build third showcase slide.** Implement type-led hero using actual synthetic deck title and a deliberate two/three-line composition.
- [ ] **DF-S08.T02 — Add image-led variant.** Use an original/permitted local illustration/photo placeholder only when explicitly marked synthetic; require asset eligibility.
- [ ] **DF-S08.T03 — Add crop and contrast checks.** Respect protected image focal regions and keep essential text out of unsafe zones.
- [ ] **DF-S08.T04 — Review impact.** Compare against the baseline title slide with identical content and brand, recording preference reasons and native-editability checks.

- [ ] **DF-S08.T05 — Exercise the Windows native variants.** Probe title edits and figure crop across both variants at fixed native export dimensions; keep critical titles native and respect font/image distribution policy.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `HERO_TEXT_OVERFLOW` | Return permitted line/variant alternatives. |
| `IMAGE_CONTRAST_UNSAFE` | Move text or change composition. |
| `ASSET_NOT_ELIGIBLE` | Do not embed the asset. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-S08.AC01 | Minimal | A short thesis with no image. | Looks intentionally composed, not an empty placeholder. |
| DF-S08.AC02 | Normal | Headline, takeaway, approved mark and image. | Clear hierarchy and all text editable. |
| DF-S08.AC03 | Dense | Long technical title and mandatory disclaimer. | Measured alternative line breaks or type-led variant; no tiny disclaimer or omitted words. |
| DF-S08.AC04 | Busy image | Text-safe region unavailable. | Use separate panel/variant rather than unreadable overlay. |
| DF-S08.AC05 | Missing image | Optional asset cannot be resolved. | Offer type-led composition explicitly; no random network image. |
| DF-S08.AC06 | Strong claim | Proposal changes “can simplify” to “guarantees”. | Claim validation blocks it regardless of visual quality. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-S08.AC07 | Native variant edit/save | The title font is unavailable or substituted in desktop PowerPoint. | Font-strict release blocks until resolved; a scene-only hero preview cannot approve it. |
| DF-S08.AC08 | Static export on Windows | Render minimal, normal, dense and long-label fixtures through PowerPoint. | Both variants retain native essentials and readable content; record application/build/font and exact artifact hash. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-S08
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-S08 as a first-milestone showcase. Make typography and composition distinctive with native text. Use approved imagery only; no need for an image provider to prove visual quality.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§7–8; Development plan PR-03. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
