---
spec_id: DF-19
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-08"]
depends_on: ["DF-11", "DF-15", "DF-16", "DF-18", "DF-S01", "DF-S02", "DF-S03", "DF-S04", "DF-S05", "DF-S06", "DF-S07", "DF-S08"]
---

# DF-19 — CI, comparative benchmarks and public-beta release

**Goal:** Release a demonstrably useful branded presentation workflow with repeatable quality gates, not just a successful demo on one machine.

**Baseline mapping:** PR-08. **Dependencies:** [DF-11](11-qa-receipts-and-release-gates.md), [DF-15](15-corporate-template-backend.md), [DF-16](16-review-ui-and-revision-ownership.md), [DF-18](18-pack-distribution-and-upstream-donors.md), [DF-S01](../structures/01-transformation-bridge.md), [DF-S02](../structures/02-hub-and-spoke.md), [DF-S03](../structures/03-architecture-layers.md), [DF-S04](../structures/04-comparison-and-scorecard.md), [DF-S05](../structures/05-roadmap-and-swimlane.md), [DF-S06](../structures/06-evidence-dashboard.md), [DF-S07](../structures/07-conceptual-and-measured-funnel.md), [DF-S08](../structures/08-editorial-hero.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own CI pipeline policy, normalized goldens, cross-engine benchmarking, native desktop and human acceptance protocols, pilot evidence and release packaging. Do not treat popularity or a model’s self-score as quality evidence or claim PowerPoint server automation has been implemented.

## 2. File ownership and integration boundary

- `.github/workflows/ci.yml (new)`
- `scripts/run-benchmarks.mjs (new)`
- `tests/benchmarks/`
- `docs/benchmarks/`
- `docs/pilots/`
- `docs/RELEASE_CHECKLIST.md`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Benchmark cases are the original F01–F14 in TRACEABILITY.md plus per-structure minimal/normal/dense/long-label fixtures. Every run records input/brand/pack/font/backend/environment hashes, gate outcomes, known limitations and review provenance.

Public CI uses synthetic data only. Company acceptance evidence and templates remain private; public reports can use sanitized summaries without reproducing proprietary inputs.

## 4. Requirements


### DF-19.R01 — Deterministic gates

Run contracts, capability, retention, geometry and package checks in a pinned environment. Compare canonical scenes and normalized package semantics; do not require byte-identical ZIP timestamps.


### DF-19.R02 — Rendered goldens

Pin rendering application, platform and font metrics. Pixel differences trigger review, not automatic approval of newly generated goldens.


### DF-19.R03 — Office application gate

Maintain native Windows PowerPoint render/inspection/edit/save receipts and a separate human review. Use an attended acceptance workstation for Office; portable CI and optional macOS/LibreOffice comparison cannot fill those native Windows gates.


### DF-19.R04 — Aesthetic benchmark

Compare frozen content/brand across candidate engines/treatments with randomized display order and recorded preference reasons. Preserve difficult content and native editing requirements.


### DF-19.R05 — Pilot definition

Complete an executive recommendation, technical architecture/migration and keynote-style deck. Record manual corrections, severe defects, brand preference, generation cost/latency and Office outcomes.


### DF-19.R06 — Release scope

Publish an explicit capability matrix and limitations. Any mandatory gate failing or NOT_RUN blocks the applicable approved-release claim. Optional experimental engines do not block the reference path.


### DF-19.R07 — Targets vs results

Keep intended cleanup-time/design-preference targets distinct from observations. Do not fabricate pilot success because code tests pass.


### DF-19.R08 — Two acceptance environments

Run deterministic unit/schema/OOXML suites on public Windows and optional Linux CI without Office. Run native acceptance separately on a private attended Windows workstation/VM, not a hosted worker or Windows service; consume only approved commits/fixtures.

### DF-19.R09 — Office-bound goldens

Bind native PNG/PDF/golden and behavior receipts to Office build, locale, font profile and export resolution. Require review when these change; do not disable corporate updates or accept screenshots from a different final hash.

### DF-19.R10 — Windows pilot gates

Default pilot decks require native rendering plus feature-specific edit/save tests and human design/repair-warning review. Separate COM automation from human evidence and include Windows path/lock/session regressions.

## 5. Implementation tasks

- [ ] **DF-19.T01 — Build reproducible CI.** Use the real dependency lock and a recorded renderer/font environment, with no private credentials in public jobs.
- [ ] **DF-19.T02 — Implement benchmark runner.** Run the same fixtures through eligible backends and compare semantics before aesthetic scoring.
- [ ] **DF-19.T03 — Add manual review forms.** Capture actual PowerPoint behaviors, device/app versions and exact artifact hashes.
- [ ] **DF-19.T04 — Run three pilots.** Use approved private pack/material only in the private lane, with retained review evidence.
- [ ] **DF-19.T05 — Package beta.** Produce source, notices, demo packs, CLI docs and a sanitized capability matrix after release allowlist checks.

- [ ] **DF-19.T06 — Add attended acceptance bundle.** Produce a signed/digest-bound fixture/request bundle for the operator, import redacted receipts, and block release for missing Windows gates. No automatic Office launch on untrusted pull requests.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `REGRESSION_FAILED` | Keep previous baseline and require reviewed fix. |
| `RELEASE_EVIDENCE_MISSING` | Block applicable release scope. |
| `GOLDEN_REVIEW_REQUIRED` | Require explicit reviewer decision. |
| `PRIVATE_ARTIFACT_DETECTED` | Stop publication. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-19.AC01 | Clean CI checkout | Run locked install and all implemented test suites from a new checkout. | No hidden local files or provider configuration required. |
| DF-19.AC02 | Changed font environment | Run a visual fixture with a different font fingerprint. | Golden comparison is identified as a different environment, not silently accepted. |
| DF-19.AC03 | Native regression | A candidate engine changes a chart to an image. | Semantic/editability gate fails regardless of visual preference. |
| DF-19.AC04 | Unrun Office check | Build release report without a manual Office receipt. | Supported workflow may remain beta/draft; no Office-approved claim. |
| DF-19.AC05 | Confidential golden | Attempt to publish a private client screenshot. | Publication allowlist blocks it. |
| DF-19.AC06 | Optional engine fails | PPTKit experiment fails a fixture but reference backend passes. | Reference release remains eligible; experiment is labeled unsupported/experimental. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-19.AC07 | Public pull request | A contributor changes worker code and requests a native run. | Public CI runs no-Office tests only; private workstation execution requires reviewed code. |
| DF-19.AC08 | Office version drift | Office updates between golden approval and a release. | Affected native results are stale and rerun/reviewed; no fake stable version assertion. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-19
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-19 only after the core workflow is usable. Publish real test/benchmark evidence and explicit limitations. Keep private pilot data out of public CI and do not let experimental engine failures block the reference path.
```

## 10. Source and decision traceability

This spec decomposes Architecture §11; Development plan PR-08, §11. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
