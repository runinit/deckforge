# Deckforge implementation specifications: Windows and native Office

**33 component specifications · 22 core + 8 visual structures + 3 experiments · windows-office-1 · documentation-only revision.**

All 31 original specs have component-specific Windows requirements, tasks and acceptance additions. New specs are [DF-20 native Office worker](core/20-windows-native-office-worker.md) and [DF-21 optional Word/Excel intake](core/21-word-excel-native-intake.md). Existing application code and dependencies are unchanged; no Office runtime or completed production CLI is supplied.

## Start here

Read [Windows setup](WINDOWS_SETUP.md), [Windows Office execution](WINDOWS_OFFICE.md), [implementation order](IMPLEMENTATION_ORDER.md), [shared contracts](CONTRACTS.md), [command availability](COMMANDS.md) and [agent workflow](AGENT_WORKFLOW.md). The [change log](WINDOWS_CHANGELOG.md) describes this revision; [traceability](TRACEABILITY.md) maps every original PR/fixture. [Validation report](VALIDATION_REPORT.md) records documentation checks only.

**Primary target:** Windows 11 x64, PowerShell 7, native Windows Node/Python and desktop PowerPoint/Excel/Word. PowerPoint is the required final-artifact acceptance application; Excel checks chart data; Word/Excel intake remains optional. The [attended execution contract](WINDOWS_OFFICE.md) separates native Office from public CI, Docker and WSL.

**First assignment:** DF-00 → DF-01 → private job/security/native export slice. **First visual milestone:** transformation bridge, architecture layers and editorial hero, reviewed in PowerPoint. Do not postpone distinctive design behind optional integrations.

## Requirements and scope

This pack contains **256 requirements, 181 implementation tasks and 272 acceptance scenarios**. Original IDs remain stable; all tasks are proposed and unchecked. [spec-manifest.json](spec-manifest.json) owns IDs/dependencies, snapshot hashes and platform coverage.

Each spec contains scope, file ownership, interfaces, requirements, tasks, failure handling, acceptance scenarios, command status, completion criteria and a focused agent assignment. Requirements describe future behavior; no PASS claim follows merely from a native application being installed.

## Core product and delivery

| Spec | Component | Original PR | Dependencies |
|---|---|---|---|
| [DF-00](core/00-baseline-and-workspace.md) | Baseline, toolchain and repository workspace | PR-00 | None |
| [DF-01](core/01-semantic-contracts-and-migrations.md) | Semantic contracts, identity and schema migration | PR-01 | [DF-00](core/00-baseline-and-workspace.md) |
| [DF-02](core/02-job-store-evidence-and-assets.md) | Job store, evidence registry and asset provenance | PR-01, PR-05 | [DF-01](core/01-semantic-contracts-and-migrations.md) |
| [DF-03](core/03-brand-capture-and-resolution.md) | Private brand capture, approval and token resolution | PR-02 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md) |
| [DF-04](core/04-voice-terminology-and-claim-integrity.md) | Voice, terminology and claim-preserving rewrites | PR-02 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-03](core/03-brand-capture-and-resolution.md) |
| [DF-05](core/05-impeccable-design-intent-adapter.md) | Impeccable design-intent adapter | PR-02 | [DF-03](core/03-brand-capture-and-resolution.md), [DF-04](core/04-voice-terminology-and-claim-integrity.md) |
| [DF-06](core/06-structure-pack-sdk-and-registry.md) | Structure-pack SDK, registry and composition contract | PR-01, PR-03 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md) |
| [DF-07](core/07-layout-text-and-scene-compiler.md) | Layout, font measurement and resolved-scene compiler | PR-01, PR-04 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-06](core/06-structure-pack-sdk-and-registry.md) |
| [DF-08](core/08-reference-pptx-writer.md) | Reference PPTX writer and capability negotiation | PR-01 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-07](core/07-layout-text-and-scene-compiler.md) |
| [DF-09](core/09-native-charts-tables-and-connectors.md) | Native charts, tables, groups and connector behavior | PR-01, PR-04 | [DF-08](core/08-reference-pptx-writer.md), [DF-20](core/20-windows-native-office-worker.md) |
| [DF-10](core/10-svg-preview-gallery-and-motion.md) | SVG/HTML preview, structure gallery and optional motion | PR-03, PR-07 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md) |
| [DF-11](core/11-qa-receipts-and-release-gates.md) | QA, review receipts and bounded repair | PR-04 | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-20](core/20-windows-native-office-worker.md) |
| [DF-12](core/12-markdown-intake.md) | Markdown intake and source-span preservation | PR-05 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-13](core/13-pptx-content-extraction.md) | PPTX content extraction and unsupported-object inventory | PR-05 | [DF-12](core/12-markdown-intake.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-20](core/20-windows-native-office-worker.md) |
| [DF-14](core/14-director-cli-and-agent-skill.md) | Presentation director, CLI and thin agent skill | PR-07 | [DF-03](core/03-brand-capture-and-resolution.md), [DF-04](core/04-voice-terminology-and-claim-integrity.md), [DF-05](core/05-impeccable-design-intent-adapter.md), [DF-08](core/08-reference-pptx-writer.md), [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-12](core/12-markdown-intake.md), [DF-20](core/20-windows-native-office-worker.md) |
| [DF-15](core/15-corporate-template-backend.md) | Corporate-template compatibility and preservation backend | PR-06 | [DF-03](core/03-brand-capture-and-resolution.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-13](core/13-pptx-content-extraction.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-20](core/20-windows-native-office-worker.md) |
| [DF-16](core/16-review-ui-and-revision-ownership.md) | Review UI, targeted revisions and manual-edit ownership | PR-07 | [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-14](core/14-director-cli-and-agent-skill.md) |
| [DF-17](core/17-sandbox-security-and-privacy.md) | Sandbox, privacy and controlled external services | PR-04, PR-05, PR-08 | [DF-02](core/02-job-store-evidence-and-assets.md) |
| [DF-18](core/18-pack-distribution-and-upstream-donors.md) | Pack distribution, upstream locks and donor-module integration | PR-08 | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-19](core/19-ci-benchmarks-and-public-beta.md) | CI, comparative benchmarks and public-beta release | PR-08 | [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-15](core/15-corporate-template-backend.md), [DF-16](core/16-review-ui-and-revision-ownership.md), [DF-18](core/18-pack-distribution-and-upstream-donors.md), [DF-S01](structures/01-transformation-bridge.md), [DF-S02](structures/02-hub-and-spoke.md), [DF-S03](structures/03-architecture-layers.md), [DF-S04](structures/04-comparison-and-scorecard.md), [DF-S05](structures/05-roadmap-and-swimlane.md), [DF-S06](structures/06-evidence-dashboard.md), [DF-S07](structures/07-conceptual-and-measured-funnel.md), [DF-S08](structures/08-editorial-hero.md) |
| [DF-20](core/20-windows-native-office-worker.md) | Windows desktop Office worker and application acceptance | PR-00, PR-04 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-21](core/21-word-excel-native-intake.md) | Native Word and Excel source intake | PR-05 | [DF-12](core/12-markdown-intake.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-20](core/20-windows-native-office-worker.md) |

## Visual structure packs

| Spec | Component | Original PR | Dependencies |
|---|---|---|---|
| [DF-S01](structures/01-transformation-bridge.md) | Transformation bridge composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |
| [DF-S02](structures/02-hub-and-spoke.md) | Hub-and-spoke ecosystem composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| [DF-S03](structures/03-architecture-layers.md) | Layered technical architecture composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |
| [DF-S04](structures/04-comparison-and-scorecard.md) | Comparison matrix and decision scorecard | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| [DF-S05](structures/05-roadmap-and-swimlane.md) | Roadmap, phases and swimlanes | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |
| [DF-S06](structures/06-evidence-dashboard.md) | Evidence dashboard and KPI composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| [DF-S07](structures/07-conceptual-and-measured-funnel.md) | Conceptual and measured funnel composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |
| [DF-S08](structures/08-editorial-hero.md) | Editorial hero and high-impact thesis composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |

## Beta and research experiments

| Spec | Component | Original PR | Dependencies |
|---|---|---|---|
| [DF-X1](experiments/01-pptkit-backend.md) | PPTKit scene adapter and promotion experiment | PR-X1 | [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-20](core/20-windows-native-office-worker.md) |
| [DF-X2](experiments/02-presenton-service-and-editor.md) | Presenton service, generation and editor experiment | PR-X2 | [DF-00](core/00-baseline-and-workspace.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-X3](experiments/03-isolated-research-critic.md) | Isolated research critic and visual ideation experiment | PR-X3 | [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-17](core/17-sandbox-security-and-privacy.md) |

## Installation and existing checkouts

The complete archive has a top-level `deckforge/`. The specs-only archive contains `docs/specs/`. The update archive contains changed documentation/agent instructions and the complete spec directory, but no application source or dependency changes. Extract to a **new staging directory** and review/merge for an existing checkout; never blindly expand over edited work.

```powershell
$Stage = Join-Path $env:USERPROFILE '04_Src\deckforge-windows-update-staging'
if (Test-Path -LiteralPath $Stage) { throw 'Staging directory exists; choose a new location.' }
Expand-Archive -LiteralPath (Join-Path $env:USERPROFILE 'Downloads\deckforge-windows-update.zip') -DestinationPath $Stage
Set-Location -LiteralPath $Stage
py -3 .\docs\specs\tools\validate_specs.py
```

Choose the actual downloaded path when Downloads is redirected. See [Windows setup](WINDOWS_SETUP.md) for full-bundle extraction and baseline commands. New native worker/CLI/spec-test commands remain TO IMPLEMENT.

## Source authority and provenance

[Active architecture](references/ARCHITECTURE.md) and [development plan](references/DEVELOPMENT_PLAN.md) incorporate this platform revision. Exact pre-Windows plans remain in the [historical archive](references/archive/pre-windows/README.md), with their original hashes. Their Linux setup/test records do not override the current platform.

New Windows/Office API facts are supported by [Microsoft sources](WINDOWS_SOURCES.md). Existing donor revisions/licensing notes are inherited from the prior audit, not newly certified. No corporate assets, font binaries, credentials, private decks or Office executables are included.
