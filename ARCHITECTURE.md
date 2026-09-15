# Deckforge: audited hybrid presentation architecture

**Status:** proposed architecture, with a small executable native-PPTX smoke starter.  
**Audit date:** 2026-09-15.  
**Working name:** Deckforge; naming and repository availability have not been checked.  
**Primary use:** a company-branded presentation system for non-designers, initially for Ferroque consulting work.  
**Companion:** [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md).


## Contents

- [1. Decision](#1-decision)
- [2. Audit findings: what changes from the previous plan](#2-audit-findings-what-changes-from-the-previous-plan)
- [3. Verified reuse and fork map](#3-verified-reuse-and-fork-map)
- [4. Product boundary](#4-product-boundary)
- [5. Architecture and ownership](#5-architecture-and-ownership)
- [6. Data contracts](#6-data-contracts)
- [7. Brand and voice capture](#7-brand-and-voice-capture)
- [8. How to preserve Astra's graphics without losing editability](#8-how-to-preserve-astras-graphics-without-losing-editability)
- [9. Layout, type, charts and templates](#9-layout-type-charts-and-templates)
- [10. Experimental engines without architectural lock-in](#10-experimental-engines-without-architectural-lock-in)
- [11. Quality and release evidence](#11-quality-and-release-evidence)
- [12. Security, privacy and distribution](#12-security-privacy-and-distribution)
- [13. Proposed repository evolution](#13-proposed-repository-evolution)
- [14. Architecture decisions to preserve](#14-architecture-decisions-to-preserve)
- [15. Source register](#15-source-register)
- [16. Audit execution record](#16-audit-execution-record)

## 1. Decision

Build a **presentation compiler and design-pack system**, not a chain of eight independent slide agents.

Keep the compelling part of the original idea: Astra's visual structures, Impeccable's design judgment, reusable graphics, brand/voice capture, and editable PowerPoint. Change how those pieces are connected:

- One presentation director owns the brief, evidence, story, and revisions.
- A versioned semantic deck describes meaning, not renderer-specific coordinates.
- Approved structure packs turn that meaning into an explicit, measured scene.
- A single selected backend writes the final PPTX for a job.
- Experimental engines remain eligible, but earn adoption using the same fixtures.
- Browser previews and the final PowerPoint file have separate verification gates.

**Initial implementation:** PptxGenJS as the executable reference backend; `presentation-skill` as a fork/donor for composition and QA; Impeccable as design guidance; an Astra structure-porting track from the first visual milestone. PPTKit and Presenton are early experiments, not distant afterthoughts. Neither is the canonical project data model.

This is not a retreat to generic corporate templates. The first visual milestone must include a transformation bridge, an architectural composition, and an editorial or infographic treatment—not merely title/bullets/cards.

## 2. Audit findings: what changes from the previous plan

| Previous assumption | Audit finding | Architectural correction |
|---|---|---|
| More presentation skills produce a better combined agent | Their workflows overlap and can disagree on output format, style, language questions, editing policy, and renderer | Load selected reference modules under one orchestrator; do not concatenate whole skill instructions |
| A `SKILL.md` is an interchangeable engine API | It is an instruction package; scripts and runtime requirements differ [S12] | Wrap actual scripts or callable APIs with tested adapters |
| PPTKit can ingest a company PPTX losslessly | Its engine roadmap puts import and round-trip preservation in a later track [S04] | Separate content extraction, visual reconstruction, and native-template reuse |
| An SVG preview verifies PowerPoint appearance | PPTKit Presentation explicitly says its preview is not pixel-identical PowerPoint [S05] | Render the final PPTX; retain an actual PowerPoint edit/save gate |
| Knowledge Cat is a portable native renderer out of the box | Its bundled native builder expects a prepared `@oai/artifact-tool` workspace [S06] | Reuse planning, evidence contracts, and appropriate validators; do not make that runtime a core dependency |
| `pptx-automizer` preserves arbitrary templates and animations | Its documented limits include animation IDs and restrictions around layouts [S09] | Admit templates through a tested compatibility profile |
| Mix a different PPTX engine on every slide | Package parts, theme IDs, masters, charts, notes, relationships, and animation references must survive assembly | One final writer per deck. Per-slide *composition* routing is supported; foreign-PPTX merging is a later, explicit mode |
| Astra is simply a dependency-free reusable template library | The inspected bridge has external font requests, SVG effects, animated/hidden elements, and dense hardcoded text [S02] | Inventory dependencies, freeze animation state, separate labels from artwork, and re-layout |
| Beta means accept any integration | Beta is a release label, not evidence about reproducibility or fidelity | Accept beta components behind pinned experiments and measurable exit gates |
| An open-source destination makes source licensing irrelevant | A public repository and a reuse license are different; an adapter does not create permission [S14] | Keep provenance and notices. Resolve redistribution rights for copied assets/code; do not block unrelated implementation |
| The core would be tiny | Layout, import fidelity, native editing, QA, privacy, and authoring UX are substantial work | Deliver vertical slices and limit v0.1 capabilities explicitly |
| Published security advisories prove current PPTAgent is unpatched | The cited code-execution advisory names a patch commit [S10] | Check ancestry and all applicable advisories; do not describe all current versions as vulnerable |

Earlier popularity counts and unverified maturity claims are not used as selection criteria. This audit inspected documentation, manifests, selected source, and recorded four repository HEADs. It did **not** execute every upstream test suite or certify any upstream as production-ready.

## 3. Verified reuse and fork map

### 3.1 Practical shortlist

| Component | What was verified | What to reuse | Decision |
|---|---|---|---|
| Astra Slide | Browser HTML/SVG workflow, structure files, explicit SVG/HTML paths [S01–S02] | Composition examples, visual motifs, structure catalog; actual ports where rights permit | Keep a pinned external reference checkout; create a licensed/publicly distributable port pack only after clearance |
| Impeccable | Product/design context, critique/refinement commands, frontend-oriented detectors; Apache-2.0 [S03] | Design intake, hierarchy/type/composition critique, context discipline | Install a pinned release; implement a presentation-specific adapter, not an Office claim |
| `siril9/presentation-skill` | v0.11.0 source-first workflow, PptxGenJS renderer, Python tooling, many named validation scripts; MIT [S07] | Composition grammar, source workspace, review receipts, relevant QA | Primary **fork candidate**, with selected contributions ported into the core rather than wholesale runtime coupling |
| Knowledge Cat | Story/evidence planning, output lanes, validators and case artifacts; MIT; native runtime prerequisite [S06] | Story planner references, evidence schema ideas, selected dependency-free checks | Module donor, not the native compiler |
| `slides-ai-plugin` | TypeScript helpers, font measurement and layout checks; helper execution uses Bun and auto-installed packages [S08] | Measured text fitting, image/SVG utilities, layout helpers | Selectively port after tests; replace dynamic installation with explicit locked dependencies |
| PptxGenJS | Native PPTX construction and native chart APIs [S11] | Final package writer for the reference path | Dependency; smoke starter deliberately pins 4.0.0, which was available for local execution |
| `pptx-automizer` | Native template editing, import/merge, PptxGenJS integration, documented limits [S09] | Approved master/template workflow | Optional template backend, separately tested |
| PPTKit | Pre-release authoring/IR/export pipeline, SVG preview, layout separation; roadmap includes charts and deferred import features [S04] | Alternative scene/export backend and layout ideas | Early backend experiment; native charts, font fit, and anchored connectors must be fixture-tested on the exact package/commit |
| PPTKit Presentation | Local review workflow and explicit export; preview is not a fidelity oracle [S05] | Review UX, session organization, input provenance ideas | Experimental review adapter, not a lossless importer |
| Presenton | Template-based generation/editor, REST and MCP, custom template workflow; Apache-2.0 [S13] | Existing team-facing UI and alternative full-deck generation | Run as a separate local service; do not assume it accepts DeckSpec or provides lossless arbitrary editing |
| PPTAgent/DeepPresenter | Research workflow plus published advisories and an identified fix [S10] | Visual ideation/evaluation experiment | Isolated research track; no default access to company data |

**Fork policy:** fork repositories only when maintaining patches. Otherwise pin a release or commit, or keep a source checkout for evaluation. Ten permanent forks would create more maintenance than useful capability.

### 3.2 Audit pins

These are repository commit IDs read from GitHub during the audit, not file/blob hashes:

| Repository | Recorded HEAD |
|---|---|
| `Astralune-ai/Astra-slide-impeccable` | `7425bb043d59bde2e84cf6d7d7685e451d31f3ac` |
| `siril9/presentation-skill` | `311e29920c7c7ab37a93c12676bab7baecc0f4a6` |
| `pbakaus/impeccable` | `0a4e72a254f3b175c95b36b82e5f2e60fa63f116` |
| `openHacking/pptkit` | `72715ca460ce649f553848393de922c52f19cd34` |

`config/upstreams.json` records these. Other repositories intentionally have null revisions until acquisition; the fetch script resolves and records them in a local lock. A source-commit pin does not pin a separately downloaded installer binary, npm dependency tree, model, font, or Docker image. Record those separately.

## 4. Product boundary

### v0.1 must do

Accept a reviewed outline or structured content; capture a private brand pack; select an appropriate composition; output a native editable widescreen PPTX; show a gallery/contact sheet; identify unsupported capabilities and unverified checks. A consultant should be able to change a heading, a hostname, a table cell, and a chart value without regenerating the deck.

### v0.1 deliberately does not promise

Lossless arbitrary-PPTX import, full PowerPoint animation translation, SmartArt editing, embedded Office objects, font embedding, universal HTML-to-OOXML conversion, multi-user real-time editing, or Word/Excel authoring. This is **PowerPoint-first**, not general Office support. Those formats require their own document models and renderers.

### User-facing modes

The user chooses a purpose, not an engine:

| Mode | Design priority | Editing contract |
|---|---|---|
| Client handoff | Clear argument and controllable detail | Essential text, tables, charts and diagram labels native |
| Technical workshop | Architecture, dependencies, readable labels | Native nodes/labels; anchoring requirements declared explicitly |
| Keynote/web | Strong composition and optional movement | Native critical text; decorative artwork may be SVG/image |

A separate editability setting may tighten these requirements. It must never silently downgrade a chart to a screenshot.

## 5. Architecture and ownership

```text
Untrusted inputs                         Private brand pack
(notes, documents, old decks)             (approved, versioned)
          |                                      |
  safe extraction + provenance             brand resolver
          |                                      |
          +------------> Presentation director <-+
                           |              |
                     approved story    DesignIntent
                           |              |
                           +------ DeckSpec
                                      |
                    semantic/evidence/brand validation
                                      |
                 structure selection + capability planning
                                      |
                         measured layout compilation
                                      |
                            ResolvedScene (points)
                              /               \
                  reference PPTX writer     SVG/HTML preview
                              |
                       final artifact render
                              |
             object checks + visual review + Office probe
                              |
                        delivery manifest
```

Parallel experiments receive **frozen inputs** and produce independent candidate decks and reports. They do not overwrite the active deck or each other's workspace.

### Three separations are mandatory

**Meaning versus geometry.** The planner decides that a slide compares current and target states. The compiler decides coordinates, line breaks, and object sizes. A free-form JSON field containing arbitrary JavaScript is not a compiler interface.

**Design intent versus brand authority.** Impeccable can propose a treatment. It cannot replace an approved corporate font, invent a new logo lockup, or remove a required disclaimer because a generic anti-pattern rule dislikes it.

**Preview versus deliverable.** A clean browser render is useful design evidence. The actual PPTX is the Office deliverable and needs its own tests.

## 6. Data contracts

Use TypeScript in the production packages and JSON Schema for interchange/validation. The included smoke harness is small plain ESM JavaScript so it can execute without a build chain; its `0.0.1-smoke` input is **not** the future production schema.

### 6.1 DeckSpec: semantic source

```ts
interface DeckSpec {
  schemaVersion: "1.0";
  id: string;
  revision: number;
  locale: string;
  canvas: { widthPt: number; heightPt: number };
  brief: {
    audience: string[];
    desiredDecision: string;
    mode: "client-handoff" | "technical" | "keynote";
  };
  brand: { id: string; version: string; digest: string };
  editability: "strict-native" | "balanced" | "visual";
  slides: SlideSpec[];
  evidence: EvidenceRecord[];
  assets: AssetRecord[];
}

interface SlideSpec {
  id: string;
  role: string;
  headline: string;
  takeaway: string;
  structure: { id: string; version: string; variant?: string };
  content: unknown; // Validated against that structure's schema, never arbitrary code.
  evidenceIds: string[];
  notes: string;
  requiredCapabilities: string[];
  overrides?: ApprovedOverride[];
}
```

Every source fact is either supported, explicitly supplied-but-unverified, an assumption, or synthetic test data. Keep these statuses distinct. A polished headline is not permission to strengthen a technical claim.

### 6.2 Evidence and assets

```ts
interface EvidenceRecord {
  id: string;
  claim: string;
  status: "supported" | "provided-unverified" | "assumption" | "synthetic";
  sourceId?: string;
  locator?: { page?: number; slide?: number; section?: string };
  retrievedAt?: string;
  sensitivity: "public" | "internal" | "confidential";
}

interface AssetRecord {
  id: string;
  contentHash: string;
  mediaType: string;
  localPath: string; // Validated beneath an approved asset root.
  origin: string;
  licenseStatus: "approved" | "restricted" | "unresolved";
  allowedOutputs: ("private" | "public")[];
  altText: string;
}
```

Do not put confidential file paths or private URLs into public speaker notes. Export uses a separate source-display policy. Private corpus indexes and their embeddings are private assets too.

### 6.3 DesignIntent: constrained creative direction

Use explicit options and constraints rather than arbitrary numbers such as `asymmetry: 0.35` that no renderer knows how to honor.

```json
{
  "treatment": "technical-editorial",
  "densityProfile": "technical-readable",
  "compositionPreferences": ["large-diagram", "asymmetric-title"],
  "allowedBackgrounds": ["brand.surface", "brand.inverseSurface"],
  "imageryPolicy": "approved-technical-illustration",
  "motionPolicy": "optional-reveal",
  "protectedBrandRules": ["primary-font", "logo-clearspace"]
}
```

The meaning and valid values of each field are owned by the compiler. Unknown fields fail validation rather than becoming undocumented prompts.

### 6.4 ResolvedScene: deterministic geometry

Use **points** internally: 72 points = one inch; a typical 16:9 canvas is 960 × 540 points. Convert to PptxGenJS inches only at the exporter boundary. SVG previews use the same numerical `viewBox`; choose the displayed browser scale independently.

A scene contains text boxes with measured lines, shape primitives, graph edges, charts, tables, image placements, clipping/stacking information, and explicit group IDs. It records the **resolved** font identity and metrics fingerprint, not just a preferred family name.

```ts
interface ResolvedElement {
  id: string;                 // Stable semantic ID.
  sourceSlideId: string;
  kind: "text" | "shape" | "edge" | "chart" | "table" | "image";
  box: { xPt: number; yPt: number; wPt: number; hPt: number };
  z: number;
  groupId?: string;
  intentionalOverlapWith?: string[];
  payload: unknown;          // Discriminated, validated union in implementation.
  provenance: { contentIds: string[]; structureVersion: string };
}
```

Intentional overlaps include labels over panels, nested groups, background decoration, and connector/node contact. A blanket “zero overlaps” test would reject correct slides.

### 6.5 Capability negotiation

Capabilities are exact contracts, not uncalibrated floating-point scores:

```text
text.native
chart.bar.native
chart.workbook.editable
table.native
shape.native
connector.native-line
connector.anchored
group.native
image.svg
notes.native
template.master-preserved
animation.reveal-native
```

An adapter returns `supported`, `unsupported`, or `degraded` for each requirement, with a reason and tested fixture ID. A native line is not an anchored connector. An SVG image is not a collection of editable diagram nodes. Native-looking text drawn into a bitmap is not native text.

```ts
interface PptxBackend {
  id: string;
  version: string;
  probe(plan: RenderPlan): CapabilityReport;
  render(plan: RenderPlan, scene: ResolvedScene): Promise<ArtifactBundle>;
}
```

`RenderPlan` selects one final package writer. In balanced mode, decorative illustration may be flattened only where declared. Essential labels/data cannot be flattened merely to pass visual QA.

## 7. Brand and voice capture

No actual Ferroque template, brand guide, or approved example deck was supplied for this audit. Earlier descriptions of its “voice” were not a validated brand specification. The public demo palette is synthetic and must not become an implicit company default.

### Private brand pack

```text
ferroque-brand/                 # Separate private location/repository
  manifest.json
  visual.tokens.json
  layout-policy.json
  voice.md
  terminology.json
  examples/                    # Explicitly approved, rights-reviewed
  templates/company-master.pptx
  assets/logos/
  fonts.manifest.json          # Font names/hashes/install policy, not public binaries
  evidence/brand-decisions.json
```

Capture more than colors. Record hierarchy, spacing relationships, diagram language, image treatment, acceptable density, logo placement/clearspace, co-branding, title style, preferred metaphors, approved unusual layouts, and examples of what the company rejects.

For voice, collect approved and rejected pairs with reasons. Examples should cover technical recommendations, executive summaries, claims/qualifiers, slide headlines, speaker notes, and calls to action. Have a company reviewer approve the extracted rules.

### Approval precedence

1. Legal, contractual, confidentiality, accessibility and content-integrity requirements.
2. Approved brand rules and approved co-branding exceptions.
3. The user's explicit brief and locked facts.
4. Structure requirements and audience/readability constraints.
5. Impeccable and upstream aesthetic suggestions.

Conflicts between higher-level requirements must be surfaced, not resolved by silently changing company identity. A required corporate font beats a generic “avoid this font” instruction. It still must be measured and readable.

### Brand does not mean one template

Start with three **brand-compatible treatments**: executive editorial, technical/diagram-led, and keynote/high-impact. A treatment changes composition, rhythm, image use and emphasis—not the identity system. Show real-content previews for brand approval.

Voice tests should check factual preservation and brand preference separately. A rewrite that scores well on style but changes an assumption into a promise fails.

## 8. How to preserve Astra's graphics without losing editability

Astra should contribute actual visual vocabulary, not merely a list of diagram names. Its porting work is a first-class workstream.

### 8.1 Structure pack contract

```text
packs/transformation-bridge/
  manifest.json
  content.schema.json
  compose.ts
  styles.json
  static-state.json
  fixtures/minimal.json
  fixtures/normal.json
  fixtures/dense.json
  fixtures/long-labels.json
  tests/contract.test.ts
  previews/                   # Generated from approved fixtures
  PROVENANCE.md
```

The public pack must identify copied/adapted material and its permission. It must not redistribute unapproved fonts, branded examples, sample numbers, or externally hosted images accidentally.

### 8.2 Porting workflow

**Inventory.** Inspect SVG nodes, CSS, external URLs, fonts, scripts, sample data, and animation targets. Record the source commit and structure file. Do not run arbitrary downloaded HTML with access to company files.

**Separate content from decoration.** Assign semantic slots to headings, labels, metrics, notes, nodes, and connectors. Decorative grids, textures, glow, particles and art occupy different layers from factual text.

**Freeze a canonical state.** An animation may begin with every element at opacity zero and counters at zero. Define a deterministic presentation-ready state. Do not screenshot an arbitrary animation timestamp or depend on undocumented global GSAP timelines.

**Re-layout for PowerPoint.** The inspected `04-bridge.html` contains small labels in a 1400-unit-wide SVG [S02]. Scaling an 8-unit label to a 960-point-wide slide yields approximately 5.5 points. A faithful coordinate copy can therefore be visually attractive but unusable in a meeting. Re-compose the same idea with fewer items, larger labels, and deliberate spacing; split a dense concept when necessary.

**Compile native essentials.** Use native text, shapes and chart/table objects for content. Build editable connectors only when the backend supports the required behavior. Keep complex decorative paths or artwork as permitted SVG/raster assets.

**Compare and approve.** Review the source design, the brand-transformed version, browser preview, and actual exported PPTX render. Approve the composition and native-object contract independently.

### 8.3 First pack portfolio

| Structure | Initial treatment | Native contract | Decorative escape hatch |
|---|---|---|---|
| Transformation bridge | Directional current → transition → target | Text, stages, panels and key relationships | Bridge arc/glow may become artwork |
| Hub-and-spoke | Ecosystem or service dependencies | Nodes/labels; edge requirements declared | Decorative orbit/background |
| Architecture layers | Control, access, workload and operations | All labels and layers | Optional technical texture |
| Comparison matrix | Decision criteria and options | Real table or explicitly editable shapes | None for factual cells |
| Roadmap/swimlane | Stages, owners, dependencies | Milestones, labels, lanes | Decorative path allowed |
| Dashboard | Evidence, metrics, charts | Native metrics and supported charts | Non-data accent art |
| Funnel | Concept or measured conversion | Native stages; numeric area semantics only when justified | Surface styling |
| Editorial hero | Thesis, image, oversized typography | Native title/takeaway | Large illustration/photo |

A pretty conceptual funnel must not imply quantitatively accurate segment areas unless the data and geometry support that interpretation. Treat radar/dashboard source graphics with the same distinction.

### 8.4 Motion

Browser animation is an optional second channel. Native PPTX initially exports the final static composition or explicit progressive-build slides. GSAP timelines are not automatically translated into PowerPoint effects. Native animation support, when added, needs a separate capability and relationship-ID test suite.

## 9. Layout, type, charts and templates

### Layout algorithm

1. Choose a structure variant that can contain the content.
2. Resolve brand tokens and fonts.
3. Measure actual runs, including bold spans, punctuation, line spacing and padding.
4. Allocate visual regions and fit within semantic groups.
5. Route graph edges; preserve direction, cardinality and grouping.
6. Check boundaries and unintended collisions.
7. On failure: use a different approved variant, shorten only with approval, or split the slide.
8. Export and verify the resulting file.

Do not repeatedly shrink all text until it fits. Minimum sizes are audience-specific brand policy. Start with conservative editable text defaults, then tune them through projector/desktop tests. Browser/canvas measurements are estimates of Office behavior, not a substitute for final rendering.

### Charts and tables

Keep dataset values and series labels in DeckSpec. Use native charts with embedded editable data for supported types. Chart counts alone do not prove that PowerPoint's **Edit Data** works. Test workbook values and perform a manual edit/save probe. Data-rich tables must keep their cell structure, not become a group of visually similar screenshots.

PPTKit's current roadmap lists native bar/line/pie charts as implemented, while its top-level documentation does not establish broad chart-type parity with PptxGenJS [S04]. Verify the precise npm release or source build. Do not claim either “no charts” or “complete chart support” based only on a headline.

### Company templates: three explicit lanes

**Reconstructed theme:** extract an approved visual specification and rebuild a native theme. This is a design reconstruction, not preservation of the original master.

**Native-template path:** use approved existing slides/layouts through `pptx-automizer`. Inventory placeholders, relationships, special objects and animations. Verify theme inheritance and that adding a new slide behaves acceptably.

**Preserved slide:** retain a complex slide as a restricted/imported element only when necessary. Declare limited editing; never count it as equivalent to a fully rebuilt native slide.

Template intake must return a compatibility report before promising preservation. `pptx-automizer` specifically documents restrictions on layouts and animation references [S09].

## 10. Experimental engines without architectural lock-in

### PPTKit experiment

Run the same fixtures through a pinned source/package build. Test rich text, nested grouping, native chart data, merged table cells, anchored connectors, notes, SVGs and font fallback. Compare final PowerPoint renders—not only its workbench SVG output. Promote it if it materially simplifies the scene/export path while satisfying the contract; otherwise retain the PptxGenJS backend.

Do not create a universal bidirectional IR converter. Implement a documented subset from our resolved scene to PPTKit and fail on unsupported fields.

### Presenton experiment

Use it as an independent full-deck generator/editor and a possible future UI. Its API can accept slide Markdown, but that is not a promise to preserve every element of our DeckSpec or every word without rewriting [S13]. Freeze inputs, inspect exported content, and compare against the reference backend.

A UI integration is not “easy wrapping.” It needs ownership of edits, job state, authentication, customer isolation, and content round-tripping. Only choose it as the team interface after those behaviors are demonstrated.

### Skill orchestration

Give the main skill a short routing document and load upstream references only for the task at hand. Design, planning, evidence review, and export are roles, not necessarily separate paid model calls. Start with an agent-driven CLI workflow; introduce direct provider integrations only when unattended operation is actually required.

Never inherit an upstream author's personal preferences, local paths, preferred image model, language defaults, or output-lane rules accidentally.

## 11. Quality and release evidence

A successful build is not a successful deck. Use explicit states:

```text
DRAFT → STORY_APPROVED → COMPILED → RENDERED → REVIEWED → RELEASED
                                        ↘ NEEDS_FIX
```

A skipped or unavailable check is `NOT_RUN`, never `PASS`.

| Gate | Automated checks | Human/application evidence |
|---|---|---|
| Content | Numeric consistency; required evidence; forbidden placeholders; changed-claim diff | Technical owner approves unsupported claims/assumptions |
| Brand/voice | Allowed tokens/fonts; protected strings; terminology; required marks | Brand reviewer approves treatment and phrasing |
| Geometry | Bounds; intended-overlap exceptions; text-fit estimates; object limits | Inspect all rendered slides at presentation scale |
| Office package | XML/package relationships; notes; charts/tables/workbooks; external links/macros policy | PowerPoint opens without repair; edit/save/reopen probe |
| Design | Density, hierarchy and repeated-layout diagnostics | Side-by-side preference test against an approved design baseline |
| Privacy | Output/log/artifact classification; asset rights; publication allowlist | Release owner approves intended recipient scope |

### Bounded repair

Proposed default: one initial render, one batched correction, one confirming render. Further passes require a visible blocker and an explicit budget increase. Re-render only affected slides where possible. Cache resolved assets and measurements by content/font/brand/compiler hashes. Record model, prompt version, cost and elapsed time without leaking private prompts into public CI.

### Aesthetic acceptance, not only lint

Use a frozen 12–20-slide benchmark covering all supported structures and both light/dark treatments. Ask at least a technical reviewer and a brand reviewer to compare the new output with approved examples. Suggested pilot targets: no critical defects; a clear majority of pairwise design preferences for the hybrid; median cleanup below ten minutes for a 10–15-slide deck. These are proposed project targets, **not measured results**.

### Manual edits after delivery

Keep generated source authoritative **until** someone edits the PPTX. Save output digests and warn before overwriting a changed artifact. v0.1 does not promise automatic reconciliation. Offer a new output filename and a controlled re-import/review path. Stable object IDs aid future reconciliation but do not solve it by themselves.

## 12. Security, privacy and distribution

Separate the public framework from private brand packs, customer inputs, output decks, visual goldens, embeddings, logs and credentials. `.gitignore` is a convenience, not the boundary: use external directories and CI publication allowlists.

Treat source files and HTML as untrusted. Before production ingestion, enforce archive size/entry/decompression limits, path confinement, XML entity/DTD policy, relationship allowlists, macro/embedded-object policy and asset type checks. Render in an isolated worker with a disposable writable directory, resource limits, no Docker socket, and no mounted home directory. Disable renderer networking; use a separate controlled fetch/model stage when necessary.

The provided local smoke scripts are for **trusted generated fixtures**. They are not a hardened arbitrary-file ingestion sandbox.

Self-hosted Presenton or a local preview does not automatically mean prompts stay local. Model, image, search, telemetry and font requests need separate policies. Start external services on loopback and with synthetic data. Do not log API keys or bake them into generated HTML.

For PPTAgent, verify the selected revision contains the published fixes and review the other advisories before execution. The code-execution advisory identifies `418491a9a1c02d9d93194b5973bb58df35cf9d00` as patched [S10]. That is not a blanket security certification.

### Rights policy

The framework can be open source and company packs can remain private. Keep dependency/asset provenance, original notices, and per-file licensing. No applicable Astra redistribution grant was established in this audit. Viewing or maintaining a GitHub-hosted fork is not equivalent to unrestricted copying into a differently licensed distribution; an adapter does not change that [S14]. Resolve permission for exact reusable files while developing the compiler and licensed packs in parallel.

Do not redistribute font files. Record approved font names, licenses/install requirements and fingerprints; let the user or company provision them.

## 13. Proposed repository evolution

```text
deckforge/
  ARCHITECTURE.md
  DEVELOPMENT_PLAN.md
  AGENTS.md
  skills/deckforge/
  config/upstreams.json
  packages/
    contracts/          # DeckSpec, BrandSpec, Scene, diagnostics
    compiler/           # structure selection and deterministic layout
    renderer-pptx/      # reference backend
    preview/            # scene-based SVG/HTML review
    brand/              # token/voice resolution
    ingest/             # safe source extraction, not arbitrary round-trip
    qa/                 # package, geometry, evidence, receipts
    adapters/           # bounded upstream contracts
  packs/
    core/               # original/permitted implementation
    consulting/
  examples/             # synthetic inputs only
  tests/
  scripts/
```

Start with a few packages once boundaries need enforcement; do not create a microservice per agent. The starter has only the smoke scripts, tests and documents. Empty/planned modules are not represented as implemented functionality.

## 14. Architecture decisions to preserve

- **ADR-001:** own semantic content and resolved geometry; do not expose an upstream engine IR as the user document format.
- **ADR-002:** one package writer per PPTX; multiple composition providers are allowed.
- **ADR-003:** design quality and native editability are independent release requirements.
- **ADR-004:** actual PPTX rendering is distinct from browser preview.
- **ADR-005:** beta components are allowed, versioned, sandboxed where necessary, and evaluated against the same fixtures.
- **ADR-006:** approved brand rules override generic design advice.
- **ADR-007:** company content, fonts, customer assets and private examples stay outside the public source tree.
- **ADR-008:** no silent flattening, no fictitious evidence, no hidden rewrite during layout repair.
- **ADR-009:** portable CLI/skill first; UI integration is a separate product decision.
- **ADR-010:** imported manual edits and preserved template content have explicit limits.

## 15. Source register

Primary sources inspected on 2026-09-15. Descriptions above distinguish upstream documentation from tests actually executed in this package. Upstream `main` and published packages may diverge; use the recorded pins and local acquisition locks for reproduction.

- **S01 — Astra workflow:** [README](https://github.com/Astralune-ai/Astra-slide-impeccable/blob/7425bb043d59bde2e84cf6d7d7685e451d31f3ac/README.md).
- **S02 — Astra implementation:** [Bridge source](https://github.com/Astralune-ai/Astra-slide-impeccable/blob/7425bb043d59bde2e84cf6d7d7685e451d31f3ac/structures/04-bridge.html).
- **S03 — Impeccable:** [README](https://github.com/pbakaus/impeccable/blob/0a4e72a254f3b175c95b36b82e5f2e60fa63f116/README.md), [package manifest](https://github.com/pbakaus/impeccable/blob/0a4e72a254f3b175c95b36b82e5f2e60fa63f116/package.json).
- **S04 — PPTKit:** [README](https://github.com/openHacking/pptkit/blob/72715ca460ce649f553848393de922c52f19cd34/README.md), [roadmap](https://github.com/openHacking/pptkit/blob/72715ca460ce649f553848393de922c52f19cd34/ROADMAP.md). Note documentation drift: README describes IR v2; roadmap foundation still names v1. Verify the exact API rather than relying on the label.
- **S05 — PPTKit Presentation:** [README and development workflow](https://github.com/openHacking/pptkit-presentation/blob/main/README.md).
- **S06 — Knowledge Cat:** [README and native-lane prerequisite](https://github.com/gnipbao/knowledge-cat-ppt-skill/blob/main/README.md).
- **S07 — presentation-skill:** [README](https://github.com/siril9/presentation-skill/blob/311e29920c7c7ab37a93c12676bab7baecc0f4a6/README.md), [package scripts and dependencies](https://github.com/siril9/presentation-skill/blob/311e29920c7c7ab37a93c12676bab7baecc0f4a6/package.json).
- **S08 — slides-ai-plugin:** [PPTX skill and helper API](https://github.com/proyecto26/slides-ai-plugin/blob/main/skills/pptx-slides/SKILL.md), [repository](https://github.com/proyecto26/slides-ai-plugin).
- **S09 — pptx-automizer:** [README](https://github.com/singerla/pptx-automizer), [limitations](https://singerla.github.io/pptx-automizer/limitations), [masters/layouts](https://singerla.github.io/pptx-automizer/masters-layouts).
- **S10 — PPTAgent:** [advisories](https://github.com/icip-cas/PPTAgent/security/advisories), [code-execution advisory and patch](https://github.com/icip-cas/PPTAgent/security/advisories/GHSA-89g2-xw5c-v95p).
- **S11 — PptxGenJS:** [quick start](https://gitbrent.github.io/PptxGenJS/docs/quick-start/), [native chart API](https://gitbrent.github.io/PptxGenJS/docs/api-charts/).
- **S12 — Agent Skills:** [specification](https://agentskills.io/specification).
- **S13 — Presenton:** [README, Docker, authentication, modes and API](https://github.com/presenton/presenton/blob/main/README.md).
- **S14 — GitHub:** [licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

## 16. Audit execution record

The accompanying prototype was executed locally with Node 22.16.0, Python 3.13.5 and the environment's preinstalled PptxGenJS 4.0.0. Thirteen validation tests passed. A six-slide native PPTX was generated and structurally inspected: 45 native text boxes, one native table, one native chart, one embedded workbook, six notes parts and zero picture objects. LibreOffice produced all six preview pages, and a contact sheet was visually reviewed.

Not executed: a clean online dependency installation, any full upstream test suite, Presenton/PPTKit integration, actual corporate-template ingestion, or Microsoft PowerPoint edit/save verification. Network access from the runtime was unavailable, although web/GitHub research tools were available. The included prototype is a starting acceptance fixture—not evidence that the proposed hybrid system is already built.
