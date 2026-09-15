# Traceability: audited plan to Windows-native specifications

Every original PR, component ID and F01–F14 fixture remains represented. Windows requirements/tasks/scenarios are added to all 31 original specs; DF-20 and DF-21 introduce the native worker and optional native document/workbook intake. Existing IDs were not renumbered or marked complete.

## Original PR coverage

| Original PR | Current implementation specs |
|---|---|
| PR-00 | [DF-00](core/00-baseline-and-workspace.md), [DF-20](core/20-windows-native-office-worker.md) |
| PR-01 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| PR-02 | [DF-03](core/03-brand-capture-and-resolution.md), [DF-04](core/04-voice-terminology-and-claim-integrity.md), [DF-05](core/05-impeccable-design-intent-adapter.md) |
| PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-S01](structures/01-transformation-bridge.md), [DF-S02](structures/02-hub-and-spoke.md), [DF-S03](structures/03-architecture-layers.md), [DF-S04](structures/04-comparison-and-scorecard.md), [DF-S05](structures/05-roadmap-and-swimlane.md), [DF-S06](structures/06-evidence-dashboard.md), [DF-S07](structures/07-conceptual-and-measured-funnel.md), [DF-S08](structures/08-editorial-hero.md) |
| PR-04 | [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-20](core/20-windows-native-office-worker.md) |
| PR-05 | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-12](core/12-markdown-intake.md), [DF-13](core/13-pptx-content-extraction.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-21](core/21-word-excel-native-intake.md) |
| PR-06 | [DF-15](core/15-corporate-template-backend.md) |
| PR-07 | [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-14](core/14-director-cli-and-agent-skill.md), [DF-16](core/16-review-ui-and-revision-ownership.md) |
| PR-08 | [DF-17](core/17-sandbox-security-and-privacy.md), [DF-18](core/18-pack-distribution-and-upstream-donors.md), [DF-19](core/19-ci-benchmarks-and-public-beta.md) |
| PR-X1 | [DF-X1](experiments/01-pptkit-backend.md) |
| PR-X2 | [DF-X2](experiments/02-presenton-service-and-editor.md) |
| PR-X3 | [DF-X3](experiments/03-isolated-research-critic.md) |

Root-plan labels PR-04W and PR-05W identify the new Windows workstreams; their source mapping remains PR-00/04 and PR-05 respectively. They do not remove or replace the original backlog.

## Original fixture coverage

| Fixture | Purpose | Specs | Windows-native acceptance |
|---|---|---|---|
| F01 | Native smoke | [DF-00](core/00-baseline-and-workspace.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-20](core/20-windows-native-office-worker.md) | Inspect six slides and actual PowerPoint rendering; notes/native object expectations remain. |
| F02 | Long text | [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-20](core/20-windows-native-office-worker.md) | Measured text plus native PowerPoint rendering, no silent shrink or content loss. |
| F03 | Fonts and mixed scripts | [DF-03](core/03-brand-capture-and-resolution.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-20](core/20-windows-native-office-worker.md) | Installed/resolved Windows font profile; CJK/mixed weight and substitution behavior. |
| F04 | Bridge/dashboard design | [DF-S01](structures/01-transformation-bridge.md), [DF-S06](structures/06-evidence-dashboard.md), [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-11](core/11-qa-receipts-and-release-gates.md) | Compare final PowerPoint composition with approved references, not just SVG. |
| F05 | Native chart | [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-20](core/20-windows-native-office-worker.md) | Excel embedded data edit, PowerPoint cache/render, saved-copy persistence. |
| F06 | Native table | [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-20](core/20-windows-native-office-worker.md) | Real cells/merges and edit/save/reopen behavior. |
| F07 | Anchored graph | [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-20](core/20-windows-native-office-worker.md) | Move native node without repairing the writer output; declared anchoring persists. |
| F08 | Corporate master | [DF-15](core/15-corporate-template-backend.md), [DF-20](core/20-windows-native-office-worker.md) | Actual master/custom-layout/placeholder/new-slide behavior on the admitted native lane. |
| F09 | Offline assets | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-20](core/20-windows-native-office-worker.md) | Local assets/static state; controlled egress, no unsupported claim that COM is offline. |
| F10 | Evidence | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-04](core/04-voice-terminology-and-claim-integrity.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-21](core/21-word-excel-native-intake.md) | Source/notes/Excel numeric/Word qualifier integrity and supported-versus-assumed status. |
| F11 | Privacy | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-18](core/18-pack-distribution-and-upstream-donors.md), [DF-21](core/21-word-excel-native-intake.md) | Private paths, hidden cells, comments, screenshots and labels do not leak. |
| F12 | Malformed input | [DF-13](core/13-pptx-content-extraction.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-20](core/20-windows-native-office-worker.md), [DF-21](core/21-word-excel-native-intake.md) | Admission before Office, including Windows path/MOTW/security handling. |
| F13 | Manual edits | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-16](core/16-review-ui-and-revision-ownership.md), [DF-20](core/20-windows-native-office-worker.md) | Immutable generated input and distinct user/probe copies; file-lock/hash conflicts preserved. |
| F14 | Engine comparison | [DF-19](core/19-ci-benchmarks-and-public-beta.md), [DF-X1](experiments/01-pptkit-backend.md), [DF-X2](experiments/02-presenton-service-and-editor.md), [DF-20](core/20-windows-native-office-worker.md) | Same frozen content and target Office profile; no SVG-only or semantic-loss win. |

## New platform fixtures

[Implementation order](IMPLEMENTATION_ORDER.md#6-added-native-windows-fixtures) defines W-F01–W-F12. They cover desktop eligibility, process ownership, timeout/cleanup, Windows paths, fonts/profile drift, direct image/PDF export, chart and connector mutations, native template behavior, document security/protection and optional Word/Excel intake.

DF-20/DF-21 acceptance tables contain the detailed checks. Shared release and receipt rules remain in [CONTRACTS.md](CONTRACTS.md) and [WINDOWS_OFFICE.md](WINDOWS_OFFICE.md).

## Authority and history

The [active architecture](references/ARCHITECTURE.md) and [development plan](references/DEVELOPMENT_PLAN.md) include the Windows revision. Original pre-Windows plans are preserved byte-for-byte in the [archive](references/archive/pre-windows/README.md). New API facts are sourced in [WINDOWS_SOURCES.md](WINDOWS_SOURCES.md); earlier upstream commit pins are not represented as newly tested.

[spec-manifest.json](spec-manifest.json) is authoritative for component/requirement/task/test IDs and dependencies. [Validation report](VALIDATION_REPORT.md) records documentation integrity, not application implementation or Office certification.
