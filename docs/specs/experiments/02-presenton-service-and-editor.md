---
spec_id: DF-X2
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-X2"]
depends_on: ["DF-00", "DF-02", "DF-17"]
---

# DF-X2 — Presenton service, generation and editor experiment

**Goal:** Evaluate Presenton as an independent full-deck generation/editor candidate while measuring content retention, native output and edit ownership.

**Baseline mapping:** PR-X2. **Dependencies:** [DF-00](../core/00-baseline-and-workspace.md), [DF-02](../core/02-job-store-evidence-and-assets.md), [DF-17](../core/17-sandbox-security-and-privacy.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own isolated service setup, authentication, actual API-schema capture and comparison results. This is not a scene-level renderer plugin. Do not invent request/response fields or polling URLs; inspect the selected running version before implementing the adapter.

## 2. File ownership and integration boundary

- `packages/adapters/presenton/`
- `tests/experiments/presenton/`
- `docs/experiments/presenton/`
- `config/experiments/presenton.json`
- `scripts/start-presenton-lab.py (existing helper; preserve behavior)`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Input is frozen approved synthetic content translated to the service’s verified submission format, with a separate mapping back to DeckSpec content IDs. Output is an independent candidate deck/session report, not a mutation of the active reference build.

Start from the existing print-only lab helper. Only explicit `--start` starts the service. Record image digest, actual API schema, authentication method and configured model/image/search/telemetry egress before sending data.

## 4. Requirements


### DF-X2.R01 — Isolation

Loopback bind, synthetic inputs, separate private service volume and approved egress policy. No company directories or host Docker socket exposed to the app.


### DF-X2.R02 — Actual API contract

Probe the selected version’s documented generation/auth behavior and save sanitized request/response fixtures. Unknown fields or endpoint changes fail explicitly.


### DF-X2.R03 — Content reconciliation

Extract generated output and compare numbers, quotes, qualifiers, labels and notes against frozen input. A more attractive deck does not pass if important facts are lost.


### DF-X2.R04 — Editing ownership

Determine whether browser edits live in the service, our DeckSpec, or exported PPTX. Do not claim bidirectional synchronization; record immutable import/export checkpoints.


### DF-X2.R05 — Credentials

Never put API/provider credentials into generated HTML, public config, logs or fixtures. External calls are separately authorized even when the app is self-hosted.


### DF-X2.R06 — Promotion criteria

Require useful review/editor behavior, reproducible editable export, known retention limits and a coherent ownership model. Promotion does not require merging its engine into our final writer.


### DF-X2.R07 — Docker Desktop boundary

Presenton may run in Docker Desktop/Linux containers as a separate experiment. It must not mount the Windows Office profile, get COM access or invoke Office through a service; move admitted exported files to DF-20 for desktop verification.

### DF-X2.R08 — Windows editor handoff

Reconcile content/notes/data from Presenton export on a staged local path, then render/probe in PowerPoint. Keep API/editor state ownership independent of DeckSpec and preserve manual Office edits.

## 5. Implementation tasks

- [ ] **DF-X2.T01 — Dry-run helper.** Inspect the exact command before starting Docker; preserve existing containers/volumes.
- [ ] **DF-X2.T02 — Capture selected service contract.** Record image digest and authenticated generation flow with only synthetic input.
- [ ] **DF-X2.T03 — Run fixed deck candidates.** Generate independently, extract/reconcile content, inspect native objects and render final PPTX.
- [ ] **DF-X2.T04 — Exercise browser editing.** Change text/data/layout; document where state changes and what can be safely re-imported.
- [ ] **DF-X2.T05 — Decide UI/backend role.** Recommend independent experimental service, approved UI adapter or no integration based on observed behavior.

- [ ] **DF-X2.T06 — Exercise the local Windows handoff.** Record image digest, loopback binding, explicit mounted paths, egress policy, download hash and native export results. No customer content until security and provider policy pass.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `SERVICE_SCHEMA_CHANGED` | Stop and recapture the selected version’s contract. |
| `SERVICE_AUTH_FAILED` | Return sanitized failure, no credential echo. |
| `CANDIDATE_CONTENT_DRIFT` | Mark candidate unapproved. |
| `EDIT_OWNERSHIP_UNRESOLVED` | Do not integrate the editor as authoritative. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-X2.AC01 | Dry run | Invoke the existing helper without --start. | No container is started; proposed configuration is printed. |
| DF-X2.AC02 | Unauthorized request | Call generation with missing/invalid credentials. | Fails without revealing secrets or using a hidden fallback. |
| DF-X2.AC03 | Content drift | Service changes a qualified metric or omits a note. | Reconciliation flags the exact content IDs. |
| DF-X2.AC04 | Existing container | Start with a conflicting lab name. | Helper refuses replacement; existing state stays intact. |
| DF-X2.AC05 | Editor roundtrip | Edit a slide in the browser and export. | Report identifies preserved/lost semantics and actual owner of edits. |
| DF-X2.AC06 | Provider denial | Configure an unapproved external model endpoint. | Synthetic-only restriction or egress policy prevents unauthorized company-data submission. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-X2.AC07 | Container requests COM | An integration asks to call desktop Office from the container. | Request is rejected; only admitted artifacts cross the boundary. |
| DF-X2.AC08 | Editor rewrites text | A generated slide changes a qualifier before export. | Content diff blocks acceptance even if PowerPoint renders cleanly. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-X2
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-X2 as a synthetic local experiment. Capture the real selected API before writing calls. Keep candidates separate, reconcile facts and report edit ownership. Do not deploy a team service or upload company files.
```

## 10. Source and decision traceability

This spec decomposes Architecture §10; source S13 retained in baseline; Development plan §8.3, PR-X2. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
