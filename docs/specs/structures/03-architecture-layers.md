---
spec_id: DF-S03
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03"]
depends_on: ["DF-06", "DF-07", "DF-08"]
---

# DF-S03 — Layered technical architecture composition

**Goal:** Produce a readable technical architecture with clear planes, boundaries and dependencies while keeping all operational labels editable.

**Baseline mapping:** PR-03. **Dependencies:** [DF-06](../core/06-structure-pack-sdk-and-registry.md), [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own `architecture-layers` pack 1.0.0. Variants: `stacked-planes` and `aligned-columns`. This is a logical architecture illustration, not automatic infrastructure discovery.

## 2. File ownership and integration boundary

- `packs/core/architecture-layers/`
- `tests/structures/architecture-layers/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Content contains 2–5 ordered layers. Each layer has ID, title, 1–4 node records and optional boundary label. Optional explicit relationships reference existing node/layer IDs and declare direction/behavior. Security boundaries are source-declared, not decorative guesses.

`stacked-planes` emphasizes vertical separation. `aligned-columns` aligns homologous components across up to three source-declared categories; absent cells stay absent rather than invented.

## 4. Requirements


### DF-S03.R01 — Hierarchy

Use layer titles and measured node groups with consistent edges/padding. A background stack effect may add depth but must not create false additional planes.


### DF-S03.R02 — Native editability

Layer names, host/service labels, boundaries and meaningful shapes remain native. Optional blueprint texture is decoration without embedded labels.


### DF-S03.R03 — Semantics

Preserve source order and boundary labels. Do not infer trust zones, ownership, high availability or replication from visual adjacency.


### DF-S03.R04 — Density

When nodes/relationships do not fit the technical-readable profile, propose a logical overview plus detail slide with lineage. No omission of difficult nodes.


### DF-S03.R05 — Relationships

All relationship lines map to explicit edges and required capabilities. The base pack can operate without edges; anchored behavior is not inferred from a stack layout.


## 5. Implementation tasks

- [ ] **DF-S03.T01 — Build the second showcase slide.** Start with four clear planes and a few labeled components, using both layouts.
- [ ] **DF-S03.T02 — Add source-declared boundaries.** Show dashed/solid boundary treatments only where semantic data declares them.
- [ ] **DF-S03.T03 — Support dense detail split.** Return overview/detail proposals while preserving IDs and source mapping.
- [ ] **DF-S03.T04 — Audit technical meaning.** Review relationships and boundaries separately from composition quality.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `ARCHITECTURE_DENSITY` | Return overview/detail alternative. |
| `BOUNDARY_UNSUPPORTED` | Surface the unresolved technical meaning. |
| `EDGE_CAPABILITY_REQUIRED` | Fail unsupported behavior explicitly. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-S03.AC01 | Minimal | Two planes with one node each. | Clear hierarchy without unnecessary decorative layers. |
| DF-S03.AC02 | Normal | Four planes with three components each. | Labels remain readable and native. |
| DF-S03.AC03 | Dense | Five planes with long component labels and edge requests. | Alternate/split proposed if needed; no components removed. |
| DF-S03.AC04 | Security label | Input has no trust-zone boundary. | No boundary suggesting a security guarantee is invented. |
| DF-S03.AC05 | Long identifier | Include a long hostname/service path. | Wrap or split follows approved policy; hostname retained exactly. |
| DF-S03.AC06 | Reorder | Change semantic layer order. | Output reflects it while preserving element IDs. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-S03
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-S03 as a technical architecture pack with native labels and explicit boundaries. Preserve the provided architecture rather than inventing infrastructure. Make it one of the first three showcase slides.
```

## 10. Source and decision traceability

This spec decomposes Architecture §8.3; Development plan PR-03. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
