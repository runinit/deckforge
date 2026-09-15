# Windows-native revision change log

**Revision:** windows-office-1 · **Date:** 2026-09-15 · **Requested change:** assume Windows with native Office applications and update the plan and every subsequent spec.

## Changes delivered

The architecture, development plan, setup/run instructions, agent instructions, shared contracts, implementation order, traceability, index and all 31 existing specs are revised. Two specs are added, for a total of 33. The old source snapshots are preserved separately, while active references now reflect Windows.

| Area | Revised behavior |
|---|---|
| Developer environment | Windows 11 x64, PowerShell, native Node/Python, explicit Windows paths and launchers |
| Native preview | PowerPoint PNG/PDF from the actual saved artifact; SVG fast preview and LibreOffice comparison clearly separate |
| Office host | Proposed signed-in attended STA/COM worker with allowlisted file transport, ownership, deadlines and safe cleanup |
| Data and diagrams | Excel chart-workbook probes; native table/group and anchored connector edit/save checks |
| Corporate template | Native PowerPoint master/custom-layout/placeholder path first; portable automizer lane separately tested |
| Source intake | Optional read-only Word/Excel extraction with revision/formula/date/hidden-data policies |
| Privacy and safety | Windows ACL/path/reparse/ADS checks, source admission before Office, protection preserved, no global process kills |
| CI and release | Portable no-Office Windows CI plus private attended native acceptance; missing native gates block Windows-approved delivery |
| Manual edits | Separate probe/review copies; immutable generated artifact, no automatic overwrite/merge of external edits |
| Visual structures | All eight receive native Windows rendering/editing acceptance without diluting the original design requirements |

## Component coverage

| Spec | Change | Added requirement IDs |
|---|---|---|
| [DF-00](core/00-baseline-and-workspace.md) | Updated existing component | `DF-00.R06`, `DF-00.R07` |
| [DF-01](core/01-semantic-contracts-and-migrations.md) | Updated existing component | `DF-01.R06`, `DF-01.R07` |
| [DF-02](core/02-job-store-evidence-and-assets.md) | Updated existing component | `DF-02.R07`, `DF-02.R08` |
| [DF-03](core/03-brand-capture-and-resolution.md) | Updated existing component | `DF-03.R07`, `DF-03.R08` |
| [DF-04](core/04-voice-terminology-and-claim-integrity.md) | Updated existing component | `DF-04.R07` |
| [DF-05](core/05-impeccable-design-intent-adapter.md) | Updated existing component | `DF-05.R07`, `DF-05.R08` |
| [DF-06](core/06-structure-pack-sdk-and-registry.md) | Updated existing component | `DF-06.R07`, `DF-06.R08` |
| [DF-07](core/07-layout-text-and-scene-compiler.md) | Updated existing component | `DF-07.R07`, `DF-07.R08` |
| [DF-08](core/08-reference-pptx-writer.md) | Updated existing component | `DF-08.R07`, `DF-08.R08` |
| [DF-09](core/09-native-charts-tables-and-connectors.md) | Updated existing component | `DF-09.R07`, `DF-09.R08` |
| [DF-10](core/10-svg-preview-gallery-and-motion.md) | Updated existing component | `DF-10.R07`, `DF-10.R08` |
| [DF-11](core/11-qa-receipts-and-release-gates.md) | Updated existing component | `DF-11.R08`, `DF-11.R09`, `DF-11.R10` |
| [DF-12](core/12-markdown-intake.md) | Updated existing component | `DF-12.R07` |
| [DF-13](core/13-pptx-content-extraction.md) | Updated existing component | `DF-13.R07`, `DF-13.R08` |
| [DF-14](core/14-director-cli-and-agent-skill.md) | Updated existing component | `DF-14.R08`, `DF-14.R09` |
| [DF-15](core/15-corporate-template-backend.md) | Updated existing component | `DF-15.R07`, `DF-15.R08`, `DF-15.R09` |
| [DF-16](core/16-review-ui-and-revision-ownership.md) | Updated existing component | `DF-16.R07`, `DF-16.R08` |
| [DF-17](core/17-sandbox-security-and-privacy.md) | Updated existing component | `DF-17.R08`, `DF-17.R09`, `DF-17.R10` |
| [DF-18](core/18-pack-distribution-and-upstream-donors.md) | Updated existing component | `DF-18.R07`, `DF-18.R08` |
| [DF-19](core/19-ci-benchmarks-and-public-beta.md) | Updated existing component | `DF-19.R08`, `DF-19.R09`, `DF-19.R10` |
| [DF-20](core/20-windows-native-office-worker.md) | Added component | `DF-20.R01`, `DF-20.R02`, `DF-20.R03`, `DF-20.R04`, `DF-20.R05`, `DF-20.R06`, `DF-20.R07`, `DF-20.R08`, `DF-20.R09`, `DF-20.R10` |
| [DF-21](core/21-word-excel-native-intake.md) | Added component | `DF-21.R01`, `DF-21.R02`, `DF-21.R03`, `DF-21.R04`, `DF-21.R05`, `DF-21.R06`, `DF-21.R07`, `DF-21.R08` |
| [DF-S01](structures/01-transformation-bridge.md) | Updated existing component | `DF-S01.R07` |
| [DF-S02](structures/02-hub-and-spoke.md) | Updated existing component | `DF-S02.R06` |
| [DF-S03](structures/03-architecture-layers.md) | Updated existing component | `DF-S03.R06` |
| [DF-S04](structures/04-comparison-and-scorecard.md) | Updated existing component | `DF-S04.R06` |
| [DF-S05](structures/05-roadmap-and-swimlane.md) | Updated existing component | `DF-S05.R06` |
| [DF-S06](structures/06-evidence-dashboard.md) | Updated existing component | `DF-S06.R07` |
| [DF-S07](structures/07-conceptual-and-measured-funnel.md) | Updated existing component | `DF-S07.R07` |
| [DF-S08](structures/08-editorial-hero.md) | Updated existing component | `DF-S08.R07` |
| [DF-X1](experiments/01-pptkit-backend.md) | Updated existing component | `DF-X1.R06`, `DF-X1.R07` |
| [DF-X2](experiments/02-presenton-service-and-editor.md) | Updated existing component | `DF-X2.R07`, `DF-X2.R08` |
| [DF-X3](experiments/03-isolated-research-critic.md) | Updated existing component | `DF-X3.R07` |

## Implementation boundaries

This is a planning/specification update. Existing application source, JSON configuration, synthetic fixture, test file and package dependency remain byte-identical to the previous complete bundle. The documentation validator is updated for 33 specs and Windows coverage. No Office worker `.ps1`, native template adapter or Word/Excel importer is supplied as implemented code.

The current npm scripts still include `python3` and LibreOffice assumptions; explicit Windows baseline commands are provided and DF-00 owns their future migration. The original fixture's Liberation Sans is preserved; a separately named approved Windows-font fixture is planned. Windows/native Office application checks remain NOT_RUN for this delivery.

## Provenance and checking

[Original snapshots](references/archive/pre-windows/README.md) remain hash-verifiable. [Microsoft source register](WINDOWS_SOURCES.md) distinguishes API facts from project decisions. [Validation report](VALIDATION_REPORT.md) includes actual documentation checks and unchanged-source verification, not a fabricated Windows result.

Before merging into an existing checkout, review the update ZIP in a new staging directory and compare local changes. Do not overwrite code, edited plans, brand inputs or user-produced decks automatically.
