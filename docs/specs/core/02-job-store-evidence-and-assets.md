---
spec_id: DF-02
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-01", "PR-05"]
depends_on: ["DF-01"]
---

# DF-02 — Job store, evidence registry and asset provenance

**Goal:** Give every input, fact, artifact and revision a controlled location and traceable identity without leaking private material into the public source tree.

**Baseline mapping:** PR-01, PR-05. **Dependencies:** [DF-01](01-semantic-contracts-and-migrations.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own local job transactions, path confinement, source/evidence/asset manifests, classification and immutable build storage. Parser sandboxing belongs to DF-17; semantic fact verification belongs to the content review workflow, not the asset loader.

## 2. File ownership and integration boundary

- `packages/jobs/src/`
- `packages/jobs/tests/`
- `packages/contracts/schemas/job.schema.json`
- `packages/contracts/schemas/source-manifest.schema.json`
- `examples/provenance/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
createJob(request: CreateJobRequest, policy: WorkspacePolicy): Promise<JobHandle>;
registerSource(job: JobHandle, source: SourceInput): Promise<SourceRecord>;
resolveAsset(job: JobHandle, assetId: string, scope: OutputScope): Promise<ResolvedAsset>;
commitRevision(job: JobHandle, expectedRevision: number, patch: ApprovedPatch): Promise<JobRevision>;
```
A job directory stores relative identifiers; internal absolute paths are resolved only at the filesystem boundary. Builds and releases are immutable subdirectories. A registry fingerprint participates in the build key.

## 4. Requirements


### DF-02.R01 — Atomic writes

Write temporary files in the destination filesystem, flush/close, then rename. Lock mutations with an expected revision. A failed build must not leave a success manifest or overwrite the last successful build.


### DF-02.R02 — Confinement

Resolve real paths and symlinks under configured roots. Recheck the file opened, reject path traversal and symlink escapes, and never trust archive paths as output paths.


### DF-02.R03 — Evidence state

Use supported, provided-unverified, assumption and synthetic exactly. Supported evidence requires a source locator and review record; registered source text is not automatically verified.


### DF-02.R04 — Asset eligibility

Require hash, verified media type, origin, sensitivity, rights status, allowed output scopes and alt text. The asset resolver performs no implicit network fetch.


### DF-02.R05 — Transitive sensitivity

Outputs inherit the maximum sensitivity of consumed inputs unless an explicit reviewed declassification exists. Sanitize display citations separately from private retrieval locators.


### DF-02.R06 — Changed artifacts

Track generated artifact hashes. Refuse to overwrite a changed PPTX; create a new version only through an explicit export action.


### DF-02.R07 — Windows-safe storage

Confine resolved paths across junctions/reparse points and case aliases. Reject ADS/device names and unsafe network/cloud-placeholder paths; stage admitted Office input locally. Logical IDs never become raw physical filenames.

### DF-02.R08 — Office locks and copies

Handle Windows sharing violations with bounded retries and revision checks. Save/edit probes use new immutable copy paths. Never remove Office lock files or overwrite open/manual-edited exports to force progress.

## 5. Implementation tasks

- [ ] **DF-02.T01 — Implement job layout.** Create the job directories, manifests and state record specified in CONTRACTS.md; reject public-repository roots for confidential jobs.
- [ ] **DF-02.T02 — Implement registries.** Store source bytes/hash and extraction metadata; bind evidence locators; register assets with explicit eligibility rules.
- [ ] **DF-02.T03 — Add revision transactions.** Support optimistic concurrency, interruption recovery and an append-only event record containing IDs and hashes rather than raw confidential prompts.
- [ ] **DF-02.T04 — Add export-safe projection.** Produce recipient-safe source labels and manifests without local paths, private source URLs or unrelated customer names.

- [ ] **DF-02.T05 — Test Windows path and file-lock behavior.** Add spaces/Unicode, case collisions, junction escape, reserved filename, long-path diagnostic, same-volume atomic replacement and open-PPTX lock fixtures.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `PATH_OUTSIDE_ROOT` | Stop input/output resolution. |
| `REVISION_CONFLICT` | Return actual revision and leave state unchanged. |
| `ASSET_NOT_ELIGIBLE` | Block the requested output scope. |
| `ARTIFACT_MODIFIED` | Preserve the file and require a new output target. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-02.AC01 | Path escape | Resolve `../secret`, an absolute path outside the root and a symlink crossing roots. | All fail before data is returned. |
| DF-02.AC02 | Concurrent edits | Two writers commit from revision 4. | Only one succeeds; the second returns a conflict without lost updates. |
| DF-02.AC03 | Evidence promotion | Register a source and an unverified claim. | The claim does not become supported without review. |
| DF-02.AC04 | Private asset | Request public output with an internal-only logo or unresolved artwork. | Export is blocked with the asset ID, not its sensitive full path. |
| DF-02.AC05 | Interrupted write | Terminate before final manifest rename. | Last successful revision/build stays valid and no success state is recorded. |
| DF-02.AC06 | Office manual edit | Change the bytes of a tracked exported PPTX. | Regeneration cannot overwrite it; an explicit new export preserves both. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-02.AC07 | Locked export | PowerPoint holds a user-edited exported file open. | Regeneration uses a new build; the open artifact and user changes remain intact. |
| DF-02.AC08 | Junction or ADS escape | An asset resolves outside the root or contains stream syntax. | Admission fails before COM or artifact publication. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-02
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-02 with synthetic files and temp directories. Test races, traversal and artifact hash protection. Do not ingest arbitrary Office files or connect a model provider.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§6.2, 11–12; Development plan PR-01, PR-02, PR-07. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
