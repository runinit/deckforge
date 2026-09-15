---
spec_id: DF-14
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-07"]
depends_on: ["DF-03", "DF-04", "DF-05", "DF-08", "DF-10", "DF-11", "DF-12", "DF-20"]
---

# DF-14 — Presentation director, CLI and thin agent skill

**Goal:** Provide one user-facing workflow from brief to approved story, branded composition and export without asking non-designers for coordinates.

**Baseline mapping:** PR-07. **Dependencies:** [DF-03](03-brand-capture-and-resolution.md), [DF-04](04-voice-terminology-and-claim-integrity.md), [DF-05](05-impeccable-design-intent-adapter.md), [DF-08](08-reference-pptx-writer.md), [DF-10](10-svg-preview-gallery-and-motion.md), [DF-11](11-qa-receipts-and-release-gates.md), [DF-12](12-markdown-intake.md), [DF-20](20-windows-native-office-worker.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own workflow orchestration, CLI commands, skill routing, content proposals and structured operation results. Direct model SDK integration is optional later; the initial path accepts agent-authored structured proposals. Do not concatenate all upstream skills or let them own competing job states.

## 2. File ownership and integration boundary

- `packages/director/src/`
- `packages/cli/src/`
- `skills/deckforge/SKILL.md`
- `skills/deckforge/references/`
- `packages/director/tests/`
- `packages/cli/tests/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed CLI is specified centrally in [COMMANDS.md](../COMMANDS.md). Operations return JSON envelopes with command, status, jobId/revision, artifact IDs, diagnostics and next allowed actions. Human-readable output is a presentation of that same result.

The director accepts a ContentBundle and brief, produces a reviewable story (“ghost deck”), then DeckSpec. A planning proposal is not an approved revision. Story edits show retention/claim differences before compilation.

## 4. Requirements


### DF-14.R01 — One authority

Job state and revisions come from DF-02. Planner, design adapter and reviewers submit proposals/receipts; they cannot independently mark a job released.


### DF-14.R02 — Minimal questions

Infer structure choices from approved content and audience; ask only for missing decision-critical information. Do not ask non-designers to select fonts or x/y coordinates.


### DF-14.R03 — Story before rendering

Draft slide headlines, purpose and evidence references first. Present additions, omissions, assumptions and proposed splits in a reviewable diff.


### DF-14.R04 — No hidden rewriting

Compiler repairs cannot alter the story or evidence. A requested executive rewrite returns an approved content patch before regeneration.


### DF-14.R05 — Task-scoped skill loading

Load only relevant donor planning/design references, stripping host paths and author preferences. The runtime does not require eight independent agent processes.


### DF-14.R06 — Machine interface

Use stable documented exit codes and structured results. Never require scripts to scrape model conversation text or assume future commands already exist.


### DF-14.R07 — Egress

Remote model/search/image calls require explicit provider and sensitivity policy; no external call from an offline build command.


### DF-14.R08 — Native Windows command routing

Run the main CLI on Windows; route Office operations only to the DF-20 allowlist. Provide windows-office and office-free-draft profiles, explicit tool availability, argument-array invocation and safe Windows job paths.

### DF-14.R09 — Foreground interaction ownership

Surface busy/activation/security/dialog/session errors with an operator action; do not hide them in unattended retries or launch a service. Source/deck instructions never become PowerShell/VBA code.

## 5. Implementation tasks

- [ ] **DF-14.T01 — Implement local command shell.** Start with validate/build/qa against already-authored DeckSpec; add init/plan/gallery/review/export after their dependencies exist.
- [ ] **DF-14.T02 — Implement story proposal.** Map content blocks to action headlines/roles, preserving notes, numbers and unsupported-source warnings.
- [ ] **DF-14.T03 — Implement state transitions.** Require exact approval/revision receipts and invalidate dependent builds when proposals are applied.
- [ ] **DF-14.T04 — Write the thin skill.** Explain available commands and load only the relevant spec/reference. Keep development and end-user modes explicitly separate.
- [ ] **DF-14.T05 — Add scripted workflow test.** Use a deterministic fake proposal provider, not a live model, for CI.

- [ ] **DF-14.T06 — Wire desktop commands.** Implement doctor, qa --render powerpoint and office probe routing after DF-20. Add optional Word/Excel ingest routing after DF-21; missing optional Word support does not block unrelated deck generation.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `BRIEF_INCOMPLETE` | Return the minimum necessary question or input field. |
| `STORY_UNAPPROVED` | Keep planning state; block approved export. |
| `WORKFLOW_TRANSITION_INVALID` | Return allowed next actions. |
| `PROVIDER_NOT_AUTHORIZED` | Do not transmit data. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-14.AC01 | End-to-end proposal | Use approved synthetic content and demo brand. | Story proposal → approval → compile → QA → draft export follows legal states. |
| DF-14.AC02 | Missing goal | Brief lacks a desired decision. | Director requests that information or records an explicit user-accepted default; it does not invent customer goals. |
| DF-14.AC03 | Fact deletion | Planner drops a source metric or qualifier. | Retention diff requires review before story approval. |
| DF-14.AC04 | Schema failure | Agent emits invalid DeckSpec. | Structured exit 2 with paths; no render or file overwrite. |
| DF-14.AC05 | Unverified release | Request approved export with a required NOT_RUN gate. | Exit 5; draft artifacts remain separate. |
| DF-14.AC06 | Offline build | Build an approved DeckSpec while no provider is configured. | Build uses no model/network. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-14.AC07 | No Office in portable CI | Run a draft build with office-free-draft. | Draft reports native gates NOT_RUN; it does not impersonate windows-office approval. |
| DF-14.AC08 | Unsafe command input | A user-derived filename includes shell metacharacters. | It is treated as one validated argument or rejected, never evaluated. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-14
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-14 incrementally around existing contracts and commands. Use a deterministic fake planner in tests. Do not add autonomous multi-agent orchestration, a vector database or a mandatory provider dependency.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§5, 10–11; Development plan §§5, 10, PR-07. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
