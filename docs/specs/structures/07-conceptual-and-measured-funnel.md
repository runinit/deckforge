---
spec_id: DF-S07
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03"]
depends_on: ["DF-06", "DF-07", "DF-08"]
---

# DF-S07 — Conceptual and measured funnel composition

**Goal:** Use an attractive funnel to explain stages while making clear whether its narrowing is conceptual or quantitatively meaningful.

**Baseline mapping:** PR-03. **Dependencies:** [DF-06](../core/06-structure-pack-sdk-and-registry.md), [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own `funnel` pack 1.0.0. Variants: `stepped-panels` and `contour-funnel`. Semantic mode is separately `conceptual` or `measured`; visual variant does not choose numeric meaning.

## 2. File ownership and integration boundary

- `packs/core/funnel/`
- `tests/structures/funnel/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Content defines 2–6 ordered stages with ID, label and optional detail. Measured mode also requires nonnegative counts, unit, common cohort/period and evidence IDs. For retention funnels, counts must be nonincreasing; other processes need a different explicit structure.

The initial measured encoding uses width proportional to count with equal stage height and an explicit “width represents count” legend. Counts and conversion labels remain native text. A conceptual funnel has no numeric-area claim.

## 4. Requirements


### DF-S07.R01 — Declared semantics

Conceptual mode is visibly identified as a process/concept. Measured mode declares its width encoding and cohort/period so viewers do not mistake decorative area for data.


### DF-S07.R02 — Quantitative integrity

Validate monotonic retention, common unit/cohort and denominator rules. Zero denominators yield undefined conversions; never coerce to 0% or 100%.


### DF-S07.R03 — Geometry

Stepped panels are native shapes with proportional widths where measured. Contour artwork may decorate conceptual mode; measured contour must preserve the declared width encoding or be unavailable.


### DF-S07.R04 — Native labels

All stages, counts and conversion percentages are native, with outside callouts allowed when a narrow stage cannot contain text.


### DF-S07.R05 — No minimum-width lie

Do not enlarge a tiny measured stage merely to fit a label. Put the label outside or choose stepped panels with explicit markers while retaining correct scale.


### DF-S07.R06 — Capacity

A seventh stage or excessive detail proposes continuation/another process structure, not dropped text.


### DF-S07.R07 — Native funnel interpretation

PowerPoint exports must preserve the conceptual versus measured distinction and any numeric scale. Native labels and values stay editable; qualitative stage widths cannot be presented as computed conversion areas.

## 5. Implementation tasks

- [ ] **DF-S07.T01 — Implement conceptual variants.** Create clear native stage labels and attractive geometry without numeric claims.
- [ ] **DF-S07.T02 — Implement measured widths.** Use an explicit common maximum/count scale; label widths and counts accurately.
- [ ] **DF-S07.T03 — Add conversion calculation.** Bind denominators to explicit previous/initial stage policy and disclose rounding.
- [ ] **DF-S07.T04 — Test visual/data semantics.** Review tiny/zero stages, nonmonotonic inputs and long labels separately.

- [ ] **DF-S07.T05 — Exercise the Windows native variants.** Test static states, one changed label and measured-value consistency through PowerPoint save/reopen on the approved Windows font profile.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `FUNNEL_SEMANTICS_INVALID` | Recommend a process flow or corrected dataset. |
| `CONVERSION_UNDEFINED` | Display explicit not-applicable state. |
| `FUNNEL_CAPACITY` | Return alternate structure/split proposal. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-S07.AC01 | Minimal | Two conceptual stages without counts. | No percentages or data geometry is invented. |
| DF-S07.AC02 | Normal | Four measured stages from a common cohort. | Widths and conversion labels follow declared calculations. |
| DF-S07.AC03 | Dense | Six stages with long descriptions. | Readable external labels or explicit split. |
| DF-S07.AC04 | Nonmonotonic | Counts grow from 100 to 150 in retention mode. | Rejected as incompatible semantics. |
| DF-S07.AC05 | Zero denominator | A zero-count stage precedes another zero. | Conversion is undefined/not applicable, not fabricated. |
| DF-S07.AC06 | Tiny stage | Last stage is 1 out of 10,000. | Width remains truthful; label moves outside. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-S07.AC07 | Native variant edit/save | A measured value changes on a probe copy. | Either geometry is explicitly recomputed by a reviewed build or the mismatch is flagged; no misleading stale area claim. |
| DF-S07.AC08 | Static export on Windows | Render minimal, normal, dense and long-label fixtures through PowerPoint. | Both variants retain native essentials and readable content; record application/build/font and exact artifact hash. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-S07
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-S07 with conceptual versus measured semantics explicit. Preserve native labels and truthful widths. Never repurpose decorative source geometry as a quantitative chart without a defined encoding.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§8.3, 9; Development plan PR-03. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
