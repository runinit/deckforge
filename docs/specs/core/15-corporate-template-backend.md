---
spec_id: DF-15
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-06"]
depends_on: ["DF-03", "DF-08", "DF-09", "DF-11", "DF-13", "DF-17"]
---

# DF-15 — Corporate-template compatibility and preservation backend

**Goal:** Use one approved corporate PPTX template with explicit, tested preservation guarantees rather than a visual imitation labeled as original-template support.

**Baseline mapping:** PR-06. **Dependencies:** [DF-03](03-brand-capture-and-resolution.md), [DF-08](08-reference-pptx-writer.md), [DF-09](09-native-charts-tables-and-connectors.md), [DF-11](11-qa-receipts-and-release-gates.md), [DF-13](13-pptx-content-extraction.md), [DF-17](17-sandbox-security-and-privacy.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own template inventory, compatibility profiles, placeholder mappings and the pptx-automizer backend. Support one known template first. Do not attempt arbitrary lossless roundtrip, preserve every animation by default or merge unreviewed decks from multiple engines.

## 2. File ownership and integration boundary

- `packages/adapters/template-pptx/`
- `packages/contracts/schemas/template-profile.schema.json`
- `tests/fixtures/templates/ (synthetic only)`
- `docs/template-compatibility/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed template profile identifies template hash, allowed slide masters/layouts, named placeholders, required fonts, theme mappings, preserved objects, unsupported features and tested export behaviors.

The template backend is one final writer/assembly owner for a deck. It may use a controlled PptxGenJS contribution path, but is responsible for final relationship integrity and theme/notes/data checks. Its profile states `reconstructed-theme`, `native-template` or `preserved-slide`; those are not interchangeable.

## 4. Requirements


### DF-15.R01 — Admission first

Inspect the template in DF-13/DF-17 before accepting it. Unknown macros, executable objects, external relationships or unsupported special objects block the initial path.


### DF-15.R02 — Exact identity

Bind a profile to the template digest and exporter pin. Template edits or backend updates invalidate compatibility receipts.


### DF-15.R03 — Placeholder semantics

Map semantic roles to verified placeholder/layout IDs. Required missing placeholders fail; no automatic replacement with floating boxes while claiming preservation.


### DF-15.R04 — Theme behavior

Verify actual theme inheritance and new-slide behavior, not only copied colors. Direct-color reconstruction is disclosed separately.


### DF-15.R05 — Preserved objects

Keep a per-object preservation/degradation list; notes, chart workbooks, layout relationships and optional animations need separate checks.


### DF-15.R06 — Manual Office gate

Add a slide with the intended layout, edit chart data/table text, save and reopen without repair. A copied master part alone is insufficient evidence.


## 5. Implementation tasks

- [ ] **DF-15.T01 — Create synthetic template.** Build a public test template with representative layout, placeholders, notes, chart/table and intentional unsupported features.
- [ ] **DF-15.T02 — Implement compatibility report.** Describe preserved/editable/degraded/unsupported elements before generation.
- [ ] **DF-15.T03 — Map approved company template.** Keep actual template and profile private; approval binds the tested digest.
- [ ] **DF-15.T04 — Implement backend adapter.** Assemble through one owner and produce the same ArtifactBundle/CapabilityReport contracts as the reference backend.
- [ ] **DF-15.T05 — Run new-slide and save tests.** Record each application behavior and release limitation separately.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `TEMPLATE_INCOMPATIBLE` | Reject the requested preservation lane; offer a disclosed reconstruction proposal. |
| `TEMPLATE_PROFILE_STALE` | Require a new compatibility run. |
| `PLACEHOLDER_MISSING` | Identify the semantic role and layout ID. |
| `PRESERVATION_FAILED` | Fail approved export. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-15.AC01 | Template changed | Modify template bytes after approval. | Compatibility profile is stale and cannot authorize release. |
| DF-15.AC02 | Missing placeholder | Required title placeholder is absent. | Build fails with the layout/role mapping problem. |
| DF-15.AC03 | New slide | Add a new slide and apply the company layout in PowerPoint. | Intended layout/theme behavior survives; record actual result. |
| DF-15.AC04 | Chart/notes persistence | Edit chart values and notes, save and reopen. | Data/notes and relationship integrity remain valid or the profile fails. |
| DF-15.AC05 | Unsupported animation | Template contains an untested animation. | Report it explicitly; do not mark animation preservation supported. |
| DF-15.AC06 | Reconstructed theme | Use a generated theme rather than the original master. | Output manifest labels reconstruction, never native-master preservation. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-15
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-15 for one synthetic template, then one explicitly supplied approved corporate template. Preserve guarantees narrowly and test actual new-slide/edit/save behavior. Do not promise generic roundtrip.
```

## 10. Source and decision traceability

This spec decomposes Architecture §9; source S09 retained in baseline; Development plan PR-06. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
