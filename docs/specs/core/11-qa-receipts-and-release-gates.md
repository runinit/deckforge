---
spec_id: DF-11
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-04"]
depends_on: ["DF-02", "DF-08", "DF-09", "DF-20"]
---

# DF-11 — QA, review receipts and bounded repair

**Goal:** Prove content, design, native structure and Office behavior separately, and block release when required evidence is absent or stale.

**Baseline mapping:** PR-04. **Dependencies:** [DF-02](02-job-store-evidence-and-assets.md), [DF-08](08-reference-pptx-writer.md), [DF-09](09-native-charts-tables-and-connectors.md), [DF-20](20-windows-native-office-worker.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own QA aggregation, receipt validity, final-artifact inspection, render orchestration and repair budgeting. Individual geometry calculations remain DF-07. Untrusted rendering must use DF-17; trusted synthetic baseline rendering can use the existing helper.

## 2. File ownership and integration boundary

- `packages/qa/src/`
- `packages/qa/tests/`
- `packages/contracts/schemas/qa-receipt.schema.json`
- `packages/contracts/schemas/release-manifest.schema.json`
- `tests/fixtures/qa/`
- `docs/review-protocols/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
runChecks(build: BuildManifest, policy: ReleasePolicy): Promise<QaReport>;
validateReceipt(receipt: ReviewReceipt, current: BuildIdentity): ReceiptValidity;
canRelease(job: JobSnapshot, report: QaReport, policy: ReleasePolicy): ReleaseDecision;
```
Every check yields PASS, FAIL, WARN or NOT_RUN. A receipt binds reviewer/tool identity, scope, exact dependency hashes, timestamp and result. Machine checks, human design review and Microsoft PowerPoint edit/save review are different check classes.

## 4. Requirements


### DF-11.R01 — No green skipping

Unavailable tools or missing manual review are NOT_RUN. Draft generation may succeed, but an approved client release fails if a required gate is NOT_RUN.


### DF-11.R02 — Content QA

Verify content-ID coverage, numeric equality, evidence states, qualifiers, protected text and speaker notes. A screenshot match alone cannot prove factual preservation.


### DF-11.R03 — Package QA

Resolve package relationships, chart/cache/workbook data, notes, tables, media and forbidden external/executable objects. Distinguish the original six-slide inspector from this general validator.


### DF-11.R04 — Final render

Inspect the actual exported PPTX through an identified renderer. Record application/version, fonts and output digest. Browser scene previews do not satisfy this requirement.


### DF-11.R05 — Scoped invalidation

Content edits invalidate story/content and downstream receipts. Layout/font edits invalidate visual/geometry/Office-render receipts. Renderer upgrades invalidate package/Office evidence. Receipt validity follows explicit dependency hashes.


### DF-11.R06 — Bounded repair

Default to one initial render, one batched approved repair and one confirmation render. Do not restart a failed loop under a new name. Further work requires a recorded budget change and blocker.


### DF-11.R07 — Final authority

Only a release transaction can set RELEASED after all required valid receipts pass. Writing a PPTX never grants release approval.


### DF-11.R08 — Windows release profile

Default client-handoff uses windows-office: required native render, save/reopen and relevant editability receipts plus human review. Missing PowerPoint is NOT_RUN and blocks approved release; LibreOffice cannot fill the native gate.

### DF-11.R09 — Granular application evidence

Store native render, object inspection, save/reopen, chart-data edit, table/group/connector/template behavior and witnessed repair-warning checks separately. COM-open success alone is not repair-dialog certification.

### DF-11.R10 — Exact final bytes

Bind every native receipt to input/final artifact hash, worker protocol/build, Office executable version, font profile, locale, export settings and required feature set. Probe mutations never replace the final file.

## 5. Implementation tasks

- [ ] **DF-11.T01 — Implement report schema.** Create named gate IDs, severity, check status, scope, artifacts and remediation pointers.
- [ ] **DF-11.T02 — Add structural/content validators.** Generalize beyond fixed smoke counts and verify graph relationships and embedded data.
- [ ] **DF-11.T03 — Implement receipt dependency graph.** Calculate current signatures and reject stale approvals even when a filename is unchanged.
- [ ] **DF-11.T04 — Integrate actual rendering.** Run in a disposable work directory with timeouts; use DF-17 for non-synthetic inputs.
- [ ] **DF-11.T05 — Implement bounded repair.** Collect findings in one batch, propose constrained fixes, apply approved patches and rerun affected checks without hiding remaining failures.

- [ ] **DF-11.T06 — Integrate DF-20 receipts.** Add environment mismatch, activation/dialog, Excel missing, human check missing and final-save invalidation paths. Keep the global one-repair budget shared across compiler, Office and reviewer.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `QA_FAILED` | Block approved release and return actionable findings. |
| `RECEIPT_STALE` | Request only affected rechecks, not blanket approval reuse. |
| `REVIEW_NOT_RUN` | Keep explicit unverified state. |
| `REPAIR_BUDGET_EXHAUSTED` | Stop at NEEDS_FIX. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-11.AC01 | Missing PowerPoint | Run all automated checks with no application review. | Required native render/edit and human gates remain NOT_RUN; windows-office approved release is blocked. |
| DF-11.AC02 | Stale approval | Change a chart value after a review receipt. | Receipt becomes stale and release fails. |
| DF-11.AC03 | Corrupt package | Remove a chart workbook or break an internal relationship. | Office package check fails with the part/relationship ID. |
| DF-11.AC04 | Layout false positive | Place text intentionally within its panel. | Geometry rules do not fail valid containment. |
| DF-11.AC05 | Repair budget | Find defects after the confirming render. | Stop at NEEDS_FIX and report the remaining slide IDs. |
| DF-11.AC06 | Rendering disagreement | SVG looks correct but final PPTX clips text. | Final-artifact failure takes precedence; no release. |
| DF-11.AC07 | Manual review evidence | Record an Office edit/save receipt. | Requires application/version, artifact digest, tested behaviors and reviewer identity. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-11.AC08 | Office unavailable | Windows profile is selected but desktop PowerPoint is missing. | Draft builds may succeed; native checks are NOT_RUN and approved export is denied. |
| DF-11.AC09 | Unwitnessed warning state | COM open returns successfully with no human observation record. | Open can pass; the no-repair-dialog/human gate cannot be invented. |
| DF-11.AC10 | Probe-copy hash | A chart probe edits and saves a test copy. | Original release candidate hash stays unchanged; evidence identifies the probe separately. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-11
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-11 as verifiable checks and receipts. Do not label a missing test PASS, auto-approve aesthetic results, or create an unbounded polish loop. Keep original trusted-fixture helpers separate from hardened ingestion.
```

## 10. Source and decision traceability

This spec decomposes Architecture §11; Development plan PR-04, §11. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
