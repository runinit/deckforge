---
spec_id: DF-06
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-01", "PR-03"]
depends_on: ["DF-01", "DF-02"]
---

# DF-06 — Structure-pack SDK, registry and composition contract

**Goal:** Provide a reusable, testable visual vocabulary where structure, style and content are separate and packs cannot silently change facts or editability.

**Baseline mapping:** PR-01, PR-03. **Dependencies:** [DF-01](01-semantic-contracts-and-migrations.md), [DF-02](02-job-store-evidence-and-assets.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own pack manifests, schema registration, variant selection interfaces, provenance checks and a fixture harness. Individual compositions belong to DF-S01–DF-S08. Untrusted executable pack installation belongs to DF-18 and requires DF-17 policy.

## 2. File ownership and integration boundary

- `packages/structures/src/`
- `packages/structures/tests/`
- `packages/contracts/schemas/structure-manifest.schema.json`
- `packs/core/registry.json`
- `tests/structures/harness/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed pack layout:
```text
packs/core/<structure-id>/
  manifest.json
  content.schema.json
  compose.ts
  styles.json
  static-state.json
  fixtures/{minimal,normal,dense,long-labels}.json
  tests/contract.test.mjs
  PROVENANCE.md
```
`manifest.json` declares pack ID/version, supported DeckSpec version, variant IDs, content limits, required capabilities, license/provenance, known font requirements and a trusted entrypoint. `compose(content, context)` returns a LayoutDraft, never HTML to execute or a completed PPTX.

## 4. Requirements


### DF-06.R01 — Pure composition

For fixed content, brand, intent, fonts and pack version, return equal layout drafts. No network, package installation, file writes, model calls or randomness inside composition.


### DF-06.R02 — Meaning-based selection

Rank candidates against semantic fit, declared content limits and required capabilities before aesthetics. Keep decision reasons in the render plan; do not pick a funnel for arbitrary sequential text only because it looks good.


### DF-06.R03 — Explicit registration

Use exact pack/version IDs from a reviewed registry. Reject collisions, missing schemas, unknown variants and mismatched compiler versions.


### DF-06.R04 — Port provenance

Record upstream commit/file and which code/art was copied, adapted or independently created. Source sample data and author preferences are not default user content.


### DF-06.R05 — Static composition

Every variant has a final presentation-ready state with all intended labels and values. Motion cannot be required to reveal essential meaning.


### DF-06.R06 — Fit outcome

A composer can return FIT, ALTERNATIVE_REQUIRED or SPLIT_PROPOSED with semantic reasons. It must never drop entries or replace native data with artwork to force FIT.


## 5. Implementation tasks

- [ ] **DF-06.T01 — Build manifest loader.** Validate reviewed packs, resolve their content schemas, and freeze registration for a build.
- [ ] **DF-06.T02 — Define LayoutDraft.** Use measured-region requests, semantic element IDs and grouping; shared compiler resolves final positions in DF-07.
- [ ] **DF-06.T03 — Build fixture harness.** Load four mandatory density fixtures for every variant; run schema, identity, content-retention and capability checks.
- [ ] **DF-06.T04 — Add port inventory template.** Capture labels, data, decoration, fonts, external requests, animation state and permitted reuse per source file.
- [ ] **DF-06.T05 — Register first three compositions.** Enable bridge, layers and hero implementations as they arrive; avoid scaffolding empty unsupported entries.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `PACK_CONFLICT` | Reject registration. |
| `STRUCTURE_CONTENT_INVALID` | Return exact content path and variant limit. |
| `LAYOUT_ALTERNATIVE_REQUIRED` | Return supported variant choices. |
| `PACK_UNTRUSTED` | Do not execute the pack. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-06.AC01 | Conflicting ID | Install two different packs claiming the same ID/version. | Registry refuses ambiguity. |
| DF-06.AC02 | Content overflow | Supply one item beyond a variant’s explicit maximum. | Structured alternate/split response; no truncation. |
| DF-06.AC03 | Hidden state | Static-state fixture starts with text opacity zero. | Fixture fails until essential content is visible. |
| DF-06.AC04 | Side effects | A trusted test composer tries a prohibited network or filesystem effect. | The harness flags it; production installation policy does not treat declarative metadata as a sandbox. |
| DF-06.AC05 | Retention | Compose all four density fixtures. | Every required content ID is mapped to native or explicitly permitted decorative scene elements. |
| DF-06.AC06 | Evidence semantics | A conceptual structure contains unapproved sample metrics. | Fixture/pack validation rejects inherited facts. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-06
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-06 registry and fixture harness. Define the LayoutDraft boundary before individual structures. Do not create an HTML-to-PPTX converter or dynamically execute arbitrary downloaded packs.
```

## 10. Source and decision traceability

This spec decomposes Architecture §8; Development plan PR-03. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
