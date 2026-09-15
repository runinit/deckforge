---
spec_id: DF-05
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-02"]
depends_on: ["DF-03", "DF-04"]
---

# DF-05 — Impeccable design-intent adapter

**Goal:** Apply Impeccable’s design reasoning to presentation composition while keeping approved brand rules and Office constraints authoritative.

**Baseline mapping:** PR-02. **Dependencies:** [DF-03](03-brand-capture-and-resolution.md), [DF-04](04-voice-terminology-and-claim-integrity.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own a narrow context/proposal adapter. It reads approved design context and yields validated DesignIntent or a critique. It is not a PPTX renderer, permission to run frontend checks on Office packages, or a concatenation of upstream skill prompts.

## 2. File ownership and integration boundary

- `packages/adapters/impeccable/`
- `skills/deckforge/references/design-direction.md`
- `examples/design-intent/`
- `tests/adapters/impeccable/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
makeDesignBrief(deck: DeckSpec, brand: ResolvedBrand, examples: ApprovedExample[]): DesignBrief;
validateDesignProposal(proposal: unknown, brand: ResolvedBrand): ValidationResult<DesignIntent>;
mapDesignCritique(critique: unknown, slideIds: string[]): DesignFinding[];
```
Use the enumerated fields in CONTRACTS.md: treatment, densityProfile, compositionPreferences, allowedBackgrounds, imageryPolicy, motionPolicy and protectedBrandRules. Do not accept arbitrary numeric “taste scores” with no implementation meaning.

## 4. Requirements


### DF-05.R01 — Context authority

Load only explicitly selected brand/product/design context. Record its digest. Missing context produces a demo/incomplete state, not invented company traits.


### DF-05.R02 — Upstream discipline

Use the pinned reference/version recorded in the upstream register. Remove inherited personal names, machine paths, preferred image models and output defaults from adapted guidance.


### DF-05.R03 — Constrained output

Map suggestions to known structure variants, brand tokens and density profiles. Unknown fields or prohibited typography are rejected before compilation.


### DF-05.R04 — Useful critique

A finding names a slide/content ID, issue, evidence from the render, severity and a proposed constrained change. “Make it more premium” alone is not an actionable repair.


### DF-05.R05 — Budget

One proposal pass and one batched review/confirmation by default. The adapter may recommend a repair but cannot start unbounded polish cycles.


### DF-05.R06 — Offline operation

Existing approved DesignIntent can be compiled without running Impeccable or calling a provider.


### DF-05.R07 — Windows host adapter

Use the upstream Windows launcher where supplied, or an explicitly isolated source-reference path. Do not require Bash, Unix executable bits or hidden author paths on the Windows core runtime.

### DF-05.R08 — Real-artifact critique

Feed PowerPoint-exported images alongside scene previews with provenance labels. Impeccable may propose design changes; it cannot mark native Office editability, template preservation or release checks passed.

## 5. Implementation tasks

- [ ] **DF-05.T01 — Define prompt/context boundary.** Create a short presentation-specific brief with audience, purpose, fixed facts, native-editability policy and protected brand rules.
- [ ] **DF-05.T02 — Implement proposal validation.** Translate only supported suggestions into DesignIntent; capture rejected suggestions and reasons.
- [ ] **DF-05.T03 — Create contrast fixtures.** Use identical content in executive-editorial, technical-diagram and keynote-impact treatments to demonstrate meaningful composition differences.
- [ ] **DF-05.T04 — Integrate critique receipt.** Bind review to the actual render, scene and brand hashes; invalidate it after a visual change.

- [ ] **DF-05.T05 — Exercise the Windows adapter.** Test launcher discovery, paths with spaces and a missing launcher; retain approved font/logo/template rules against conflicting aesthetic suggestions.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `DESIGN_INTENT_INVALID` | Return constrained alternatives or rejected fields. |
| `CONTEXT_UNAPPROVED` | Keep draft-only status. |
| `DESIGN_CONFLICT` | Surface the protected rule instead of weakening it. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-05.AC01 | Brand violation | Proposal replaces the required corporate font because upstream guidance dislikes it. | Rejected with protected rule ID. |
| DF-05.AC02 | Unknown aesthetic field | Proposal includes unsupported `asymmetry: 0.35`. | Schema rejects it rather than treating it as an invisible prompt. |
| DF-05.AC03 | Office false positive | Frontend accessibility checker reports success. | No Office QA gate changes state. |
| DF-05.AC04 | Actionable review | Reviewer reports a clipped label with a slide/content ID. | Mapped to a structured finding, not an uncontrolled code edit. |
| DF-05.AC05 | No provider | Compile using an approved saved intent with no network. | Compilation remains available. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-05.AC06 | Missing Unix shell | Run the design adapter on a Windows host without Bash. | A valid Windows entrypoint is selected or a precise dependency error is returned. |
| DF-05.AC07 | Preview disagreement | SVG is clean but the PowerPoint PNG clips a title. | Native artifact finding remains blocking; aesthetic approval cannot override it. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-05
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-05 as a small input/output adapter around saved context and proposals. Do not fork Impeccable by default, install every skill, or claim its web checks validate PowerPoint.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§5, 6.3, 7, 10; Development plan §5.2. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
