---
spec_id: DF-X3
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-X3"]
depends_on: ["DF-11", "DF-17"]
---

# DF-X3 — Isolated research critic and visual ideation experiment

**Goal:** Check whether an optional PPTAgent/DeepPresenter-style critic improves actionable design review without executing model code or exposing company material.

**Baseline mapping:** PR-X3. **Dependencies:** [DF-11](../core/11-qa-receipts-and-release-gates.md), [DF-17](../core/17-sandbox-security-and-privacy.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

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


### DF-X3.R07 — Native-review input and isolation

Give the critic only approved PowerPoint-rendered images and sanitized semantic context through a controlled egress stage. It has no desktop/COM/VBA access and cannot alter files or mark Office checks passed.

## 5. Implementation tasks

- [ ] **DF-X3.T01 — Review runtime.** Document selected pin, dependency surface and security disposition before launching anything.
- [ ] **DF-X3.T02 — Build inert adapter.** Validate output and map findings; reject code/commands and unknown IDs.
- [ ] **DF-X3.T03 — Create defect set.** Use known clipping, bad hierarchy, weak directional flow and correct-control fixtures.
- [ ] **DF-X3.T04 — Run comparative review.** Record what the critic catches/misses and whether accepted suggestions improve the final render.

- [ ] **DF-X3.T05 — Compare bounded Windows critique.** Measure critic findings against the same native artifacts and repair budget as human/baseline review; do not let screenshots leak private paths or source metadata.

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

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-X3.AC06 | Critic emits script | Research output includes PowerShell/VBA instructions. | Treat as unsupported proposed text and reject execution. |
| DF-X3.AC07 | Critic passes broken chart | Aesthetic review passes a chart with uneditable data. | Native feature gate remains failed; the critic cannot override it. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-X3
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

This spec decomposes Architecture §§10–12; source S10 retained in baseline; Development plan PR-X3. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
