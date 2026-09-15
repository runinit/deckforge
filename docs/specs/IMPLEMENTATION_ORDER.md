# Implementation order and parallel work

File numbers are navigation labels, **not a topological build order**. Security DF-17 intentionally comes before untrusted intake; optional experiments may begin as source acquisition earlier than their adapter-promotion gates.

The hard dependency graph is in [spec-manifest.json](spec-manifest.json). Dependencies refer to usable contracts/features, not ceremonial completion of every optional stretch goal. A contract may be implemented in a small tested slice, but downstream work must declare which slice it consumes.

## 1. First vertical slice: reliable native output

| Sequence | Specs / tasks | Deliverable |
|---|---|---|
| A1 | DF-00 | Preserve fixture, real dependency lock, baseline report and honest test dispatch |
| A2 | DF-01 | Strict semantic/scene schemas, IDs, validation and explicit smoke migration |
| A3 | DF-02 | Private job roots, registries, atomic revisions, immutable builds |
| A4 | DF-06 | Pack manifest/registry and composition boundary; fixtures, not a huge catalog |
| A5 | DF-07 | Measured point-based scene compilation and fit failures |
| A6 | DF-08 | Scene-to-PPTX reference writer, native essentials and explicit capabilities |

Do not bundle A1–A6 into one unreviewable coding-agent assignment. The compiler/writer can first use synthetic test scenes; full composition packs are implemented next. No company approval is necessary to prove the demo path, but the demo must not be labeled company-branded.

## 2. First visual milestone: three showcase compositions

As soon as A6 works, implement [bridge DF-S01](structures/01-transformation-bridge.md), [architecture DF-S03](structures/03-architecture-layers.md) and [hero DF-S08](structures/08-editorial-hero.md). In parallel, implement [preview/gallery DF-10](core/10-svg-preview-gallery-and-motion.md).

This milestone must demonstrate large readable diagrams, deliberate typography, meaningful layout variety and native text—not just functioning OOXML. Produce both a scene preview and an actual-PPTX render. Side-by-side review uses identical content, not a more flattering simplified version.

### Brand work runs alongside this

After A3, run [DF-03](core/03-brand-capture-and-resolution.md) → [DF-04](core/04-voice-terminology-and-claim-integrity.md) → [DF-05](core/05-impeccable-design-intent-adapter.md). Real company inputs stay private and require authority/approval. The three treatments can be exercised with the synthetic demo until approved material is supplied.

A visually impressive demo is not yet a Ferroque-branded deliverable. The brand milestone is complete only when the actual brand owner approves the identity/treatment/voice pack.

## 3. Data, remaining structures and QA

After A6, implement [native data/edges DF-09](core/09-native-charts-tables-and-connectors.md), then [QA DF-11](core/11-qa-receipts-and-release-gates.md). Early core and visual work still has local tests; this adds reusable release gates, not the first testing in the project.

Finish the remaining packs: hub/spoke, comparison, roadmap/swimlane, dashboard and funnel. Data packs depend on actual native chart/table/edge behavior. Each pack gets two purposeful variants and four density fixtures with semantic/native coverage.

Aesthetic and editability acceptance are separate: a beautiful bitmap cannot pass a native-table requirement, and a technically valid but unreadable native deck cannot pass design review.

## 4. Intake and orchestration

After A3, security can proceed independently as [DF-17](core/17-sandbox-security-and-privacy.md). Then implement [Markdown DF-12](core/12-markdown-intake.md) → [PPTX extraction DF-13](core/13-pptx-content-extraction.md).

[Director/CLI DF-14](core/14-director-cli-and-agent-skill.md) integrates the approved content/brand/design/QA operations when their contracts exist. Start with manual/agent-authored structured proposals and a deterministic fake planner in CI. Direct provider SDKs and autonomous background agents are not prerequisites.

Do not ship arbitrary-file ingestion by invoking the existing trusted-smoke render helper on uploads. Hardened workers are an explicit dependency.

## 5. Company template and review experience

[Template backend DF-15](core/15-corporate-template-backend.md) and [review UI DF-16](core/16-review-ui-and-revision-ownership.md) are separate implementation tracks once their listed dependencies pass.

Start with one approved template and a narrow compatibility profile. Start the UI as a read-only story/gallery/QA viewer, then add revision-checked proposals and approved export. Neither track is permission to build a general PowerPoint editor or lossless import/export roundtrip.

## 6. Upstream reuse and experiments

[Pack/donor integration DF-18](core/18-pack-distribution-and-upstream-donors.md) can start after job/registry/security foundations. Port one tested module at a time; do not wait until final release to capture provenance.

| Track | Can begin early | Needs the full spec prerequisites for |
|---|---|---|
| PPTKit DF-X1 | Pinned source acquisition, upstream build/example reproduction | Scene adapter comparison and promotion |
| Presenton DF-X2 | Existing print-only setup; safe source review | Running service with controlled data/egress and ownership testing |
| Research critic DF-X3 | Paper/source review and security inventory | Executed critic over approved fixtures and measured comparative value |

No optional experiment blocks the reference backend. Promote only on the same frozen semantic/native/visual fixtures, not because beta software is new or visually impressive.

## 7. Release milestone

[DF-19](core/19-ci-benchmarks-and-public-beta.md) assembles the full CI/benchmark/pilot release process. Basic test CI should already exist after the baseline/contracts work; DF-19 adds complete rendered/native/application evidence and public-beta packaging.

Release gates include the eight visual structures, protected brand/voice behavior, safe intake, declared template support, review UX, public/private separation and three realistic pilot deck types. Actual PowerPoint review remains a separately recorded application/human gate.

## 8. Safe parallel ownership

| Workstream | Owned area | Coordination point |
|---|---|---|
| Contracts | `packages/contracts/` | One owner merges schema/public type changes |
| Compiler | `packages/compiler/` | Stable LayoutDraft/Scene fields agreed before pack work |
| Writer/native data | `packages/renderer-pptx/` | DF-08 owns adapter shell; DF-09 owns specialized handlers |
| Brand/voice | `packages/brand/` | DF-03 owns resolver; DF-04 owns voice subdirectory |
| Individual visual packs | One `packs/core/<id>/` per task | Registry additions and common harness changes reviewed centrally |
| Preview and UI | `packages/preview/` versus `apps/review/` | No second document state; both consume shared jobs/contracts |
| Experiments | One adapter/lab per engine | Never rewrite the reference path or global dependency pins |

Avoid two agents independently changing `package.json`, the schema validator, root TypeScript config, the pack registry or receipt state model. Use small contract-change PRs before parallel implementation that depends on them. Workers return patches/proposals; a coordinator handles shared integration.

## 9. First coding-agent task

Use [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md). Begin with DF-00 unless its current-baseline acceptance evidence already exists in the actual checkout. Then implement DF-01 only. Do not infer completion from this spec pack or the historical audit report.
