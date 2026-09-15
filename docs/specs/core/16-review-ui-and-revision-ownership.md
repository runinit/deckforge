---
spec_id: DF-16
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-07"]
depends_on: ["DF-10", "DF-11", "DF-14"]
---

# DF-16 — Review UI, targeted revisions and manual-edit ownership

**Goal:** Let a non-designer approve the argument, compare real-content visual options, revise one slide and export without learning rendering APIs.

**Baseline mapping:** PR-07. **Dependencies:** [DF-10](10-svg-preview-gallery-and-motion.md), [DF-11](11-qa-receipts-and-release-gates.md), [DF-14](14-director-cli-and-agent-skill.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own the local review surface and user interactions over the canonical job API. Do not create a second mutable deck model, a PowerPoint clone, multi-user collaboration or automatic reconciliation of arbitrary edited PPTX files.

## 2. File ownership and integration boundary

- `apps/review/`
- `packages/director/src/review-api/`
- `tests/review/`
- `docs/review-flows/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Required views: job status; outline/ghost deck; slide preview; variant gallery; evidence/assumptions; QA findings; targeted revision diff; export status.

All mutations submit a structured patch with expected revision. Read-only previews identify whether they are scene SVG or actual PPTX renders and show hash freshness. An export dialog shows recipient scope, remaining NOT_RUN checks and the native/degraded contract.

## 4. Requirements


### DF-16.R01 — Non-designer workflow

Users choose purpose and treatment through real-content previews. Coordinates, library APIs and engine selection are not required UI inputs.


### DF-16.R02 — Canonical state

Keep DeckSpec and DF-02 revisions authoritative. The UI uses shared CLI/director operations; no hidden local state is silently exported.


### DF-16.R03 — Targeted revision

A request such as “make slide 5 clearer” proposes changes only to that slide and disclosed derived slides. Locked claims/notes stay unchanged unless separately approved.


### DF-16.R04 — Freshness

Show changed/stale previews and approvals visibly. Applying a layout or text patch triggers the appropriate receipt invalidation.


### DF-16.R05 — External edits

Detect changed exported PPTX hashes. Offer a new export or controlled re-import; never overwrite Office edits or claim they were automatically synchronized.


### DF-16.R06 — Interaction quality

Support keyboard navigation, readable labels, focus management, empty/error/loading states and side-by-side comparison. Visual polish cannot hide a failed QA gate.


## 5. Implementation tasks

- [ ] **DF-16.T01 — Implement read-only workspace.** Display story, previews, evidence and check states before adding any editing.
- [ ] **DF-16.T02 — Add approved patch actions.** Support text proposal acceptance, variant selection and slide reorder through revision-checked APIs.
- [ ] **DF-16.T03 — Add targeted repair flow.** Show exact before/after content and design changes plus invalidated receipts.
- [ ] **DF-16.T04 — Add export flow.** Distinguish draft from approved release and preserve manually edited output files.
- [ ] **DF-16.T05 — Run task-based pilot.** Ask a consultant to create/revise/export using a frozen synthetic brief without explaining source coordinates.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `REVISION_CONFLICT` | Refresh/rebase the proposed edit without discarding user work. |
| `PREVIEW_STALE` | Do not accept approval for outdated pixels. |
| `RELEASE_BLOCKED` | Show exact failed/missing gates. |
| `EXTERNAL_EDIT_DETECTED` | Preserve the artifact. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-16.AC01 | One-slide revision | Change one slide’s structure. | Other semantic content stays unchanged; dependent previews are refreshed. |
| DF-16.AC02 | Concurrent tab | Two browser tabs edit the same revision. | Second edit receives a visible conflict, no silent last-write-wins. |
| DF-16.AC03 | Stale preview | Modify brand tokens after rendering. | Old preview is visibly stale and cannot be approved as current. |
| DF-16.AC04 | Failed QA | Open export with a critical finding. | Approved release is disabled with a direct remediation link. |
| DF-16.AC05 | External Office edit | Alter the exported PPTX and request regeneration. | User sees protected changed artifact plus explicit new-export/re-import choices. |
| DF-16.AC06 | Keyboard task | Navigate story, variant selection, finding and export via keyboard. | Focus and labels make the complete task operable. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-16
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-16 as a thin job/preview UI. Begin read-only, then add revision-checked actions. Keep DeckSpec authoritative and preserve external PowerPoint edits. Do not start with drag-and-drop freeform layout editing.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§10–11; Development plan PR-07. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
