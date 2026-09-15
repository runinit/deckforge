---
spec_id: DF-00
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-00"]
depends_on: []
---

# DF-00 — Baseline, toolchain and repository workspace

**Goal:** Preserve the runnable six-slide fixture and create a reproducible development starting point before replacing any renderer code.

**Baseline mapping:** PR-00. **Dependencies:** None.

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own local bootstrap, dependency locking, the smoke compatibility contract, and a small spec-test dispatcher. Do not implement a semantic compiler, publish a remote, install all upstream skills, or change the baseline visual design in this task.

## 2. File ownership and integration boundary

- `package.json`
- `package-lock.json`
- `tsconfig.json (handoff to DF-01)`
- `scripts/doctor.py`
- `scripts/test-spec.mjs (new)`
- `config/spec-tests.json (new)`
- `docs/BASELINE_REPORT.md (new)`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed dispatcher: `npm run test:spec -- DF-01`.

`config/spec-tests.json` maps a spec ID to explicit repository-relative test files and prerequisites. The dispatcher rejects unknown IDs, empty test selections and missing files; invokes child processes with argument arrays; and propagates nonzero exits. A missing suite is NOT_RUN, never a successful zero-test execution.

The existing commands remain `npm test`, `npm run smoke`, `npm run inspect`, `npm run check` and optional `npm run preview`. Do not change their behavior without a separate migration note.

## 4. Requirements


### DF-00.R01 — Baseline preservation

Record hashes of the original smoke input, source and tests. Keep the legacy `0.0.1-smoke` schema independent of production DeckSpec. Its chart range and fixed counts are fixture restrictions only.


### DF-00.R02 — Reproducible installation

Use the supplied exact PptxGenJS 4.0.0 baseline, create a real lockfile through a successful installation, then reproduce with `npm ci`. Record runtime/platform and lock digest. Do not invent a lockfile offline.


### DF-00.R03 — Honest capabilities

Keep connector anchoring, full text measurement, brand approval and Microsoft PowerPoint verification explicitly unverified until the corresponding tests exist.


### DF-00.R04 — Workspace privacy

Use external private brand/job roots and a separate upstream lab. Public source contains synthetic fixtures only. No font binaries or credentials enter the repository.


### DF-00.R05 — Test selection

The dispatcher accepts only manifest IDs, never evaluates input as a shell command and refuses test paths outside the repository.


## 5. Implementation tasks

- [ ] **DF-00.T01 — Capture before changes.** Run existing tests and structural inspection; record commands and results without copying the previous audit result as a new execution.
- [ ] **DF-00.T02 — Establish install evidence.** Install online when available, commit the reviewed lockfile, and reproduce in a clean directory. Record network/tool blockers rather than changing version pins silently.
- [ ] **DF-00.T03 — Add dispatcher.** Implement explicit ID-to-suite selection and a help/status view. Later specs add their own test mappings only when the suites are created.
- [ ] **DF-00.T04 — Record Office gate.** Render the final fixture locally when tools exist. Store a separate NOT_RUN/FAIL/PASS PowerPoint edit/save record with application version and file hash.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `DEPENDENCY_MISSING` | Explain the missing executable or package and stop only the affected operation. |
| `TEST_SELECTION_EMPTY` | Fail the requested spec test; do not mark implementation complete. |
| `BASELINE_REGRESSION` | Stop the migration and compare the original input and outputs. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-00.AC01 | Legacy fixture | Run all original validation cases and generate the original synthetic deck. | All 13 existing cases pass; the six-slide fixture retains its native chart/table/workbook/notes counts. |
| DF-00.AC02 | Clean install | Install in a new directory using the committed lockfile. | Command log and lock digest recorded; unavailable registry access produces NOT_RUN. |
| DF-00.AC03 | Dispatcher rejects input | Request an unknown ID, an empty suite and a path-escape test entry. | Each fails before executing tests; no arbitrary command execution. |
| DF-00.AC04 | Offline baseline | Run the installed smoke workflow with networking disabled. | No model, font CDN or upstream service request occurs. |
| DF-00.AC05 | Missing Office tools | Run reporting with no PowerPoint or LibreOffice available. | Each unavailable application check is NOT_RUN, not PASS. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-00
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-00 only. Preserve all original fixtures and source. Add installation evidence and the spec-test dispatcher; report which checks were actually executed. Do not create a public GitHub repository or add company assets.
```

## 10. Source and decision traceability

This spec decomposes Development plan §§2–5, 13; Architecture §§4, 16. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
