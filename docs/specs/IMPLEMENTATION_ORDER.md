# Implementation order: Windows and native Office

**Revision:** windows-office-1. Dependencies in [spec-manifest.json](spec-manifest.json) are the machine-readable task graph; the sequence below groups work into useful increments. A dependency means its required contract/slice is available, not that every optional feature must be finished first. Read [shared contracts](CONTRACTS.md) and [Office execution](WINDOWS_OFFICE.md) before parallel work.

## 1. First executable slice

| Sequence | Work | Exit evidence |
|---|---|---|
| 1 | [DF-00](core/00-baseline-and-workspace.md): native Windows baseline, portable launchers, reviewed lockfile, separate Windows-font fixture | Explicit Node/Python commands work; exact Windows/Office inventory; historical test results remain labeled |
| 2 | [DF-01](core/01-semantic-contracts-and-migrations.md): production schemas, stable IDs, closed Office transport types | Invalid fields/references rejected; safe physical filenames distinct from semantic IDs |
| 3 | [DF-02](core/02-job-store-evidence-and-assets.md): private jobs, immutable builds/probes, Windows path/lock rules | No overwrite of edited/open files; real confinement including junction/case/ADS tests |
| 4 | Minimal [DF-17](core/17-sandbox-security-and-privacy.md) admission + [DF-20](core/20-windows-native-office-worker.md) attended worker | Safe doctor, read-only six-slide PowerPoint PNG/PDF export, unchanged-input hash and ownership cleanup |
| 5 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) | Semantic content compiles to a measured scene and one native PPTX writer; native PowerPoint render available for comparison |

Steps 4 and 5 can overlap after their shared contracts are committed. Do not put COM in the compiler, or postpone all native validation until after building every visual pack. DF-20 mutation probes come after its read-only export/ownership slice, not in its first patch.

## 2. Brand and the first three showcase slides

[DF-03](core/03-brand-capture-and-resolution.md), [DF-04](core/04-voice-terminology-and-claim-integrity.md) and [DF-05](core/05-impeccable-design-intent-adapter.md) capture actual company authority and approved voice. Use synthetic inputs until the private brand pack is approved. The existing palette and Liberation Sans demo are not a Ferroque standard.

Build these before expanding the entire catalogue:

| Showcase | Spec | Approval focus |
|---|---|---|
| Transformation bridge | [DF-S01](structures/01-transformation-bridge.md) | Strong directional composition with readable native labels and a correct static export |
| Architecture layers | [DF-S03](structures/03-architecture-layers.md) | Technical relationships, large diagrams, native editable objects and no false implied connections |
| Editorial hero | [DF-S08](structures/08-editorial-hero.md) | Brand typography, purposeful art and actual PowerPoint crop/font fidelity |

[DF-10](core/10-svg-preview-gallery-and-motion.md) provides actual-content previews; [DF-11](core/11-qa-receipts-and-release-gates.md) binds final PowerPoint and human review to exact artifacts. Native render success alone does not approve design or factual content.

## 3. Data, remaining structures and complete acceptance

[DF-09](core/09-native-charts-tables-and-connectors.md) and the later DF-20 probes establish real chart workbook edits in Excel, table/group edits and anchored connectors where supported. An exported line is not an anchored connector; probes may not repair it to fabricate support.

Then develop the remaining packs against the same brand/font profile: [hub/spoke](structures/02-hub-and-spoke.md), [comparison](structures/04-comparison-and-scorecard.md), [roadmap](structures/05-roadmap-and-swimlane.md), [dashboard](structures/06-evidence-dashboard.md) and [funnel](structures/07-conceptual-and-measured-funnel.md). Structure tasks can proceed in parallel after the pack/scene/writer contracts are stable. Share the same evidence and repair budget.

## 4. Intake, template assembly and review

[DF-12](core/12-markdown-intake.md) precedes [DF-13](core/13-pptx-content-extraction.md). Untrusted source parsing/admission runs before Office opens a file. Content extraction is not a lossless roundtrip guarantee.

[DF-15](core/15-corporate-template-backend.md) now prioritizes the admitted **PowerPoint-native template backend**. Real masters/custom layouts/placeholders are inventoried and tested on a copy; native assembly/save becomes the selected final writer. Keep `pptx-automizer` as an explicitly tested portable comparison. Neither lane silently mixes package writers.

[DF-14](core/14-director-cli-and-agent-skill.md) and [DF-16](core/16-review-ui-and-revision-ownership.md) expose the workflow to consultants. Their UI distinguishes fast SVG preview, native PowerPoint preview, PowerPoint-edited copies, and source-owned regeneration. There is no general automatic merge of arbitrary Office edits.

[DF-21](core/21-word-excel-native-intake.md) is an **optional intake extension** after DF-12/17/20. Word/Excel being installed does not require this extension before the first branded deck, nor authorize Word report or Excel model generation.

## 5. Distribution and experiment boundaries

[DF-18](core/18-pack-distribution-and-upstream-donors.md) and [DF-19](core/19-ci-benchmarks-and-public-beta.md) prepare the public beta. Windows no-Office CI checks portable code; private attended acceptance supplies real Office receipts. No public pull request executes code in a logged-in company Office profile. Office build/font updates trigger affected calibration and acceptance; do not disable security updates to preserve a screenshot baseline.

| Experiment | Timing and isolation | Promotion evidence |
|---|---|---|
| [DF-X1 PPTKit](experiments/01-pptkit-backend.md) | After scene/reference/native data contracts; independent output directory | Same data/content, native Windows rendering and real editing behavior on exact version |
| [DF-X2 Presenton](experiments/02-presenton-service-and-editor.md) | Early synthetic generation experiment under Docker Desktop/WSL or a separate service | Explicit local file transfer/admission, content diff, PowerPoint acceptance; no COM in container |
| [DF-X3 research critic](experiments/03-isolated-research-critic.md) | After QA/privacy boundaries | Measured benefit from admitted images/text without any COM, shell or private-path access |

## 6. Added native Windows fixtures

These supplement, rather than replace, original F01–F14. Every fixture records scenario input hash, environment, checks and cleanup. A scenario is a requirement, not a claimed test result.

| Fixture | Scenario | Required behavior | Main owner |
|---|---|---|---|
| W-F01 | Missing, blocked or unactivated desktop application | Clear prerequisite/interaction result; no green native gate | DF-00, DF-20 |
| W-F02 | Normal signed-in operator versus SYSTEM/service/disconnected session | Only approved attended desktop accepted; no hidden launch retry | DF-20 |
| W-F03 | User's unsaved deck/workbook already open; later ownership race | Refuse/pause without quitting, saving or killing user’s application | DF-20, DF-16 |
| W-F04 | Modal dialog, hang and cleanup failure | Deadline, bounded recovery, operator-required cleanup; no taskkill-all | DF-20 |
| W-F05 | Spaces, Unicode, case aliases, colon IDs, ADS and junction paths | Canonical private confinement and safe mapping; no traversal or overwrite | DF-01, DF-02, DF-17 |
| W-F06 | Approved font absent, different Office build, display-scaling change | Record affected profile and invalidate relevant receipts; native text review | DF-03, DF-07, DF-20 |
| W-F07 | Direct PNG/PDF export, hidden-slide and static-state mapping | Complete explicit slide mapping, fixed dimensions, unchanged source | DF-10, DF-20 |
| W-F08 | Native chart value edited and reopened | Excel data, PowerPoint cache and visual match; original untouched | DF-09, DF-20 |
| W-F09 | Native node moved; group/table edited | Claimed anchoring/group/cell behavior persists or fails explicitly | DF-09, DF-20 |
| W-F10 | Approved template adding a slide and changing theme token | Real custom layout/placeholders survive; final saved artifact revalidated | DF-15 |
| W-F11 | MOTW/Protected View, IRM/labels, macros, external links | Preserve provenance/protection, reject/require authorized action; no bypass | DF-17, DF-20 |
| W-F12 | Word tracked changes; Excel dates/formulas/hidden data | Declared read-only interpretation, no refresh/recalc or incidental leakage | DF-21 |

## 7. Handoff discipline

Each change names one primary spec and a bounded slice. Run existing tests first, add that slice's tests, list actual commands and unrun checks, and retain all prior requirement IDs. Coordinate shared contracts in DF-01/CONTRACTS before parallel implementations. New native commands and scripts remain TO IMPLEMENT until code and application evidence are delivered.
