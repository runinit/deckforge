# Deckforge implementation specifications

**31 component specifications · documentation-only delivery · based on the audited 2026-09-15 plan.**

This pack turns the broad development plan into bounded implementation work. It does not add a production compiler, CLI, brand pack, renderer integration or passing application tests. The existing six-slide starter remains the baseline.

## Start here

Read [implementation order](IMPLEMENTATION_ORDER.md), [shared contracts](CONTRACTS.md), [command availability](COMMANDS.md) and [coding-agent workflow](AGENT_WORKFLOW.md). The [traceability map](TRACEABILITY.md) covers every original PR and F01–F14 acceptance fixture. [Validation report](VALIDATION_REPORT.md) records documentation checks only.

**First assignment:** DF-00 to reproduce/preserve the actual baseline, then DF-01 for production schemas. **First visual milestone:** bridge, architecture layers and editorial hero—not generic bullet slides. The eight structure packs are separate specs so they can be implemented/tested in parallel once shared boundaries exist.

## What every spec contains

Scope/non-goals, proposed file ownership, input/output interfaces, numbered requirements, implementation tasks, failure behavior, acceptance scenarios, command status, definition of done and a focused agent assignment. All new tasks start unchecked; test scenarios are requirements, not claims of execution.

The pack contains **183 requirements, 138 implementation tasks and 186 acceptance scenarios**, each with a stable ID. [spec-manifest.json](spec-manifest.json) exposes IDs and dependency relationships for tooling.

## Core product and delivery

| Spec | Implementation unit | Original PR | Depends on |
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
| [DF-09](core/09-native-charts-tables-and-connectors.md) | Native charts, tables, groups and connector behavior | PR-01, PR-04 | [DF-08](core/08-reference-pptx-writer.md) |
| [DF-10](core/10-svg-preview-gallery-and-motion.md) | SVG/HTML preview, structure gallery and optional motion | PR-03, PR-07 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md) |
| [DF-11](core/11-qa-receipts-and-release-gates.md) | QA, review receipts and bounded repair | PR-04 | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| [DF-12](core/12-markdown-intake.md) | Markdown intake and source-span preservation | PR-05 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-13](core/13-pptx-content-extraction.md) | PPTX content extraction and unsupported-object inventory | PR-05 | [DF-12](core/12-markdown-intake.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-14](core/14-director-cli-and-agent-skill.md) | Presentation director, CLI and thin agent skill | PR-07 | [DF-03](core/03-brand-capture-and-resolution.md), [DF-04](core/04-voice-terminology-and-claim-integrity.md), [DF-05](core/05-impeccable-design-intent-adapter.md), [DF-08](core/08-reference-pptx-writer.md), [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-12](core/12-markdown-intake.md) |
| [DF-15](core/15-corporate-template-backend.md) | Corporate-template compatibility and preservation backend | PR-06 | [DF-03](core/03-brand-capture-and-resolution.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-13](core/13-pptx-content-extraction.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-16](core/16-review-ui-and-revision-ownership.md) | Review UI, targeted revisions and manual-edit ownership | PR-07 | [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-14](core/14-director-cli-and-agent-skill.md) |
| [DF-17](core/17-sandbox-security-and-privacy.md) | Sandbox, privacy and controlled external services | PR-04, PR-05, PR-08 | [DF-02](core/02-job-store-evidence-and-assets.md) |
| [DF-18](core/18-pack-distribution-and-upstream-donors.md) | Pack distribution, upstream locks and donor-module integration | PR-08 | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-19](core/19-ci-benchmarks-and-public-beta.md) | CI, comparative benchmarks and public-beta release | PR-08 | [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-15](core/15-corporate-template-backend.md), [DF-16](core/16-review-ui-and-revision-ownership.md), [DF-18](core/18-pack-distribution-and-upstream-donors.md), [DF-S01](structures/01-transformation-bridge.md), [DF-S02](structures/02-hub-and-spoke.md), [DF-S03](structures/03-architecture-layers.md), [DF-S04](structures/04-comparison-and-scorecard.md), [DF-S05](structures/05-roadmap-and-swimlane.md), [DF-S06](structures/06-evidence-dashboard.md), [DF-S07](structures/07-conceptual-and-measured-funnel.md), [DF-S08](structures/08-editorial-hero.md) |

## Visual structure packs

| Spec | Implementation unit | Original PR | Depends on |
|---|---|---|---|
| [DF-S01](structures/01-transformation-bridge.md) | Transformation bridge composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |
| [DF-S02](structures/02-hub-and-spoke.md) | Hub-and-spoke ecosystem composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| [DF-S03](structures/03-architecture-layers.md) | Layered technical architecture composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |
| [DF-S04](structures/04-comparison-and-scorecard.md) | Comparison matrix and decision scorecard | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| [DF-S05](structures/05-roadmap-and-swimlane.md) | Roadmap, phases and swimlanes | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |
| [DF-S06](structures/06-evidence-dashboard.md) | Evidence dashboard and KPI composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| [DF-S07](structures/07-conceptual-and-measured-funnel.md) | Conceptual and measured funnel composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |
| [DF-S08](structures/08-editorial-hero.md) | Editorial hero and high-impact thesis composition | PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md) |

## Optional beta/research experiments

| Spec | Implementation unit | Original PR | Depends on |
|---|---|---|---|
| [DF-X1](experiments/01-pptkit-backend.md) | PPTKit scene adapter and promotion experiment | PR-X1 | [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-11](core/11-qa-receipts-and-release-gates.md) |
| [DF-X2](experiments/02-presenton-service-and-editor.md) | Presenton service, generation and editor experiment | PR-X2 | [DF-00](core/00-baseline-and-workspace.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| [DF-X3](experiments/03-isolated-research-critic.md) | Isolated research critic and visual ideation experiment | PR-X3 | [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-17](core/17-sandbox-security-and-privacy.md) |

## Add this pack to the existing project

The ZIP contains only `docs/specs/`. It does not replace the starter’s source, root plans, package manifest or AGENTS.md. Run from the existing project root; use a separate directory when `docs/specs` already exists.

```sh
cd "$HOME/04_Src/deckforge"
python3 -c "from pathlib import Path; assert not Path('docs/specs').exists(), 'docs/specs already exists; extract elsewhere and merge'"
python3 -m zipfile -e "$HOME/Downloads/deckforge-implementation-specs.zip" .
python3 docs/specs/tools/validate_specs.py
```

Execute extraction only after the guard succeeds. The guard/extraction are separate commands, not an atomic installer. No Git operation or external publication is performed.

Existing `npm test` / `npm run check` remain the smoke workflow. `npm run test:spec` and the `deck` commands are planned and do not exist until their implementation tasks are completed. See [COMMANDS.md](COMMANDS.md).

## Specification authority and source snapshots

[CONTRACTS.md](CONTRACTS.md) is the common field/behavior reference. Component specs refine its implementation. Preserve the architecture’s decisions: one final PPTX writer, no silent flattening, actual-artifact verification, approved brand precedence, controlled beta experiments and private company inputs.

The [architecture](references/ARCHITECTURE.md) and [development plan](references/DEVELOPMENT_PLAN.md) are copied unchanged for provenance. [Starter inventory](references/STARTER_INVENTORY.md) records actual files/scripts. External source/repository facts and pins are inherited from that audit, not newly researched or re-certified by this decomposition.

Source code remains unmodified. No company assets, font binaries, credentials, generated customer decks or upstream code are included in this specification pack.
