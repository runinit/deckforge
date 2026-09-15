---
spec_id: DF-S05
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03"]
depends_on: ["DF-06", "DF-07", "DF-08"]
---

# DF-S05 — Roadmap, phases and swimlanes

**Goal:** Explain migration phases, owners and dependencies without suggesting unsupported dates, durations or progress.

**Baseline mapping:** PR-03. **Dependencies:** [DF-06](../core/06-structure-pack-sdk-and-registry.md), [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own `roadmap-swimlane` pack 1.0.0. Variants: `phase-path` and `owner-swimlanes`. Support ordinal phases and calendar time as distinct modes.

## 2. File ownership and integration boundary

- `packs/core/roadmap-swimlane/`
- `tests/structures/roadmap-swimlane/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Content has a timelineMode of `ordinal` or `calendar`, 2–6 phase records, optional 1–4 lane records and explicit dependencies. Ordinal phases have sequence only. Calendar phases include valid date-only start/end values and a displayed timezone/date policy where relevant.

Native labels/milestones/lanes are required. Decorative winding paths are allowed only in ordinal mode or clearly separated from time-scale semantics. Progress percentages require provided data/evidence.

## 4. Requirements


### DF-S05.R01 — Time truth

An ordinal roadmap must not appear to encode relative duration. In calendar mode, positions reflect the declared date scale and reveal missing dates rather than guess them.


### DF-S05.R02 — Dependencies

Validate endpoint IDs and cycles. Cycles require explicit iterative-process semantics or rejection; do not draw impossible acyclic project flow.


### DF-S05.R03 — Ownership

Use source-declared lane owners. Never infer team responsibilities or commitments from a brand template.


### DF-S05.R04 — Native content

Phase names, dates, owners and milestones are native text/shapes. Dependency anchoring uses explicit capabilities; default static lines are not advertised as attached connectors.


### DF-S05.R05 — Capacity

If six phases or four lanes do not fit approved typography, propose summary/detail continuation with repeated labels and source mapping.


## 5. Implementation tasks

- [ ] **DF-S05.T01 — Implement ordinal phase path.** Use equal phase spacing unless content requires an approved layout alternative; avoid implied dates.
- [ ] **DF-S05.T02 — Implement calendar positioning.** Map dates deterministically to a bounded horizontal range and validate interval ordering.
- [ ] **DF-S05.T03 — Implement lane layout.** Group phase boxes by owner with direct labels and explicit dependencies.
- [ ] **DF-S05.T04 — Test split proposals.** Preserve sequence, milestones and owner labels across summary/detail slides.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `TIMELINE_DATE_INVALID` | Identify phase/date issue. |
| `DEPENDENCY_CYCLE` | Return cycle IDs. |
| `ROADMAP_DENSITY` | Propose summary/detail composition. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-S05.AC01 | Minimal | Two ordinal phases without dates. | No invented calendar or durations. |
| DF-S05.AC02 | Normal | Four phases across three owners. | Readable lanes and correct dependency direction. |
| DF-S05.AC03 | Dense | Six long phases in four lanes. | Readable layout or explicit split, no omission. |
| DF-S05.AC04 | Calendar bounds | Provide end date before start date. | Rejected with phase ID. |
| DF-S05.AC05 | Dependency cycle | Provide A→B→A in an acyclic project mode. | Cycle reported, not hidden. |
| DF-S05.AC06 | Undated milestone | Calendar input has a milestone without date. | Visible incomplete-data diagnostic; no guessed position. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-S05
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-S05 with ordinal/calendar modes separated. Keep dates, ownership and progress factual. Add dependency-cycle and density tests before decorative paths.
```

## 10. Source and decision traceability

This spec decomposes Architecture §8.3; Development plan PR-03. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
