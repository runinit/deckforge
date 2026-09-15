---
spec_id: DF-18
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-08"]
depends_on: ["DF-02", "DF-06", "DF-17"]
---

# DF-18 — Pack distribution, upstream locks and donor-module integration

**Goal:** Reuse proven pieces of existing skills without coupling the product to their runtimes or accidentally publishing company assets.

**Baseline mapping:** PR-08. **Dependencies:** [DF-02](02-job-store-evidence-and-assets.md), [DF-06](06-structure-pack-sdk-and-registry.md), [DF-17](17-sandbox-security-and-privacy.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own pack acquisition/trust, provenance, version compatibility, upstream locks, donor-module extraction and release file allowlists. Fork only for maintained changes. Do not create ten mandatory skill dependencies or infer permission from a public repository.

## 2. File ownership and integration boundary

- `packages/packs/src/`
- `packages/packs/tests/`
- `config/upstreams.json`
- `config/donors.json (new)`
- `config/public-files.json (new)`
- `THIRD_PARTY_NOTICES.md`
- `docs/upstream-integrations/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

A donor record identifies upstream repo/commit/file, original license/notice, intended module, copied/adapted boundaries, transitive dependencies, local replacement path and executed test evidence.

Initial donor candidates remain those in the audited baseline: presentation-skill composition/QA, Knowledge Cat planning/evidence, slides-ai text/layout helpers, Impeccable guidance and eligible Astra visuals. Exact four recorded commits are inherited unchanged; unpinned candidates stay unverified until acquired and tested.

## 4. Requirements


### DF-18.R01 — No runtime inheritance

Port bounded functions/references rather than full agents. Remove hidden absolute paths, dynamic dependency installation, model defaults and host-specific dependencies.


### DF-18.R02 — Exact provenance

Lock source commits, dependency versions and asset hashes separately. A source pin does not pin a fetched binary, font, package tree or container image.


### DF-18.R03 — Trusted execution

Declarative packs and executable composition modules are distinct. Arbitrary TypeScript is executable code; require a reviewed allowlist for executable modules. Do not call a manifest signature a sandbox.


### DF-18.R04 — Rights and privacy

Retain per-file notices and output eligibility. Keep unresolved copied assets out of public distributions and never distribute company/private examples or font binaries.


### DF-18.R05 — Compatibility

Verify schema/compiler range and required capabilities before install/activation. Duplicate pack versions or changed digest under the same immutable version are rejected.


### DF-18.R06 — Update discipline

Updates run original and local regression fixtures on a review branch. Preserve the last known-good pin; no automatic production update to HEAD.


### DF-18.R07 — Windows distribution

Ship source/specs and signed-or-policy-approved worker scripts with exact digests; never bundle Office binaries, registration changes, credentials or fonts. No install-time COM actions or system-wide execution-policy changes.

### DF-18.R08 — Cross-platform upstream isolation

Re-audit donor scripts for bash/python3 assumptions, executable bits, symlinks, native module builds and case-colliding filenames. A successful WSL test does not prove Windows portability; preserve one lock/evidence record per environment.

## 5. Implementation tasks

- [ ] **DF-18.T01 — Create donor ledger.** Record candidate module boundaries and evaluation status without claiming suites already passed.
- [ ] **DF-18.T02 — Port one module.** Choose a measured-text or QA helper, isolate dependencies, add fixtures and original notices, and compare behavior with baseline.
- [ ] **DF-18.T03 — Implement local pack installer.** Start with reviewed local directories/archives; enforce digest, compatibility and path/size checks before registration.
- [ ] **DF-18.T04 — Build public release allowlist.** Include only original/permitted source, synthetic examples, schemas/docs and required notices.
- [ ] **DF-18.T05 — Add update workflow.** Resolve new pins deliberately, run regression evidence and publish a changed-capability report.

- [ ] **DF-18.T06 — Validate Windows packages.** Extract/install in a clean Windows path containing spaces, check copied skill digests without symlink privileges and run no-Office tests. Stage beta services outside the Office runtime with no profile or COM exposure.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `PACK_VERSION_CONFLICT` | Reject ambiguous content. |
| `PACK_PERMISSION_UNRESOLVED` | Block affected distribution only. |
| `DONOR_RUNTIME_DEPENDENCY` | Keep experimental until made portable. |
| `PUBLICATION_DENIED` | List disallowed logical assets/files without leaking sensitive content. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-18.AC01 | Hidden dependency | Donor function relies on an author-specific absolute path. | Port is rejected until the dependency is explicit or removed. |
| DF-18.AC02 | Same version different bytes | Install a pack ID/version with a different digest. | Reject ambiguity; require a new version. |
| DF-18.AC03 | Untrusted code pack | Install an executable composer not on the trust list. | No execution or dynamic import occurs. |
| DF-18.AC04 | Public artifact scan | Bundle includes a private logo, source deck or font binary. | Release packaging fails. |
| DF-18.AC05 | Upstream change | Update a donor pin and introduce a text-fit regression. | Upgrade fails the fixture comparison and prior pin remains usable. |
| DF-18.AC06 | Unresolved rights | A copied visual lacks established output eligibility. | Exclude it from public output and report it; original packs continue to work. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-18.AC07 | No admin install | Install source/spec/skill files under a standard user account. | Copy-based skill setup works or reports policy limits without elevation. |
| DF-18.AC08 | Untrusted upstream change | An update adds a post-install executable or Office automation. | Require explicit review before reuse; no automatic activation. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-18
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-18 with a donor ledger and one bounded tested port. Keep external lab checkouts separate. Do not install every upstream skill globally, execute unreviewed packs or publish unresolved/private assets.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§3, 10, 12; Development plan §§6–8, PR-08. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
