# Deckforge: development plan and project bootstrap

**Original audit date:** 2026-09-15.
**Platform revision:** windows-office-1, 2026-09-15. Primary environment: native Windows 11 x64 with installed desktop PowerPoint, Excel and Word. Implementation remains planned except the existing smoke starter.  
**Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md).  
**Scope:** open-source presentation framework; private company brand/voice packs; editable PowerPoint first; ambitious visual structures and beta backends explicitly included.


## Contents

- [1. Start with the right deliverable](#1-start-with-the-right-deliverable)
- [2. Toolchain and workspace](#2-toolchain-and-workspace)
- [3. Run the supplied starter](#3-run-the-supplied-starter)
- [4. Put the project under version control](#4-put-the-project-under-version-control)
- [5. Make the repository usable by a coding agent](#5-make-the-repository-usable-by-a-coding-agent)
- [6. Acquire upstream source without entangling runtimes](#6-acquire-upstream-source-without-entangling-runtimes)
- [7. Run the most useful upstream checks](#7-run-the-most-useful-upstream-checks)
- [8. Beta backend experiments run early](#8-beta-backend-experiments-run-early)
- [9. Delivery backlog: vertical slices and dependencies](#9-delivery-backlog-vertical-slices-and-dependencies)
- [10. Future CLI contract — TO IMPLEMENT](#10-future-cli-contract--to-implement)
- [11. Test matrix and benchmarking](#11-test-matrix-and-benchmarking)
- [12. First coding-agent assignment](#12-first-coding-agent-assignment)
- [13. What is verified in this delivery](#13-what-is-verified-in-this-delivery)
- [14. Primary sources](#14-primary-sources)

## 1. Start with the right deliverable

The first milestone is **a branded, visually distinctive, editable deck rendered and checked in desktop PowerPoint**, not a plugin installer that launches eight unrelated agents.

The supplied repository is a runnable **acceptance-fixture starter**, not the finished hybrid system. It establishes native text/shapes/charts/tables/notes, a small input validator, structural inspection, and local preview. Its six designs are original smoke fixtures, not Astra ports or a validated Ferroque template.

Every command below has one of three statuses:

| Status | Meaning |
|---|---|
| **RUN NOW** | Implemented in the supplied starter, or a documented upstream command clearly identified as such |
| **EXPERIMENT** | Optional upstream installation/execution; may need network, Docker, a model provider, or additional dependencies |
| **TO IMPLEMENT** | Proposed future interface or task; not a command that exists in this starter |

Do not call planned `/deck` commands and assume the product has been implemented. The initial skill tells a coding agent how to work on this repository; it does not yet accept arbitrary client material and generate a finished corporate deck.

## 2. Toolchain and workspace

The primary developer environment is **Windows 11 x64 and PowerShell 7** with native Windows Node/Python/Git. The chosen project lines are Node 24.x and Python 3.13.x; record and lock actual tested versions. Existing 22.x starter evidence remains historical, not Windows qualification. Company-approved desktop PowerPoint, Excel and Word are assumed deployed/licensed; verify actual edition/build/architecture rather than guessing.

| Tool/application | Required use | Scope |
|---|---|---|
| Node/npm/Git | Portable core, dependencies and source | Lock exact resolved dependencies; do not hardcode Linux shell commands |
| Python | Standard-library inspection and spec validation | Use `py -3` explicitly until a portable launcher is implemented |
| PowerShell 7 | Primary setup/developer shell | Prefer npm.cmd; do not bypass script policy |
| Windows PowerShell 5.1 STA | Planned DF-20 Office worker host | Explicit child process in signed-in desktop session |
| PowerPoint desktop | Native PNG/PDF, object/text inspection, edit/save probes and template operations | Primary final-artifact reference |
| Excel desktop | Native embedded chart data probes; optional source intake | No implicit external refresh or destructive edits |
| Word desktop | Optional native document intake | Not Word document generation |
| LibreOffice/Poppler | Optional portability comparison | Not the required Windows approval gate |
| Docker Desktop/WSL, pnpm, Bun | Separate optional upstream experiments | No Office/COM hosting in these environments |

[Windows setup](docs/specs/WINDOWS_SETUP.md) supplies exact PowerShell/WinGet/extraction/private-path/skill-copy commands. [Windows execution contract](docs/specs/WINDOWS_OFFICE.md) defines Office session/process policy and cites [Microsoft documentation](docs/specs/WINDOWS_SOURCES.md).

Use separate source/lab/private locations: `$env:USERPROFILE\04_Src\deckforge`, `$env:USERPROFILE\04_Src\deckforge-lab`, and `$env:LOCALAPPDATA\DeckforgePrivate\{brands,jobs}`. Validate actual ACL/local-storage/sync behavior; these example paths alone are not a privacy boundary. Office files use short local staged paths, safe filenames and hashes. UNC/cloud placeholders/WSL paths do not reach COM directly in v0.1.

## 3. Run the supplied starter

### 3.1 Extract and install — RUN NOW on the target, not executed here

The complete Windows bundle is `deckforge-windows-complete.zip`, with top-level `deckforge/`. Use [the guarded PowerShell extraction](docs/specs/WINDOWS_SETUP.md) into a new folder. For an existing checkout, stage `deckforge-windows-update.zip` and merge reviewed documentation changes; do not overwrite local source.

From the project root after installing Node/Python:

```powershell
if (Test-Path -LiteralPath '.\package-lock.json') { npm.cmd ci } else { npm.cmd install }
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
node --test .\tests\validate.test.mjs
if ($LASTEXITCODE -ne 0) { throw 'Baseline tests failed.' }
node .\scripts\build-smoke.mjs .\examples\smoke-deck.json .\out\smoke
if ($LASTEXITCODE -ne 0) { throw 'Baseline generation failed.' }
py -3 .\scripts\inspect-pptx.py .\out\smoke\deck.pptx
if ($LASTEXITCODE -ne 0) { throw 'Package inspection failed.' }
py -3 .\docs\specs\tools\validate_specs.py
```

PptxGenJS 4.0.0 remains the historical fixture pin, not a newest-release claim. Create and commit a real dependency lock after a reviewed successful install; no lockfile is fabricated by this documentation revision. The original smoke font is Liberation Sans, which must be checked locally. A separate Windows-font fixture is DF-00 work; substitution is a reported condition, not a silent baseline change.

### 3.2 Expected outputs

The unchanged fixture produces `out/smoke/deck.pptx`, `geometry.json` and `build.json`. The fixture inspector expects six slides, one native chart/table/workbook and six notes parts; it does not prove fitting, anchoring or native edit/save behavior. These are fixture counts, not restrictions on the future product.

### 3.3 Actual PowerPoint review now; automation in DF-20

Use desktop PowerPoint to open a probe copy, edit a heading/table cell/chart datum, save/close/reopen and inspect warnings. Export PNG/PDF through PowerPoint’s UI and review all pages. [Windows setup](docs/specs/WINDOWS_SETUP.md) provides copy/open commands. Keep the generated original immutable; altered probes are not release candidates.

The current `npm run inspect/check/preview` chains still call `python3`; `preview` still uses LibreOffice/Poppler. They have **not** become native Office commands. Use the explicit Windows commands above until DF-00 ports launchers. DF-20 will add PowerPoint PNG/PDF export directly through the object model, with no Poppler requirement for its PNG channel. Future `deck qa --render powerpoint` remains TO IMPLEMENT.

### 3.4 Baseline evidence

Record native PowerPoint/Excel behavior on the actual Windows Office/font/locale profile. Missing or unperformed checks remain NOT_RUN. Historical Linux rendering and existing documentation tests cannot be copied into a Windows PASS record. Source and baseline application code remain unchanged in this revision.

## 4. Put the project under version control

For a new extracted project only:

```powershell
git init -b main
git add README.md ARCHITECTURE.md DEVELOPMENT_PLAN.md AGENTS.md LICENSE THIRD_PARTY_NOTICES.md
git add package.json .gitignore .env.example src scripts tests skills config examples docs
if (Test-Path -LiteralPath '.\package-lock.json') { git add package-lock.json }
git diff --cached --stat
git diff --cached --name-only
git status --short
```

Review staged files before committing. No Office binaries, company template/fonts, private corpus, customer data, generated decks, temporary locks, credentials or private acceptance receipts belong in public source.

```powershell
git commit -m 'Document Windows-native Office architecture and implementation specs'
git switch -c feat/windows-baseline
```

For an existing repository, create a review branch and merge the staged document update rather than reinitializing/resetting it. Optional publication through an authenticated GitHub CLI remains explicit and separate; this delivery creates no remote or public repository. Source licenses/provenance remain unchanged; private brand/Office assets are not redistributed.

## 5. Make the repository usable by a coding agent

Follow the Windows setup's project-local copy installation for `skills/deckforge` into `.agents/skills/` or `.claude/skills/`. It works without symlink privileges; record the source/copy digest and refresh deliberately. The root AGENTS.md and skill now point to the Windows contract and 33-spec index. This is still a development skill, not a completed `/deck` product.

Impeccable remains a separately reviewed optional dependency. The prior audit's pinned launcher command, adapted to PowerShell invocation, is:

```powershell
npm.cmd exec --yes --package=impeccable@4.1.0 -- impeccable install --providers=claude,codex --scope=project
```

**EXPERIMENT, not Windows-tested here.** Verify installed engine/version and its actual Windows launcher; a launcher package pin does not pin every downloaded binary. Do not invoke Unix-only scripts in the native core or copy an upstream author's preferences into a brand pack. DF-05 owns the presentation-specific adapter and approved brand precedence.

## 6. Acquire upstream source without entangling runtimes

### 6.1 Fetch the first four checkouts — RUN NOW, requires network

The supplied script, invoked through `py -3` on Windows, clones source only. It does not install packages, load skills, or run upstream code. Four commits were verified through GitHub during this audit; the manifest records them.

```powershell
py -3 scripts/fetch-upstreams.py --root "$env:USERPROFILE/04_Src/deckforge-lab" --only astra presentation-skill impeccable pptkit
```

It creates detached checkouts and writes:

```text
%USERPROFILE%\04_Src\deckforge-lab\upstreams.lock.json
```

The script refuses existing checkout directories rather than resetting local edits. To rerun only unfinished acquisitions, pass only those IDs. A failed fetch may leave a partial directory for inspection; it is not silently deleted.

### 6.2 Add selective experiments — RUN NOW, requires network

```powershell
py -3 scripts/fetch-upstreams.py --root "$env:USERPROFILE/04_Src/deckforge-lab" --only knowledge-cat slides-ai pptkit-presentation presenton pptx-automizer
```

These extra repositories were reviewed as candidates, but their exact commit IDs were not recorded during this audit. The script resolves and locks their fetched HEADs at acquisition. Do not describe those as pre-audited revisions.

PPTAgent is a separate research-only acquisition:

```powershell
py -3 scripts/fetch-upstreams.py --root "$env:USERPROFILE/04_Src/deckforge-lab" --only pptagent
```

Fetching is not a security approval. Before execution, review the selected revision against all applicable advisories and inspect dependencies. The known code-execution advisory identifies a fix commit, so check patch inclusion rather than rejecting the project solely by its name [D11].

### 6.3 Fork only where patches are needed

Initial patch-maintenance priorities:

| Repository | Fork purpose | First proposed change |
|---|---|---|
| `siril9/presentation-skill` | Reusable composition and QA modules | Extract a small stable module boundary and eliminate workspace-specific assumptions |
| `pbakaus/impeccable` | Usually no fork needed | Keep a separate Office adapter; propose generic context improvements upstream |
| `openHacking/pptkit` | Only when an experiment finds a fixable gap | Add a fixture-backed exporter/layout change rather than replace our core model |
| Astra | Visual structures and art direction | Resolve reuse permission, then port selected templates with provenance and native labels |
| Presenton | Only after editor/backend experiment succeeds | Add a documented adapter contract or export fix, not a wholesale UI rewrite |

For example, after reviewing the candidate, create a fork without modifying the pinned reference checkout:

```powershell
gh repo fork siril9/presentation-skill --clone=false
```

A GitHub fork preserves a source relationship. It is not a substitute for a redistribution grant for unlicensed material. This should be a small rights/provenance task, not a reason to postpone the original compiler, brand pack or synthetic structure work.

## 7. Run the most useful upstream checks

These are **optional upstream command probes**, adapted at the shell entrypoint for Windows but not tested here. Upstream npm/Python scripts may still contain python3/Bash/POSIX assumptions; report those before execution, port only reviewed modules, or run an explicitly separate WSL lab. A WSL pass is not native-Windows evidence. Keep each experiment in its own checkout and dependency environment.

### 7.1 presentation-skill — EXPERIMENT

Its audited v0.11.0 package exposes the following scripts [D03]:

```powershell
Set-Location "$env:USERPROFILE/04_Src/deckforge-lab/presentation-skill"
npm.cmd install
npm.cmd run setup:python
npm.cmd run doctor
npm.cmd run check:node
npm.cmd run check:python
npm.cmd run check:role-contracts-v2
npm.cmd run check:visual-receipt
```

`check:python` is largely syntax validation; do not call that full behavioral QA. `setup:python` installs an isolated runtime and needs network. Read its emitted diagnostics before adding other test suites.

Inspect the supported CLI surface rather than assuming the future Deckforge commands exist there:

```powershell
py -3 scripts/present.py --help
```

**Acceptance for reuse:** identify the exact composition/QA modules that work without hidden files, custom runtimes, or absolute paths; run their tests; document interface and license; port one module at a time. Do not copy its entire agent prompt into ours.

### 7.2 Knowledge Cat — EXPERIMENT

Start with the available check runner [D06]:

```powershell
Set-Location "$env:USERPROFILE/04_Src/deckforge-lab/knowledge-cat"
py -3 scripts/run_checks.py
```

Its native lane expects a prepared `@oai/artifact-tool` workspace. Passing planning checks does not establish a portable native renderer. Reuse planning/evidence ideas and dependency-free validators only after inspection, or build a specific adapter for an environment where the dependency is legitimately available.

### 7.3 slides-ai-plugin — EXPERIMENT

Its helper skill documents execution through Bun and can auto-install text/graphics dependencies [D07]. Do not trigger that side effect in the main project. Inspect `skills/pptx-slides/scripts/` and its imports first.

For the core, port only a tested text-measurement or geometry helper, pin its explicit dependencies in our npm lockfile, and remove automatic package installation. Golden fixtures must cover long labels, different weights, CJK, padding, line spacing and missing fonts. A helper's own `autoFontSize()` name is not proof of Office fitting accuracy.

## 8. Beta backend experiments run early

Accept beta software, but require a short experiment report. Every experiment gets the same frozen synthetic deck inputs, declared capability requirements, output hashes, environment manifest, actual PPTX renders, and an explicit list of failures.

### 8.1 PPTKit source experiment — EXPERIMENT

Use its pinned source checkout. Read `package.json` and `pnpm-lock.yaml` before choosing the package-manager version; honor the checkout's own `packageManager` field when supplied. Do not replace it with a guessed global version.

With that pnpm available, its documented developer workflow is [D08]:

```powershell
Set-Location "$env:USERPROFILE/04_Src/deckforge-lab/pptkit"
pnpm install --frozen-lockfile
pnpm build
pnpm typecheck
pnpm lint
pnpm test
pnpm dev
```

If a checkout has no lockfile or the frozen install fails, stop and record the mismatch. Do not silently rewrite it and claim reproduction of the audited state.

Alternatively, test published preview packages in a **separate** npm project:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE/04_Src/deckforge-lab/pptkit-package-probe"
Set-Location "$env:USERPROFILE/04_Src/deckforge-lab/pptkit-package-probe"
npm.cmd init -y
npm.cmd install --save-exact @pptkit/core @pptkit/pptx-exporter @pptkit/svg-renderer
npm.cmd ls --depth=0
```

This resolves whatever published versions are available at execution and saves exact direct versions plus a lockfile. It is a package experiment, **not** proof that the packages equal the audited source commit. Start from the upstream README's `createPresentation` / `writePptx` example, then implement our scene adapter as PR-X1.

Required capability probes: rich text, native charts with editable workbook data, real tables, groups, anchored connectors after manual node movement, notes, theme colors, missing fonts and final-PPTX rendering. Import/roundtrip remains a separate later track; do not promise it from an exporter test.

### 8.2 PPTKit Presentation review experiment — EXPERIMENT

Its audited README specifies Node 20+ and pnpm 10.13.1 and provides this workflow [D09]. Keep it separate from the core checkout's package-manager choice:

```powershell
Set-Location "$env:USERPROFILE/04_Src/deckforge-lab/pptkit-presentation"
npm.cmd exec --yes --package=pnpm@10.13.1 -- pnpm install
npm.cmd exec --yes --package=pnpm@10.13.1 -- pnpm build
npm.cmd exec --yes --package=pnpm@10.13.1 -- pnpm typecheck
npm.cmd exec --yes --package=pnpm@10.13.1 -- pnpm test
npm.cmd exec --yes --package=pnpm@10.13.1 -- pnpm --filter presentation-preview dev
```

Assess session/review UX independently of the underlying exporter. Its browser SVG review is not advertised as pixel-identical PowerPoint. Do not put customer content into an unreviewed input path.

### 8.3 Presenton service experiment — EXPERIMENT

Docker is optional and must already be installed/configured. The included helper is print-only unless `--start` is provided:

```powershell
Set-Location "$env:USERPROFILE/04_Src/deckforge"
py -3 scripts/start-presenton-lab.py
```

To actually pull and start the local experiment:

```powershell
py -3 scripts/start-presenton-lab.py --start
```

The helper uses the documented Presenton image and `/app_data` volume [D10]. It pulls the selected tag, resolves a repository digest, and runs that digest rather than the moving tag. It binds port 5001 to **127.0.0.1 only**, disables the documented memory/image-generation/web-grounding options for the initial text-only experiment, and records the resolved image in `out/lab/presenton-image.json`.

Use Docker Desktop only as a separate experiment; do not expose Office COM or the Windows profile to the container. Open `http://127.0.0.1:5001` locally; finish authentication/provider setup in the UI. No credential or model is preconfigured by this starter. A local service may still send content to an external model provider. Use only synthetic input during this experiment. Pulling/running the image and provider configuration have **not** been executed in the audit environment.

```powershell
docker logs --tail 100 deckforge-presenton-lab
docker stop deckforge-presenton-lab
docker start deckforge-presenton-lab
```

The helper refuses to replace an existing container. A fresh test can use another name and port, leaving the first experiment and volume intact:

```powershell
py -3 scripts/start-presenton-lab.py --start --name deckforge-presenton-lab-2 --port 5002
```

When repeating a specific image, pass the recorded digest through `--image`; keep the private application-data volume out of version control. Tag discovery is a one-time convenience, not the final release pin.

**Integration contract to implement:** authenticate with a Presenton API key, submit frozen content/slide Markdown to the documented `/api/v1/ppt/presentation/generate` endpoint, capture its actual response schema, and reconcile the exported content. Do not invent a REST polling URL or assume a generic `render(DeckSpec)` API. Its UI/MCP/API are application interfaces, not interchangeable with our native writer.

### 8.4 Promotion decision

Choose an engine based on measured results, not stars or beta labels. A candidate can become the default only when it meets all required native/editability gates and improves a meaningful aspect of layout, visual quality, maintenance or authoring. Preserve the previous backend until the same fixtures pass.

Do not auto-select a different export engine for each slide. Composition providers may vary by slide; the final PPTX package writer remains one explicit choice per deck.

## 9. Delivery backlog: vertical slices and dependencies

These are implementation units, not elapsed-time promises. Run X1/X2 in parallel with the core only when there is capacity; they must not block an original native renderer or the first attractive structures.

| PR | Depends on | Concrete deliverable | Acceptance evidence |
|---|---|---|---|
| **PR-00 Baseline** | None | Supplied fixture, local tests, clean online install, committed lockfile | Six native slides; local preview; install log; PowerPoint check recorded separately |
| **PR-01 Contracts/compiler** | PR-00 | Versioned semantic schema, structure registry, measured scene boundary, reference writer | Unknown fields/capabilities rejected; same resolved geometry on repeat runs; no silent flattening |
| **PR-02 Brand/voice** | PR-01 | Private pack loader, token rules, voice pairs, brand approval record | Three company-approved treatments; no invented company defaults; approved vocabulary and co-brand policy |
| **PR-03 Visual pack v1** | PR-01; PR-02 for real branding | First eight attractive structures and a real-content gallery | Minimal/normal/dense/long-label fixtures; native essentials; visual review against agreed references |
| **PR-04 Office/QA gates** | PR-01–03 plus Windows admission/session contracts | Text fit, package inspection, final renders, capability reports and receipts | No unreviewed clipping/repair warnings; chart/table edits; missing-font diagnostic; bounded repair loop |
| **PR-04W Native Office host** | PR-01 and security/admission | DF-20: attended STA worker, native render/inspect/save/edit probes | Exact PowerPoint/Excel/font environment; ownership and timeout fixtures |
| **PR-05 Source intake** | PR-01, PR-04 | Markdown intake, then PPTX content extraction with provenance | Text/data/notes retention tests; unsupported content inventory; hostile-file limits |
| **PR-05W Word/Excel intake** | PR-05 foundations plus DF-20 | DF-21 optional native read-only source extraction | Revisions, typed values, links/privacy and unchanged source hashes |
| **PR-06 Template lane** | PR-02, PR-04, DF-20 | Native `powerpoint-template` adapter for one approved company template; optional automizer comparison | Approved masters/placeholders/theme inheritance; edited chart/notes survive; limits declared |
| **PR-07 Review experience** | PR-03–05 | Story approval, gallery, specific-slide revision, preview/export states | Consultant completes a deck without choosing coordinates or understanding APIs |
| **PR-08 Public beta** | PR-04–07 | Pack distribution, reproducible CI, privacy review, documentation and pilot | Synthetic public fixtures only; brand pack private; three realistic pilot decks meet gates |
| **PR-X1 PPTKit** | PR-01 | Subset scene adapter + comparison report | Final artifact fidelity and native contracts pass on exact pin |
| **PR-X2 Presenton** | PR-00 | Independent generation/editor experiment | Input/output content diff, authenticated loop, editable export, state ownership understood |
| **PR-X3 Research critic** | PR-04 | Optional isolated visual critic/ideator | No code execution from model output; measurable benefit over existing review |

### PR-01 implementation details

Create TypeScript packages for `contracts`, `compiler`, and `render-pptxgenjs`; use npm workspaces only once there are actual package boundaries. Choose one schema validator and commit its exact version/lockfile. Do not create a dozen empty framework packages merely to match an architecture diagram.

Implement in order:

1. `DeckSpec` plus a discriminated structure-content union; stable deck/slide/element IDs; schema migration policy.
2. Evidence and asset registries with allowed paths, sensitivity and output rights.
3. `BrandSpec` resolver with explicit conflict handling; demo brand is a separate pack.
4. `ResolvedScene` in points, with fonts, measured lines, z-order and declared overlap exceptions.
5. `RenderPlan` containing the selected backend and required capabilities.
6. The first compiler for cover, bridge, layers and comparison; an explicit adapter from the smoke input for regression tests.
7. PptxGenJS emission from the scene, not an LLM-generated source file. Add the separate DF-20 Windows worker early after storage/security boundaries; do not embed COM calls in the compiler.

Determinism means the same canonical scene for fixed inputs, fonts and versions. Raw PPTX ZIP bytes may differ due to timestamps or packaging metadata; normalize those before using a binary hash as a regression assertion.

### PR-02 brand capture is a product task

Acquire the corporate master/template, authoritative brand guide, approved logo assets, font licensing/install information, and a small set of genuinely good decks. Add representative writing samples and rejected examples with reasons. Fewer reviewed examples are better than an indiscriminate corpus of old slides.

Create the private workspace without placing actual material in the public project:

```powershell
New-Item -ItemType Directory -Force -Path "$env:LOCALAPPDATA/DeckforgePrivate/brands/ferroque"
New-Item -ItemType Directory -Force -Path "$env:LOCALAPPDATA/DeckforgePrivate/jobs"
```

The capture tool should produce candidate rules with a source and confidence for each inference, then require brand-owner approval. It should distinguish `official`, `observed`, `proposed`, and `deprecated` rather than treating an old deck as authority.

Create three previews from identical actual content: executive editorial, technical/diagram-led and high-impact keynote. Brand review chooses permissible treatments, not just hex colors. Voice review should compare before/after pairs and confirm the rewrite preserved the claim and qualification.

Acceptance includes private-path validation and an export test proving that private source filenames, customer names from unrelated examples, and approval comments do not leak into speaker notes, HTML, logs, screenshots or public fixtures.

### PR-03 is where it becomes attractive

Do not postpone this until after every backend is integrated. Port the *composition* and visual vocabulary that motivated the project.

The first eight structures are bridge, hub/spoke, layers, comparison, roadmap/swimlane, dashboard, funnel, and editorial hero. Give each one at least two purposeful variants, not arbitrary palette swaps. Start with three showcase slides before implementing the whole catalog.

For an Astra-derived candidate, record source file/commit, asset rights, labels/data, effects, external dependencies and static-state behavior. The bridge example includes hidden animation states and very small text [D12]. Replace its embedded sample labels with semantic slots; separate decoration; redesign spacing for readable native PowerPoint text.

Each pack needs `manifest.json`, content schema, compiler, style variants, static-state rules, minimal/normal/dense/long-label fixtures, native capability requirements, provenance and preview fixtures. Do not run copied HTML in a privileged browser; review/freeze dependencies in an isolated experiment first.

**Definition of done:** a company reviewer prefers the approved treatment over the generic baseline, essential text and data are editable, no false data semantics are introduced, and final-PPTX rendering is reviewed. Lint passing is necessary, not sufficient.

### PR-04 QA must separate facts from appearance

Produce a machine-readable result with `PASS`, `FAIL`, `WARN`, or `NOT_RUN` for every check. Never let a missing PowerPoint installation produce a green Office-compatibility result. PowerPoint-native rendering and feature probes are required for the default Windows release; human review remains independent.

Implement a bounded loop: compile/render, inspect all affected slides, apply a single batched repair, rerender and confirm. A remaining failure stops release and lists the affected slide IDs. Do not create an unbounded polish agent.

For text fitting, test measured line metrics against exported renders. For geometry, allow intentional panel/text containment and correct connector/node contact. Fail unintended overlaps, out-of-bounds critical elements and below-policy type sizes. Prefer a new layout or extra slide over shrinking everything.

### PR-05 ingest without claiming round-trip preservation

Markdown is the first intake format. Preserve source spans, explicit slide separators, notes, tables, numbers and quotations. A planner may propose a different narrative; content deletion or claim changes must appear in a reviewable diff.

Then add PPTX **content extraction**, with a capability inventory for charts, tables, notes, images, groups, animations and unsupported objects. Content extraction, visual reconstruction and native-template preservation are three different operations. Return a report instead of promising lossless conversion.

Use bounded ZIP/XML parsing, path checks, entity restrictions, decompression limits, isolated rendering, timeouts and no network by default. Reject macros/executable content for the initial product. The small smoke inspector is not the hardened importer.

### PR-06 corporate template compatibility

Start with one approved template. Identify its layout names, placeholders, masters, theme mapping, font requirements, notes and special objects. Add fixture slides with tables/charts and unusual content, then copy/edit/export through the selected Windows `powerpoint-template` worker backend. Test `pptx-automizer` separately as a portability path. Native layout-based slide creation is documented in W10; preservation still needs empirical evidence.

Test adding a new slide in PowerPoint and applying the intended layout. Test chart data, notes and theme colors after save/reopen. Existing animation/layout limitations must be declared [D13]. A visually similar rebuilt theme must never be described as preservation of the original master.

### PR-07 editing ownership

The canonical source is DeckSpec until a user edits the exported PPTX. Record the export hash; if it changes, do not overwrite that file during regeneration. Offer a new export or an explicit re-import workflow. Arbitrary native Office edits cannot automatically be inferred back into the source.

The first review UI should show the story/outline, structure options with actual content, rendered slide previews, evidence/assumptions, native/degraded capability warnings, and targeted revision controls. Avoid starting with a full drag-and-drop PowerPoint clone.

## 10. Future CLI contract — TO IMPLEMENT

These commands are specifications for future work. They do **not** run in the supplied starter:

```text
deck init --job <private-job-directory>
deck brand capture --inputs <private-reference-directory> --out <private-brand-pack>
deck plan --brief <file> --brand <approved-pack> --out <deck.json>
deck validate <deck.json>
deck gallery --deck <deck.json> --structures bridge,roadmap
deck build <deck.json> --backend pptxgenjs --out <job>/build
deck qa <job>/build --render powerpoint --profile windows-office
deck review <job>
deck export <job> --require-approved
```

Additional planned commands: `deck doctor --profile windows-office`, `deck office probe <build> --checks save-reopen,chart-data,connectors`, and optional `deck ingest <source.docx|source.xlsx> --engine word-desktop|excel-desktop --job <job>` (choose the matching file/engine, not literal pipe syntax).

Expected job files:

```text
brief.json
sources/manifest.json
story.md
deck.json
design-intent.json
render-plan.json
scene.json
build/deck.pptx
build/preview/powerpoint/
qa/content.json
qa/geometry.json
qa/office.json
qa/office-environment.json
qa/visual-review.json
release/manifest.json
```

Proposed exit codes: `0` requested operation succeeded; `2` invalid input/schema; `3` unsupported required capability; `4` failed render/QA; `5` missing approval/dependency. A successful draft build may coexist with `NOT_RUN` Office review, but `export --require-approved` must fail until required gates pass.

Every command should emit enough structured data for another coding agent or UI to call it without scraping conversational text.

## 11. Test matrix and benchmarking

### Acceptance fixtures

| Fixture | Main failure it should expose | Evidence |
|---|---|---|
| F01 native smoke | Flattened slides or absent notes/data | Package counts, XML, render and manual editing |
| F02 long title/labels | Shrink-to-fit and broken line breaks | Measured lines plus actual exported render |
| F03 CJK and mixed weights | Font fallback/metric mismatch | Resolved font manifest and screenshot |
| F04 bridge/dashboard | Attractive source losing clarity in native form | Side-by-side design review and native essentials |
| F05 native chart | Screenshot chart or missing workbook | Dataset equality and PowerPoint Edit Data probe |
| F06 table | Fake cell structure or bad pagination | Cell/merge inspection and manual edit |
| F07 anchored graph | Lines that disconnect on node movement | Move/save/reopen in PowerPoint |
| F08 company master | Theme/layout/placeholder drift | Template fixture and new-slide behavior |
| F09 offline assets | Missing CDN font/art/animation state | Network-denied render and canonical static state |
| F10 evidence | Invented metric or strengthened assertion | Claim diff; supported vs assumption status |
| F11 privacy | Customer/logo/source-path leakage | Publication allowlist and artifact inspection |
| F12 malformed input | ZIP/XML/path traversal/resource abuse | Rejection fixture in isolated parser |
| F13 manual edits | Overwriting a consultant's changes | Hash mismatch preserves original file |
| F14 cross-engine | Similar screenshot with different semantics | Same dataset, label/notes retention and native contract |

### Metrics are targets, not claims

Record supported capability coverage, severe visual failures, factual changes, brand-review preference, manual corrections, generation cost/latency, and Office edit/save success. Do not rank engines solely on speed or an LLM's self-score.

For visual comparison, use frozen content and a fixed brand pack. Randomize candidate order for reviewers; record ties and reasons. Include both executive and technical slides. An engine should not win merely by deleting difficult content or substituting artwork for an editable chart.

CI should run deterministic tests and render goldens in a pinned environment. Keep automated CI credentials and private corpora separate. The initial public CI uses synthetic inputs only. Run public Windows/no-Office CI plus optional Linux portability checks. Run native application acceptance separately on a private attended Windows workstation using approved commits, not a service or untrusted pull request. Import granular application and human receipts; do not advertise unattended Office support.

## 12. First coding-agent assignment

```text
Read AGENTS.md, ARCHITECTURE.md, DEVELOPMENT_PLAN.md and docs/specs/README.md.
Read WINDOWS_SETUP.md and WINDOWS_OFFICE.md under docs/specs.

Implement DF-00 for native Windows first. Preserve the original fixture, add a
portable Python launcher and explicit test paths, record actual tools/fonts/
Office prerequisites, and introduce a separately identified Windows-font fixture.
Do not mark Windows tests as passed from historical Linux evidence.

Then implement DF-01 only in a separate change: strict semantic/scene and Office
request/result contracts without running arbitrary model-generated scripts.

After DF-02 and the DF-17 security/session slice, implement DF-20's attended
read-only PowerPoint render/inspection path in parallel with visual structures.
No SYSTEM/service/container Office automation, Trust Center bypass, blanket
process termination, or overwriting user documents. Add mutation probes later.

Keep one final writer, native essential text/chart/table data and bounded QA.
Deliver changed-file summary, exact tests/results, blockers and the next bounded
spec task. Report unavailable Windows/Office checks as NOT_RUN.
```

Use the [33-spec implementation order](docs/specs/IMPLEMENTATION_ORDER.md) for subsequent work. First design milestone remains bridge + architecture layers + editorial hero, reviewed in actual PowerPoint. Word/Excel intake is an optional DF-21 extension, not a prerequisite for that milestone.

## 13. What is verified in this delivery

This Windows revision updates the architecture, development plan, every original component spec and shared index/contracts/agent workflow, and adds DF-20/DF-21. The existing starter application code and dependencies remain unchanged. The documentation validator checks IDs, dependency graph, links, source snapshots and platform coverage; its current result is in [VALIDATION_REPORT.md](docs/specs/VALIDATION_REPORT.md).

The earlier thirteen-test/six-slide/LibreOffice record is retained as a historical non-Windows result in [LOCAL_TEST_REPORT.md](docs/LOCAL_TEST_REPORT.md). It does not establish Windows install success or native Office behavior. No Office worker, native template adapter, Word/Excel importer, PowerShell script execution or Windows/PowerPoint/Excel/Word acceptance has been performed for this documentation revision.

Immediate sequence: follow guarded Windows setup, reproduce the original fixture, record native manual observations, implement DF-00/01/02 and the security/Office host slice, then deliver the three showcase compositions. Use new exports and immutable probe copies; never overwrite a consultant's edited file.

## 14. Primary sources

Prior donor-source audit entries below are retained from 2026-09-15 and not re-certified by the Windows revision. New native Windows/Office API facts are verified in [WINDOWS_SOURCES.md](docs/specs/WINDOWS_SOURCES.md). Upstream commands may evolve; use the recorded checkout or re-audit a deliberate update. The architecture document contains the detailed source/commit register.

- **D01:** [Impeccable installation](https://github.com/pbakaus/impeccable), [audited package manifest](https://github.com/pbakaus/impeccable/blob/0a4e72a254f3b175c95b36b82e5f2e60fa63f116/package.json).
- **D02:** [Arch Node 24 LTS package](https://archlinux.org/packages/extra/x86_64/nodejs-lts-krypton/).
- **D03:** [presentation-skill scripts](https://github.com/siril9/presentation-skill/blob/311e29920c7c7ab37a93c12676bab7baecc0f4a6/package.json), [README](https://github.com/siril9/presentation-skill/blob/311e29920c7c7ab37a93c12676bab7baecc0f4a6/README.md).
- **D04:** [Claude Code skills](https://code.claude.com/docs/en/skills).
- **D05:** [Official Codex skill discovery](https://developers.openai.com/codex/skills).
- **D06:** [Knowledge Cat runtime and checks](https://github.com/gnipbao/knowledge-cat-ppt-skill).
- **D07:** [slides-ai-plugin helper runtime](https://github.com/proyecto26/slides-ai-plugin/blob/main/skills/pptx-slides/SKILL.md).
- **D08:** [PPTKit quickstart/development](https://github.com/openHacking/pptkit/blob/72715ca460ce649f553848393de922c52f19cd34/README.md), [roadmap](https://github.com/openHacking/pptkit/blob/72715ca460ce649f553848393de922c52f19cd34/ROADMAP.md).
- **D09:** [PPTKit Presentation workflow](https://github.com/openHacking/pptkit-presentation/blob/main/README.md).
- **D10:** [Presenton Docker/API/authentication](https://github.com/presenton/presenton/blob/main/README.md).
- **D11:** [PPTAgent advisory and patch](https://github.com/icip-cas/PPTAgent/security/advisories/GHSA-89g2-xw5c-v95p).
- **D12:** [Astra bridge source](https://github.com/Astralune-ai/Astra-slide-impeccable/blob/7425bb043d59bde2e84cf6d7d7685e451d31f3ac/structures/04-bridge.html).
- **D13:** [pptx-automizer limitations](https://singerla.github.io/pptx-automizer/limitations).
