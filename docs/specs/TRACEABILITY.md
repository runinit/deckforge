# Traceability to the original development plan

This map records decomposition, not new implementation progress. All component specs are proposals. The source [development plan](references/DEVELOPMENT_PLAN.md) and [architecture](references/ARCHITECTURE.md) remain bundled unchanged.

## 1. Every original PR

| Original implementation unit | Detailed specs |
|---|---|
| PR-00 | [DF-00](core/00-baseline-and-workspace.md) |
| PR-01 | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md) |
| PR-02 | [DF-03](core/03-brand-capture-and-resolution.md), [DF-04](core/04-voice-terminology-and-claim-integrity.md), [DF-05](core/05-impeccable-design-intent-adapter.md) |
| PR-03 | [DF-06](core/06-structure-pack-sdk-and-registry.md), [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-S01](structures/01-transformation-bridge.md), [DF-S02](structures/02-hub-and-spoke.md), [DF-S03](structures/03-architecture-layers.md), [DF-S04](structures/04-comparison-and-scorecard.md), [DF-S05](structures/05-roadmap-and-swimlane.md), [DF-S06](structures/06-evidence-dashboard.md), [DF-S07](structures/07-conceptual-and-measured-funnel.md), [DF-S08](structures/08-editorial-hero.md) |
| PR-04 | [DF-07](core/07-layout-text-and-scene-compiler.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| PR-05 | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-12](core/12-markdown-intake.md), [DF-13](core/13-pptx-content-extraction.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| PR-06 | [DF-15](core/15-corporate-template-backend.md) |
| PR-07 | [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-14](core/14-director-cli-and-agent-skill.md), [DF-16](core/16-review-ui-and-revision-ownership.md) |
| PR-08 | [DF-17](core/17-sandbox-security-and-privacy.md), [DF-18](core/18-pack-distribution-and-upstream-donors.md), [DF-19](core/19-ci-benchmarks-and-public-beta.md) |
| PR-X1 | [DF-X1](experiments/01-pptkit-backend.md) |
| PR-X2 | [DF-X2](experiments/02-presenton-service-and-editor.md) |
| PR-X3 | [DF-X3](experiments/03-isolated-research-critic.md) |

## 2. Plan section coverage

| Source section | Owners |
|---|---|
| §1 Right deliverable | [DF-00](core/00-baseline-and-workspace.md), [DF-S01](structures/01-transformation-bridge.md), [DF-S03](structures/03-architecture-layers.md), [DF-S08](structures/08-editorial-hero.md) |
| §2 Toolchain/workspace | [DF-00](core/00-baseline-and-workspace.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| §3 Supplied starter | [DF-00](core/00-baseline-and-workspace.md), [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-08](core/08-reference-pptx-writer.md) |
| §4 Version control/publication | [DF-00](core/00-baseline-and-workspace.md), [DF-18](core/18-pack-distribution-and-upstream-donors.md), [DF-19](core/19-ci-benchmarks-and-public-beta.md) |
| §5 Coding-agent integration | [DF-05](core/05-impeccable-design-intent-adapter.md), [DF-14](core/14-director-cli-and-agent-skill.md) |
| §6 Upstream acquisition/forks | [DF-18](core/18-pack-distribution-and-upstream-donors.md), [DF-X1](experiments/01-pptkit-backend.md), [DF-X2](experiments/02-presenton-service-and-editor.md), [DF-X3](experiments/03-isolated-research-critic.md) |
| §7 Upstream checks/donor modules | [DF-18](core/18-pack-distribution-and-upstream-donors.md) |
| §8 Beta experiments | [DF-X1](experiments/01-pptkit-backend.md), [DF-X2](experiments/02-presenton-service-and-editor.md), [DF-X3](experiments/03-isolated-research-critic.md) |
| §9 Delivery backlog | [DF-00](core/00-baseline-and-workspace.md), [DF-19](core/19-ci-benchmarks-and-public-beta.md) |
| §10 Future CLI/job artifacts | [DF-01](core/01-semantic-contracts-and-migrations.md), [DF-02](core/02-job-store-evidence-and-assets.md), [DF-14](core/14-director-cli-and-agent-skill.md), [DF-16](core/16-review-ui-and-revision-ownership.md) |
| §11 Test matrix/benchmark | [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-11](core/11-qa-receipts-and-release-gates.md), [DF-17](core/17-sandbox-security-and-privacy.md), [DF-19](core/19-ci-benchmarks-and-public-beta.md) |
| §12 First coding-agent assignment | [DF-00](core/00-baseline-and-workspace.md), [DF-01](core/01-semantic-contracts-and-migrations.md) |
| §13 Verified delivery scope | [DF-00](core/00-baseline-and-workspace.md) |
| §14 Sources/pins | [DF-18](core/18-pack-distribution-and-upstream-donors.md) |

## 3. Original acceptance fixtures F01–F14

The named case is an entry point, not the sole test for that fixture. Supporting specs add the structural, visual and manual application evidence.

| Fixture | Concern | Primary acceptance case | Supporting specs |
|---|---|---|---|
| F01 | Native smoke | [DF-00.AC01](core/00-baseline-and-workspace.md) | [DF-08](core/08-reference-pptx-writer.md), [DF-09](core/09-native-charts-tables-and-connectors.md), [DF-11](core/11-qa-receipts-and-release-gates.md) |
| F02 | Long title/labels | [DF-07.AC02](core/07-layout-text-and-scene-compiler.md) | [DF-S01](structures/01-transformation-bridge.md), [DF-S03](structures/03-architecture-layers.md), [DF-S08](structures/08-editorial-hero.md) |
| F03 | CJK and mixed weights | [DF-07.AC03](core/07-layout-text-and-scene-compiler.md) | [DF-03](core/03-brand-capture-and-resolution.md), [DF-11](core/11-qa-receipts-and-release-gates.md) |
| F04 | Attractive bridge/dashboard | [DF-S01.AC02](structures/01-transformation-bridge.md) | [DF-S06](structures/06-evidence-dashboard.md), [DF-10](core/10-svg-preview-gallery-and-motion.md), [DF-19](core/19-ci-benchmarks-and-public-beta.md) |
| F05 | Native chart/workbook | [DF-09.AC03](core/09-native-charts-tables-and-connectors.md) | [DF-S06](structures/06-evidence-dashboard.md), [DF-11](core/11-qa-receipts-and-release-gates.md) |
| F06 | Native table/merges | [DF-09.AC05](core/09-native-charts-tables-and-connectors.md) | [DF-S04](structures/04-comparison-and-scorecard.md), [DF-11](core/11-qa-receipts-and-release-gates.md) |
| F07 | Anchored graph | [DF-09.AC06](core/09-native-charts-tables-and-connectors.md) | [DF-S02](structures/02-hub-and-spoke.md), [DF-X1](experiments/01-pptkit-backend.md) |
| F08 | Company master | [DF-15.AC03](core/15-corporate-template-backend.md) | [DF-03](core/03-brand-capture-and-resolution.md), [DF-11](core/11-qa-receipts-and-release-gates.md) |
| F09 | Offline/static assets | [DF-10.AC02](core/10-svg-preview-gallery-and-motion.md) | [DF-S01](structures/01-transformation-bridge.md), [DF-17](core/17-sandbox-security-and-privacy.md) |
| F10 | Evidence/claim fidelity | [DF-04.AC01](core/04-voice-terminology-and-claim-integrity.md) | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-12](core/12-markdown-intake.md), [DF-14](core/14-director-cli-and-agent-skill.md) |
| F11 | Privacy/publication | [DF-17.AC05](core/17-sandbox-security-and-privacy.md) | [DF-02](core/02-job-store-evidence-and-assets.md), [DF-18](core/18-pack-distribution-and-upstream-donors.md), [DF-19](core/19-ci-benchmarks-and-public-beta.md) |
| F12 | Malformed input | [DF-13.AC05](core/13-pptx-content-extraction.md) | [DF-17](core/17-sandbox-security-and-privacy.md) |
| F13 | Manual Office edits | [DF-02.AC06](core/02-job-store-evidence-and-assets.md) | [DF-16](core/16-review-ui-and-revision-ownership.md) |
| F14 | Cross-engine comparison | [DF-X1.AC05](experiments/01-pptkit-backend.md) | [DF-X2](experiments/02-presenton-service-and-editor.md), [DF-19](core/19-ci-benchmarks-and-public-beta.md) |

## 4. Deliberate implementation clarifications

| Refinement | Reason / owner |
|---|---|
| Immutable revision/build/release directories | Avoid stale approvals and overwriting Office edits; DF-02 |
| Separate source/evidence registries with multi-source locators | Make extraction and claim verification distinct; DF-01/02 |
| Exact common DesignIntent values | Prevent packs/adapters from interpreting vague numeric taste fields differently; DF-05/07 |
| Explicit static states for all packs | Avoid hidden GSAP labels/zero counters and unreliable screenshots; DF-06/10 |
| Early data/edge capability probes | Plain lines, editable charts, native groups and attached connectors are different behaviors; DF-09 |
| Security before arbitrary intake | Existing local helpers handle trusted fixtures, not hostile uploads; DF-17 before DF-12/13 |
| Template backend has one final assembly owner | Internal helper libraries do not justify arbitrary per-slide writer mixing; DF-15 |
| Full release depends on all eight visual packs | Keep the desired design vocabulary in the product, not only native OOXML plumbing; DF-19 |
| Source acquisition may precede adapter dependencies | Beta experiments can start early, but promotion still requires evidence; DF-X1/X2 |
| Test command lifecycle is explicit | Do not advertise future CLI/test scripts as installed; DF-00/14 |

None of these changes authorizes silent rewriting, rasterizing essential data, unbounded agent loops, unapproved company branding or lossless roundtrip claims.
