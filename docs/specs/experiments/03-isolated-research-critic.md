---
spec_id: DF-X3
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-X3"]
depends_on: ["DF-11", "DF-17"]
---

# DF-X3 — Isolated research critic and visual ideation experiment

**Goal:** Check whether an optional PPTAgent/DeepPresenter-style critic improves actionable design review without executing model code or exposing company material.

**Baseline mapping:** PR-X3. **Dependencies:** [DF-11](../core/11-qa-receipts-and-release-gates.md), [DF-17](../core/17-sandbox-security-and-privacy.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own isolated evaluation adapters and measured critic value. No final writer ownership, automatic patches, default customer-data access or agent-code execution. Reassess the selected revision’s security before execution; this spec does not certify a runtime.

## 2. File ownership and integration boundary

- `packages/adapters/research-critic/`
- `tests/experiments/research-critic/`
- `docs/experiments/research-critic/`
- `config/experiments/research-critic.json`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Input: approved synthetic rendered slides, semantic content IDs, intended message and a fixed review rubric. Output: validated DesignFinding[] with slide/element IDs, severity, visual evidence and bounded proposed changes.

The critic cannot return runnable code, modify DeckSpec directly or mark its own proposals approved. Proposal approval and bounded repair stay in DF-11/DF-14.

## 4. Requirements


### DF-X3.R01 — Revision security

Record exact revision/dependencies, review all applicable advisories and patch inclusion before execution. A named historical fix is not general certification.


### DF-X3.R02 — Sandbox

Run without home/credentials/company inputs or uncontrolled network. Give the critic only approved synthetic images/metadata needed for the test.


### DF-X3.R03 — Structured findings

Require specific observable defects or composition improvements with affected IDs. Reject generic aesthetic praise and unverifiable claims as non-actionable.


### DF-X3.R04 — Budget and authority

At most one critic pass plus one confirmation within the shared budget. No independent recursive agent loop or automatic source-code edits.


### DF-X3.R05 — Comparative value

Compare against existing deterministic/Impeccable-style review using fixed defects and blinded reviewer judgments. Measure useful findings, false positives, cost and latency.


### DF-X3.R06 — Optional path

A missing or failed critic never blocks the tested reference workflow; it remains an explicitly optional experiment.


## 5. Implementation tasks

- [ ] **DF-X3.T01 — Review runtime.** Document selected pin, dependency surface and security disposition before launching anything.
- [ ] **DF-X3.T02 — Build inert adapter.** Validate output and map findings; reject code/commands and unknown IDs.
- [ ] **DF-X3.T03 — Create defect set.** Use known clipping, bad hierarchy, weak directional flow and correct-control fixtures.
- [ ] **DF-X3.T04 — Run comparative review.** Record what the critic catches/misses and whether accepted suggestions improve the final render.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `CRITIC_OUTPUT_INVALID` | Reject the proposal. |
| `RESEARCH_RUNTIME_UNAPPROVED` | Do not execute. |
| `CRITIC_BUDGET_EXHAUSTED` | Stop without changing release state. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-X3.AC01 | Code output | Critic returns Python/JavaScript or a shell command as a proposed fix. | Rejected as nonconforming data; never executed. |
| DF-X3.AC02 | Unknown slide | Finding references an ID absent from the input. | Rejected rather than applied to another slide. |
| DF-X3.AC03 | False positive | Show an intentionally valid overlap fixture. | Record incorrect criticism as a false positive. |
| DF-X3.AC04 | Budget exhaustion | Critic requests repeated redesign passes. | Shared repair budget stops the loop. |
| DF-X3.AC05 | No measurable gain | Critic adds cost without useful accepted findings. | Do not promote; keep optional or remove. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-X3
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-X3 only as an isolated synthetic evaluation. Never execute model-produced code or auto-apply changes. Report whether the critic adds measurable value over existing review.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§10–12; source S10 retained in baseline; Development plan PR-X3. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
