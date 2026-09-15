# Shared contracts and implementation conventions

**Platform revision:** windows-office-1. **Status:** proposed public interfaces; no application implementation is supplied in this pack. These contracts refine the accompanying audited architecture. They are the single reference for field names, units, identity, approval and capability behavior across the component specs.

## 1. Non-negotiable boundaries

Meaning belongs to DeckSpec; coordinates belong to the compiler; one selected backend writes a complete PPTX. Company brand authority is distinct from design advice. A browser preview is distinct from a render of the actual PPTX. PowerPoint desktop is the primary final-artifact renderer for the Windows profile; LibreOffice is a separately labeled portability comparison. Content extraction, visual reconstruction and original-template preservation are separate operations.

The synthetic smoke schema and its fixed 0–100 chart range are not production restrictions. The original validator and renderer remain a regression harness during migration. Existing public files are listed in [STARTER_INVENTORY.md](references/STARTER_INVENTORY.md).

## 2. Common representation

| Concern | Contract |
|---|---|
| Interchange | UTF-8 JSON with explicit schemaVersion; Markdown for human story/voice/review documents |
| Initial production schema | `"1.0"`; the starter remains `"0.0.1-smoke"` |
| Validation | One authoritative schema source plus verified/generated TypeScript types; unknown fields rejected except explicitly versioned extension registries |
| Identity | Nonempty IDs matching `[A-Za-z][A-Za-z0-9._:-]*`; stable through label edits, reorder and re-layout |
| Namespace | Deck, slide, content, node, edge, evidence, source, dataset and asset IDs have explicit domains; validate all cross-references |
| Geometry | Points internally, 72 points per inch; demo canvas 960×540 points; no mixed-unit scene fields |
| Numbers | Finite values only; explicit null for missing data; never conflate null with zero |
| Versions | Exact brand/pack/backend version and content digest, not a moving label alone |
| Canonical hashing | Deterministic key order, meaningful array order retained, UTF-8 encoding, SHA-256; canonicalization implementation/version recorded |
| Timestamp policy | Timestamps belong to manifests/receipts; do not introduce current time into layout output or source digests |
| Diagnostics | Stable code, severity, affected IDs, JSON pointer where possible, safe user message and proposed next action |

Schema extensions are registered and versioned. An unrestricted `metadata` object is not an escape hatch for executable source or backend options. Serialized documents contain no functions, arbitrary JS/Python, shell commands or unsanitized markup to execute.

## 3. Semantic document

The following defines the envelope, not a complete compilable TypeScript module. DF-01 owns the actual schemas and exported types.

```ts
interface DeckSpec {
  schemaVersion: "1.0";
  id: string;
  revision: number;
  locale: string;
  canvas: { widthPt: number; heightPt: number };
  brief: Brief;
  brand: { id: string; version: string; digest: string };
  editability: "strict-native" | "balanced" | "visual";
  slides: SlideSpec[];
  evidence: EvidenceRecord[];
  assets: AssetRecord[];
  datasets: DatasetRecord[];
}
interface Brief {
  audience: string[];
  desiredDecision: string;
  mode: "client-handoff" | "technical" | "keynote";
}
interface SlideSpec {
  id: string;
  role: string;
  headline: string;
  takeaway: string;
  structure: { id: string; version: string; variant: string };
  content: StructureContent;
  evidenceIds: string[];
  notes: string;
  requiredCapabilities: CapabilityId[];
  overrides?: ApprovedOverride[];
}
```

`StructureContent` is a discriminated schema resolved by exact structure ID/version; it is not arbitrary unchecked JSON. Content blocks, list items, nodes, table rows/cells, chart series and meaningful values have stable IDs. A headline may keep its ID when wording changes, but the revision/content digest changes.

`DatasetRecord` keeps categories, series IDs, finite values or null, units, period/cohort where applicable, evidence bindings and explicit display/axis policy. Retain original numeric lexemes in extraction provenance when precision/format matters. A formatter may display `1.2k` only through an approved format rule; the dataset remains 1200.

Reorder preserves identity. A split produces derived slide IDs with `derivedFrom` information in the migration/patch report. No implicit renumbering of source references. Notes are never harvested from unrelated reference decks.

## 4. Source, evidence and asset contracts

`SourceManifest` is job-private and contains source IDs, content hashes, logical filenames, media types, sensitivity, extraction version and source locators. The deck uses source IDs, not uncontrolled absolute paths. A source’s private path is resolved only by the job store.

An evidence record has:

- `id`, `claim`, `status` (`supported`, `provided-unverified`, `assumption`, `synthetic`) and `sensitivity` (`public`, `internal`, `confidential`).
- One or more source ID/locator bindings when present. Locator types include Markdown line/span, original PPTX slide/object, document page/section and a separately controlled external citation.
- Review/verification metadata for supported claims. A source’s existence does not prove the claim; registration alone cannot promote status.
- A safe display label policy for the intended audience. Private locators remain private even if a footnote is shown.

This formalizes multi-source evidence and source-locator bindings beyond the architecture’s illustrative single-source example. DF-01 must choose one schema representation and use it consistently; these are not already-implemented migration rules.

An asset record has `id`, `contentHash`, verified `mediaType`, root-confined `localPath`, `origin`, `sensitivity`, `licenseStatus` (`approved`, `restricted`, `unresolved`), `allowedOutputs` (`private`, `public`), `altText` and any approved crop/focal metadata. Paths are relative to an approved asset root and must survive realpath/symlink/junction/reparse-point confinement and Windows alias/ADS/case-collision checks. Logical IDs never become raw physical filenames. A hash is integrity metadata, not permission.

Output eligibility combines rights, sensitivity, approved recipients and source-display policy. “Private” does not authorize sending any company content to any external recipient. Derived charts, screenshots, embeddings, previews and logs inherit source classification unless explicitly reviewed for declassification.

## 5. Brand and voice authority

A private `BrandSpec` includes manifest/version/digest, visual tokens, layout/readability policy, approved treatments, voice rules, terminology, font manifest, approved examples, template references and decision records.

Rule authority and approval are separate:

| Field | Purpose |
|---|---|
| Authority | `official`, `observed`, `proposed`, `deprecated` |
| Approval | Candidate, approved or rejected; reviewer/date and exact rule/pack digest |
| Confidence | Inference confidence where meaningful; never a substitute for approval |
| Provenance | Source ID, locator and rationale |
| Protection | Whether a generic design suggestion may override the rule |

Precedence: legal/confidentiality/content-integrity and required accessibility constraints → approved brand/co-brand rules → user brief and locked facts → structure/readability constraints → optional upstream aesthetic advice. Conflicts among protected requirements are errors requiring a decision, not permission to silently discard one.

Initial treatment IDs: `executive-editorial`, `technical-diagram`, `keynote-impact`. Initial density profiles: `executive-readable`, `technical-readable`, `data-readable`. Actual sizes/palette/fonts are values in the approved pack, not fixed company assumptions in code. The demo pack may have its own explicit synthetic values.

Co-branding names exact allowed marks, placements, sizes and color interactions. No opportunistic borrowing of customer colors or fonts from an unrelated project.

## 6. DesignIntent

```ts
interface DesignIntent {
  treatment: "executive-editorial" | "technical-diagram" | "keynote-impact";
  densityProfile: "executive-readable" | "technical-readable" | "data-readable";
  compositionPreferences: CompositionPreference[];
  allowedBackgrounds: BrandTokenReference[];
  imageryPolicy: "none" | "approved-technical-illustration" | "approved-photography";
  motionPolicy: "none" | "optional-reveal";
  protectedBrandRules: string[];
}
```

Initial composition preferences are explicit supported values such as `large-diagram`, `asymmetric-title`, `direct-labels`, `lead-metric` and `editorial-type`. Packs declare which preferences they can honor. Unknown values are rejected rather than silently ignored. The compiler can explain that a requested preference is incompatible with content capacity.

A design proposal cannot override a required font, add a logo, strengthen a claim or change a dataset. The Impeccable adapter is a proposal producer, not a second authority or a validator of Office packages.

## 7. LayoutDraft, measurements and ResolvedScene

`LayoutDraft` is the composition/compiler boundary. It contains canvas regions, semantic groups, element requests, constraints, content IDs and variant identity. Region constraints are a closed data vocabulary (fixed bounds, alignment, gaps, containment and ordering), not code or string expressions to evaluate. Initial implementations may use simple deterministic geometry functions inside reviewed packs; do not build a general constraint language first.

`TextMeasurement` records actual resolved font/weight identity and fingerprint, content/runs, line breaks, baseline/advance metrics, padding, line spacing and provider version. Metrics are estimates of application rendering; final PPTX rendering remains an independent check.

`ResolvedScene` is immutable compiler output with deck/revision, canvas, brand/intent/pack/font/compiler digests and ordered slides. Each element has:

```ts
interface ResolvedElementBase {
  id: string;
  sourceSlideId: string;
  kind: "text" | "shape" | "edge" | "chart" | "table" | "image";
  box: { xPt: number; yPt: number; wPt: number; hPt: number };
  z: number;
  groupId?: string;
  intentionalOverlapWith?: string[];
  provenance: { contentIds: string[]; structureVersion: string };
}
```

Payloads are validated discriminated unions. Text contains measured runs/lines; edges contain endpoint/port IDs and behavior; charts contain dataset/axis references; tables contain actual rows/cells/merges; images contain resolved asset/crop references. Groups are explicit, acyclic and distinct from visual containment.

A content coverage map relates every essential content ID to emitted elements. Decorations cannot claim to satisfy missing factual labels. Intentional overlap requires a specific allowed relationship; a background covering a whole slide cannot authorize every foreground collision.

Compiler outcomes: `FIT`, `ALTERNATIVE_REQUIRED`, `SPLIT_PROPOSED` or `FAILED`. Alternate/split proposals retain content and need workflow acceptance when the semantic slide structure changes. Text cannot be silently shortened or shrunk below approved policy.

## 8. Capability and backend contract

Capabilities are exact requirements, initially:

```text
text.native
shape.native
chart.bar.native
chart.line.native
chart.pie.native
chart.workbook.editable
table.native
table.merges.native
connector.native-line
connector.anchored
group.native
image.svg
notes.native
template.master-preserved
animation.reveal-native
```

The initial catalog can describe a capability before any backend supports it. An adapter must not advertise it until its fixture proves the behavior. A capability result is `supported`, `unsupported` or `degraded` with reason and fixture/environment evidence. Unverified capability is reported unsupported with reason `unverified`, not a fictitious pass.

`RenderPlan` identifies one backend ID/version, source/scene digests, requested capability requirements, declared optional degradations, static/motion mode and output scope. `PptxBackend.probe(plan)` runs before writing. `render(plan, scene)` returns `ArtifactBundle` with files/hashes, source-object mapping, capability outcomes and manifest.

Balanced mode permits complex decorative SVG/artwork with native labels/data. Strict-native does not ban legitimate photos/icons, but tightens editable diagram/shape requirements. Visual mode permits more illustration; it does not silently turn charts, tables or protected text into pictures. Any relaxation of essential editability must be an explicit approved contract change, not a renderer fallback.

Template assembly is a separately selected backend with one final package-ownership boundary. Internal use of another generator does not create permission for arbitrary foreign-slide merging.

## 9. Job state and revisions

Proposed private layout:

```text
<job-root>/<job-id>/
  job.json
  brief.json
  sources/manifest.json
  assets/manifest.json
  revisions/000001/{deck.json,story.md,design-intent.json}
  builds/<build-id>/{scene.json,render-plan.json,deck.pptx,preview/,build.json}
  qa/<build-id>/{content.json,geometry.json,office.json,visual-review.json}
  releases/<release-id>/{deck.pptx,manifest.json}
  events.jsonl
```

This expands the baseline’s illustrative flat job layout into immutable revision/build directories. Friendly `latest` pointers are metadata, not mutable overwrites of released files. Use same-volume atomic writes and optimistic revision checks; handle Windows file-sharing violations and use fresh paths rather than deleting lock files or overwriting an open Office document.

State progression: `DRAFT → STORY_APPROVED → COMPILED → RENDERED → REVIEWED → RELEASED`; failures go to `NEEDS_FIX` with retained last-good artifacts. Updating content returns the active revision to DRAFT. Re-layout can preserve story approval only when its bound content/meaning digest is unchanged; it invalidates downstream visual/artifact receipts. Released revisions remain immutable; new changes create a new revision.

Approval cannot be created by the same model marking its own output successful. The workflow records who/tool performed the review and what exact artifacts were reviewed.

## 10. Receipt invalidation

| Change | Must re-evaluate |
|---|---|
| Claim, number, notes, title or table text | Content/voice/story and all affected compiled/rendered/release evidence |
| Slide order | Narrative/story plus final artifact and order-dependent design evidence |
| Variant, geometry, imagery or font | Geometry, visual and final-render/Office evidence; preserve content approval only if semantic digest is unchanged |
| Brand tokens or protected rules | Brand resolution plus affected layout/voice/visual/release checks |
| Source bytes or evidence status | Evidence/content and downstream release eligibility |
| Backend/dependency/rendering app version | Backend capability, package and application-render evidence |
| Output recipient/publication scope | Rights/privacy/source-display/release checks |
| Manual edits to exported PPTX | External-edit warning; never overwrite or treat old receipt as applying to changed file |

Receipts bind exact dependency digests. Timestamps and filenames alone are not proof of freshness. Unknown impact invalidates conservatively and reports why; it does not silently retain approval.

## 11. QA and command results

Check states: PASS, FAIL, WARN, NOT_RUN. Required WARN behavior is policy-defined; required FAIL or NOT_RUN blocks approved export. A successful office-free-draft build and missing Office review are compatible only when labeled draft. The default windows-office release profile requires native PowerPoint rendering, save/reopen and applicable feature probes plus independent human review. Word intake is optional; Excel chart-data gates are required when editable chart workbooks are used.

```ts
interface OperationResult {
  command: string;
  status: "succeeded" | "failed" | "needs-review";
  jobId?: string;
  revision?: number;
  artifactIds: string[];
  diagnostics: Diagnostic[];
  nextActions: string[];
}
```

Exit codes: 0 requested operation succeeded; 2 invalid input/schema; 3 unsupported required capability; 4 render/QA failure; 5 missing required approval/dependency. A revision conflict is an invalid requested operation (2) with `REVISION_CONFLICT`. Egress/privacy policy denial is 5 with a specific diagnostic. CI/spec-test dispatcher failures use ordinary nonzero status and are not themselves the public CLI contract.

Repair budget defaults to one initial render, one batched approved correction and one confirming render. A different component cannot reset that shared counter. More work requires a recorded budget decision.

## 12. Implementation discipline

Start with contracts and the existing smoke harness. Create package boundaries only as features are implemented. The listed paths are ownership targets, not permission to generate empty scaffolding for every package. Keep one schema validator, one agreed test harness and one explicit package writer.

Current commands versus proposed commands are listed in [COMMANDS.md](COMMANDS.md). Specification validation only checks this documentation pack’s integrity; it is not application or Office verification.


## 13. Windows execution and Office environment contracts

The [Windows Office execution contract](WINDOWS_OFFICE.md) is normative for host/session/process/path behavior. [DF-20](core/20-windows-native-office-worker.md) implements the bridge; [DF-21](core/21-word-excel-native-intake.md) adds optional Word/Excel intake. DeckSpec and ResolvedScene remain portable and do not contain COM objects or raw Office commands.

`OfficeEnvironmentManifest` records `schemaVersion`, `id`, OS name/build/architecture, worker/protocol/PowerShell versions, interactive-session eligibility, per-application availability/edition/executable build/architecture/channel when known, locale, font profile, export dimensions/settings and policy digest. Unknown values remain explicit; no product-key/account credentials are serialized. Raw paths and process/user details stay in job-private diagnostics.

`OfficeRequest` and `OfficeResult` use the exact closed envelopes in WINDOWS_OFFICE. Operation names are `doctor`, `render-powerpoint`, `inspect-powerpoint`, `probe-save-reopen`, `probe-chart-data`, `probe-connectors`, `compose-template`, `extract-word`, `extract-excel`. Implement each operation with a discriminated parameters/result schema; unsupported operations fail. The worker executes reviewed code, never source text from a model.

`ApplicationReceipt` has `id`, `checkId`, `status`, `inputArtifactId`, `inputSha256`, optional distinct `probeArtifactId`/`probeSha256`, `environmentId`/digest, `policyDigest`, `workerVersion`, `operation`, output artifact hashes, affected slide/object IDs, reviewer/tool identity and cleanup outcome. Human UI/repair-warning review is not synthesized by an automated receipt.

Initial check IDs:

```text
powerpoint.render.png
powerpoint.render.pdf
powerpoint.objects.inspect
powerpoint.save-reopen
powerpoint.text-fit
powerpoint.table.edit
powerpoint.chart-data.edit
powerpoint.connector.move
powerpoint.group.edit
powerpoint.template.new-slide
powerpoint.ui.human-review
powerpoint.ui.no-repair-observed
word.source.extract
excel.source.extract
```

Check IDs are **application observations**, not writer capability IDs. They may be NOT_RUN without changing what a draft can build. Required check selection is feature/profile-based: chart workbooks require chart-data edit evidence, declared anchored diagrams require connector-move evidence, template preservation requires native new-slide evidence. An absent optional Word operation does not block a deck with no Word source.

The `windows-office` profile requires native PowerPoint evidence on the actual release bytes; `office-free-draft` never claims that status. Alternate Linux/macOS/LibreOffice outcomes are separately recorded. Exports do not downgrade profiles silently. A selected `powerpoint-template` backend owns its final native save; the default `pptxgenjs` backend does not gain capabilities from probe-copy repairs.

Office build/locale/font/export-setting changes invalidate related render/visual/capability receipts. A last-minute native save creates new artifact bytes: rehash and re-run final-byte checks. Save/reopen copies are evidence, not permission to overwrite the final build. Workspace source IDs containing colons map to safe filenames; JSON line endings/encoding rules stay canonical across shells.
