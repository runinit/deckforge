# Deckforge: development plan and project bootstrap

**Audit date:** 2026-09-15.  
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

The first milestone is **a branded, visually distinctive, editable deck**, not a plugin installer that launches eight unrelated agents.

The supplied repository is a runnable **acceptance-fixture starter**, not the finished hybrid system. It establishes native text/shapes/charts/tables/notes, a small input validator, structural inspection, and local preview. Its six designs are original smoke fixtures, not Astra ports or a validated Ferroque template.

Every command below has one of three statuses:

| Status | Meaning |
|---|---|
| **RUN NOW** | Implemented in the supplied starter, or a documented upstream command clearly identified as such |
| **EXPERIMENT** | Optional upstream installation/execution; may need network, Docker, a model provider, or additional dependencies |
| **TO IMPLEMENT** | Proposed future interface or task; not a command that exists in this starter |

Do not call planned `/deck` commands and assume the product has been implemented. The initial skill tells a coding agent how to work on this repository; it does not yet accept arbitrary client material and generate a finished corporate deck.

## 2. Toolchain and workspace

### Core tooling

Use Node.js and npm for the starter. Use Python for local inspection and optional previews. The production packages should migrate to TypeScript in PR-01, without requiring a monorepo task orchestrator on day one.

| Tool | Starter | Later use |
|---|---|---|
| Node.js | 22+; locally tested on 22.16.0 | Prefer a current Node 24 environment for experiments; the audited Impeccable installer requires at least 22.18.0 [D01] |
| npm | Dependency installation and scripts | Commit a lockfile after the first successful online installation |
| Python | Standard library only for supplied scripts | Isolated ingestion/QA dependencies when introduced |
| LibreOffice + Poppler | Optional actual-PPTX render to PDF/PNG | Reference rendering, not Microsoft PowerPoint certification |
| Git | Source and revision tracking | Pin upstream source checkouts |
| Docker | Not required | Presenton and isolated conversion experiments |
| pnpm | Not required | PPTKit/PPTKit Presentation experiments only |
| Bun | Not required | Optional `slides-ai-plugin` source experiments; not the proposed core runtime |

### Commands work without Bash-only syntax

The main commands use normal arguments and quoted `$HOME` paths and can be entered in fish, zsh or bash. No heredocs, shell activation scripts, or `export NAME=value` are required. The example workspace is `$HOME/04_Src`; change that path consistently to suit your machine.

**RUN NOW — inventory an existing installation:**

```sh
node --version
npm --version
python3 --version
git --version
```

For an **Arch/CachyOS machine only**, the following packages provide a suitable Linux starting point. Review the transaction; do not replace an existing Node version-manager installation blindly. The Node 24 LTS package is `nodejs-lts-krypton` in Arch's repository [D02].

```sh
sudo pacman -Syu --needed git python unzip nodejs-lts-krypton npm libreoffice-fresh poppler ttf-liberation
```

On another OS, install equivalent tools through its normal package manager. The code does not require Arch. PowerPoint desktop validation may take place on a separate Windows or macOS workstation.

### Keep four locations separate

```text
~/04_Src/deckforge/              public source + synthetic fixtures
~/04_Src/deckforge-lab/          external pinned upstream checkouts
~/02_Areas/DeckforgePrivate/    private brand packs and client inputs
~/04_Src/deckforge/out/          ignored local generated artifacts
```

The last location is acceptable for the synthetic starter. Real client jobs should also use a private external job root, not merely rely on `.gitignore`.

## 3. Run the supplied starter

### 3.1 Extract and install — RUN NOW

The archive contains a top-level `deckforge/` directory. There is no public Deckforge Git remote to clone yet; this is a working name, not an established repository.

Assuming the downloaded archive is in Downloads:

```sh
mkdir -p "$HOME/04_Src"
python3 -m zipfile -e "$HOME/Downloads/deckforge-audited-starter.zip" "$HOME/04_Src"
cd "$HOME/04_Src/deckforge"
python3 scripts/doctor.py
npm install
npm test
npm run smoke
npm run inspect
```

Extract into a new destination if `deckforge/` already contains your work. Do not overwrite an unrelated project.

The starter pins `pptxgenjs` to **4.0.0**, the version used for the local execution evidence. It does **not** claim this is the newest release. The audited `presentation-skill` manifest uses 4.0.1 [D03]; test an upgrade separately rather than changing the baseline without a comparison.

A lockfile is deliberately not fabricated: the artifact-building environment had no working registry/network access. Your first successful `npm install` creates `package-lock.json`; inspect and commit it. Subsequently use `npm ci` for reproducible installs. Record Node, npm and platform versions as well as the lockfile.

### 3.2 Expected outputs — RUN NOW

```text
out/smoke/deck.pptx
out/smoke/geometry.json
out/smoke/build.json
```

`npm run inspect` prints a structural report. On the supplied fixture, expect six slides, one native chart, one native table, one embedded workbook, six notes parts and zero picture objects. These counts are a test of the fixture, not a universal quality standard for future decks.

The inspector should reject a missing chart/workbook or broken internal relationship. It does not prove text fits, connectors are anchored, or PowerPoint can edit and save the file correctly.

### 3.3 Render the actual PPTX — RUN NOW

```sh
npm run preview
```

This requires `soffice` and `pdftoppm` on PATH. It creates:

```text
out/smoke/preview/deck.pdf
out/smoke/preview/slide-1.png ... slide-6.png
```

The helper uses a temporary LibreOffice profile to avoid sharing state with a desktop instance. Use it only on trusted generated fixtures; it is not an untrusted-document sandbox.

On a Linux desktop:

```sh
xdg-open out/smoke/preview/deck.pdf
```

Open the PPTX in Microsoft PowerPoint separately. Edit a heading, a table cell and chart data; save and reopen it; check for repair warnings. Record that check as `NOT_RUN` until it actually happens. LibreOffice success cannot substitute for this gate.

### 3.4 Modify the fixture — RUN NOW

Change the bounded text and synthetic values in `examples/smoke-deck.json`, then run:

```sh
npm run check
npm run preview
```

The builder also accepts explicit paths:

```sh
node scripts/build-smoke.mjs examples/smoke-deck.json out/second-smoke
python3 scripts/inspect-pptx.py out/second-smoke/deck.pptx
python3 scripts/render-local.py out/second-smoke/deck.pptx
```

The fixture inspector intentionally expects this six-slide contract. Do not mistake it for a general DeckSpec validator.

## 4. Put the project under version control

**RUN NOW — review the included MIT license for original starter code and initialize locally:**

```sh
cd "$HOME/04_Src/deckforge"
git init -b main
git add README.md ARCHITECTURE.md DEVELOPMENT_PLAN.md AGENTS.md LICENSE THIRD_PARTY_NOTICES.md
git add package.json package-lock.json .gitignore .env.example src scripts tests skills config examples docs
git diff --cached --stat
git diff --cached --name-only
git status --short
```

Inspect the staged files before committing. No fonts, customer inputs, company template, generated deck, credentials, source checkout, or proprietary brand pack should be staged.

```sh
git commit -m "Bootstrap audited native-PPTX fixture and hybrid architecture"
git switch -c feat/contracts-and-scene
```

A network remote is optional. After installing/authenticating GitHub CLI and reviewing the staged/public content, an explicit publication command is:

```sh
gh repo create deckforge --public --source . --remote origin --push
```

That command creates a public repository under the account selected by `gh`; it may fail if the name is taken. Change the name deliberately rather than overwriting another remote. No repository has been created on your behalf by this delivery.

Use the included MIT license for original code if that matches the project's choice. Adapted upstream files retain their own licenses and notices. A license on this project does not cover an upstream file or asset with unresolved permission.

## 5. Make the repository usable by a coding agent

### 5.1 Install only our thin development skill — RUN NOW

From the project root, choose the host you use. These links are project-scoped and fail rather than overwrite an existing destination.

For Claude Code, whose documented project skill location is `.claude/skills/` [D04]:

```sh
mkdir -p .claude/skills
ln -s ../../skills/deckforge .claude/skills/deckforge
```

For Codex, whose documented repository skill directory is `.agents/skills/` and which supports symlinks [D05]:

```sh
mkdir -p .agents/skills
ln -s ../../skills/deckforge .agents/skills/deckforge
```

The bundled skill reads `AGENTS.md` and both plans and directs implementation/testing. Do not install every presentation skill globally under competing auto-trigger descriptions. Reusable references should be loaded selectively by the eventual director.

### 5.2 Add Impeccable — EXPERIMENT

Use a Node version satisfying its audited installer manifest. The following pins the npm launcher; it does not magically pin every separately fetched engine or generated provider file [D01].

```sh
npm exec --yes --package=impeccable@4.1.0 -- impeccable install --providers=claude,codex --scope=project
```

Inspect its generated files and record the installed engine version/hash. Use it initially for design-context capture and review of the gallery/preview UI. The Office-specific adapter still needs implementation. Do not tell it that the smoke palette is Ferroque's identity.

The future adapter should read approved `PRODUCT.md`/`DESIGN.md`, translate permitted design intent into our brand/structure contracts, and emit proposed changes. It must not invoke frontend-only checks as if they were PowerPoint validators.

## 6. Acquire upstream source without entangling runtimes

### 6.1 Fetch the first four checkouts — RUN NOW, requires network

The supplied script clones source only. It does not install packages, load skills, or run upstream code. Four commits were verified through GitHub during this audit; the manifest records them.

```sh
python3 scripts/fetch-upstreams.py --root "$HOME/04_Src/deckforge-lab" --only astra presentation-skill impeccable pptkit
```

It creates detached checkouts and writes:

```text
~/04_Src/deckforge-lab/upstreams.lock.json
```

The script refuses existing checkout directories rather than resetting local edits. To rerun only unfinished acquisitions, pass only those IDs. A failed fetch may leave a partial directory for inspection; it is not silently deleted.

### 6.2 Add selective experiments — RUN NOW, requires network

```sh
python3 scripts/fetch-upstreams.py --root "$HOME/04_Src/deckforge-lab" --only knowledge-cat slides-ai pptkit-presentation presenton pptx-automizer
```

These extra repositories were reviewed as candidates, but their exact commit IDs were not recorded during this audit. The script resolves and locks their fetched HEADs at acquisition. Do not describe those as pre-audited revisions.

PPTAgent is a separate research-only acquisition:

```sh
python3 scripts/fetch-upstreams.py --root "$HOME/04_Src/deckforge-lab" --only pptagent
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

```sh
gh repo fork siril9/presentation-skill --clone=false
```

A GitHub fork preserves a source relationship. It is not a substitute for a redistribution grant for unlicensed material. This should be a small rights/provenance task, not a reason to postpone the original compiler, brand pack or synthetic structure work.

## 7. Run the most useful upstream checks

These are **documented upstream commands to run locally**, not test results from this audit. Keep each experiment in its own checkout and dependency environment.

### 7.1 presentation-skill — EXPERIMENT

Its audited v0.11.0 package exposes the following scripts [D03]:

```sh
cd "$HOME/04_Src/deckforge-lab/presentation-skill"
npm install
npm run setup:python
npm run doctor
npm run check:node
npm run check:python
npm run check:role-contracts-v2
npm run check:visual-receipt
```

`check:python` is largely syntax validation; do not call that full behavioral QA. `setup:python` installs an isolated runtime and needs network. Read its emitted diagnostics before adding other test suites.

Inspect the supported CLI surface rather than assuming the future Deckforge commands exist there:

```sh
python3 scripts/present.py --help
```

**Acceptance for reuse:** identify the exact composition/QA modules that work without hidden files, custom runtimes, or absolute paths; run their tests; document interface and license; port one module at a time. Do not copy its entire agent prompt into ours.

### 7.2 Knowledge Cat — EXPERIMENT

Start with the available check runner [D06]:

```sh
cd "$HOME/04_Src/deckforge-lab/knowledge-cat"
python3 scripts/run_checks.py
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

```sh
cd "$HOME/04_Src/deckforge-lab/pptkit"
pnpm install --frozen-lockfile
pnpm build
pnpm typecheck
pnpm lint
pnpm test
pnpm dev
```

If a checkout has no lockfile or the frozen install fails, stop and record the mismatch. Do not silently rewrite it and claim reproduction of the audited state.

Alternatively, test published preview packages in a **separate** npm project:

```sh
mkdir -p "$HOME/04_Src/deckforge-lab/pptkit-package-probe"
cd "$HOME/04_Src/deckforge-lab/pptkit-package-probe"
npm init -y
npm install --save-exact @pptkit/core @pptkit/pptx-exporter @pptkit/svg-renderer
npm ls --depth=0
```

This resolves whatever published versions are available at execution and saves exact direct versions plus a lockfile. It is a package experiment, **not** proof that the packages equal the audited source commit. Start from the upstream README's `createPresentation` / `writePptx` example, then implement our scene adapter as PR-X1.

Required capability probes: rich text, native charts with editable workbook data, real tables, groups, anchored connectors after manual node movement, notes, theme colors, missing fonts and final-PPTX rendering. Import/roundtrip remains a separate later track; do not promise it from an exporter test.

### 8.2 PPTKit Presentation review experiment — EXPERIMENT

Its audited README specifies Node 20+ and pnpm 10.13.1 and provides this workflow [D09]. Keep it separate from the core checkout's package-manager choice:

```sh
cd "$HOME/04_Src/deckforge-lab/pptkit-presentation"
npm exec --yes --package=pnpm@10.13.1 -- pnpm install
npm exec --yes --package=pnpm@10.13.1 -- pnpm build
npm exec --yes --package=pnpm@10.13.1 -- pnpm typecheck
npm exec --yes --package=pnpm@10.13.1 -- pnpm test
npm exec --yes --package=pnpm@10.13.1 -- pnpm --filter presentation-preview dev
```

Assess session/review UX independently of the underlying exporter. Its browser SVG review is not advertised as pixel-identical PowerPoint. Do not put customer content into an unreviewed input path.

### 8.3 Presenton service experiment — EXPERIMENT

Docker is optional and must already be installed/configured. The included helper is print-only unless `--start` is provided:

```sh
cd "$HOME/04_Src/deckforge"
python3 scripts/start-presenton-lab.py
```

To actually pull and start the local experiment:

```sh
python3 scripts/start-presenton-lab.py --start
```

The helper uses the documented Presenton image and `/app_data` volume [D10]. It pulls the selected tag, resolves a repository digest, and runs that digest rather than the moving tag. It binds port 5001 to **127.0.0.1 only**, disables the documented memory/image-generation/web-grounding options for the initial text-only experiment, and records the resolved image in `out/lab/presenton-image.json`.

Open `http://127.0.0.1:5001` locally; finish authentication/provider setup in the UI. No credential or model is preconfigured by this starter. A local service may still send content to an external model provider. Use only synthetic input during this experiment. Pulling/running the image and provider configuration have **not** been executed in the audit environment.

```sh
docker logs --tail 100 deckforge-presenton-lab
docker stop deckforge-presenton-lab
docker start deckforge-presenton-lab
```

The helper refuses to replace an existing container. A fresh test can use another name and port, leaving the first experiment and volume intact:

```sh
python3 scripts/start-presenton-lab.py --start --name deckforge-presenton-lab-2 --port 5002
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
| **PR-04 Office/QA gates** | PR-01–03 | Text fit, package inspection, final renders, capability reports and receipts | No unreviewed clipping/repair warnings; chart/table edits; missing-font diagnostic; bounded repair loop |
| **PR-05 Source intake** | PR-01, PR-04 | Markdown intake, then PPTX content extraction with provenance | Text/data/notes retention tests; unsupported content inventory; hostile-file limits |
| **PR-06 Template lane** | PR-02, PR-04 | `pptx-automizer` adapter for one approved company template | Approved masters/placeholders/theme inheritance; edited chart/notes survive; limits declared |
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
7. PptxGenJS emission from the scene, not an LLM-generated source file.

Determinism means the same canonical scene for fixed inputs, fonts and versions. Raw PPTX ZIP bytes may differ due to timestamps or packaging metadata; normalize those before using a binary hash as a regression assertion.

### PR-02 brand capture is a product task

Acquire the corporate master/template, authoritative brand guide, approved logo assets, font licensing/install information, and a small set of genuinely good decks. Add representative writing samples and rejected examples with reasons. Fewer reviewed examples are better than an indiscriminate corpus of old slides.

Create the private workspace without placing actual material in the public project:

```sh
mkdir -p "$HOME/02_Areas/DeckforgePrivate/ferroque-brand"
mkdir -p "$HOME/02_Areas/DeckforgePrivate/jobs"
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

Produce a machine-readable result with `PASS`, `FAIL`, `WARN`, or `NOT_RUN` for every check. Never let a missing PowerPoint installation produce a green Office-compatibility result.

Implement a bounded loop: compile/render, inspect all affected slides, apply a single batched repair, rerender and confirm. A remaining failure stops release and lists the affected slide IDs. Do not create an unbounded polish agent.

For text fitting, test measured line metrics against exported renders. For geometry, allow intentional panel/text containment and correct connector/node contact. Fail unintended overlaps, out-of-bounds critical elements and below-policy type sizes. Prefer a new layout or extra slide over shrinking everything.

### PR-05 ingest without claiming round-trip preservation

Markdown is the first intake format. Preserve source spans, explicit slide separators, notes, tables, numbers and quotations. A planner may propose a different narrative; content deletion or claim changes must appear in a reviewable diff.

Then add PPTX **content extraction**, with a capability inventory for charts, tables, notes, images, groups, animations and unsupported objects. Content extraction, visual reconstruction and native-template preservation are three different operations. Return a report instead of promising lossless conversion.

Use bounded ZIP/XML parsing, path checks, entity restrictions, decompression limits, isolated rendering, timeouts and no network by default. Reject macros/executable content for the initial product. The small smoke inspector is not the hardened importer.

### PR-06 corporate template compatibility

Start with one approved template. Identify its layout names, placeholders, masters, theme mapping, font requirements, notes and special objects. Add fixture slides with tables/charts and unusual content, then copy/edit/export through `pptx-automizer`.

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
deck qa <job>/build --render libreoffice
deck review <job>
deck export <job> --require-approved
```

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
build/preview/
qa/content.json
qa/geometry.json
qa/office.json
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

CI should run deterministic tests and render goldens in a pinned environment. Keep automated CI credentials and private corpora separate. The initial public CI uses synthetic inputs only. Add actual PowerPoint application verification as a separately recorded human/approved-workstation gate, not an untested server-automation promise.

## 12. First coding-agent assignment

Paste this into the coding agent from the repository root:

```text
Read AGENTS.md, ARCHITECTURE.md and DEVELOPMENT_PLAN.md.

Implement PR-01 only: a minimal TypeScript semantic contract, structure registry,
resolved-scene model and PptxGenJS adapter. Preserve the supplied smoke harness
as a regression baseline, and explicitly migrate its synthetic input rather
than pretending its schema is production DeckSpec.

Keep native text, table cells, chart data and notes. Distinguish line primitives
from anchored connectors. Reject unsupported capabilities rather than silently
rasterizing. Use one final PPTX package writer. Do not add a web UI, Presenton,
PPTKit, an LLM SDK, a vector database or real company assets in this change.

Run the baseline tests first. Install/lock dependencies only where network access
is available. Add tests for schema rejection, evidence state, point-to-inch
conversion, stable IDs and capability failures. Render the final PPTX if tools
are available. Report unexecuted checks as NOT_RUN.

Deliver the implementation, test log, changed-file summary and the next bounded
PR task. Do not fabricate a brand guide, technical claims, permissions, a clean
install result or Microsoft PowerPoint verification.
```

After this PR, start PR-02 with real brand inputs and PR-03 with the three showcase structures. Run X1/X2 as experiments rather than delaying the first branded deck.

## 13. What is verified in this delivery

The starter's thirteen tests passed locally. It generated a six-slide PPTX with native text, shapes, one table, one chart, an embedded workbook and six notes parts. The actual PPTX rendered to six LibreOffice pages, and a contact sheet was inspected for obvious layout failures. See [docs/LOCAL_TEST_REPORT.md](docs/LOCAL_TEST_REPORT.md).

The environment's preinstalled PptxGenJS 4.0.0 was used through a local module link, excluded from the distribution. A clean registry installation, the external clone commands, upstream suites, Docker/Presenton, PPTKit and Microsoft PowerPoint were not executed. The helper scripts for upstream fetching and Presenton setup are provided for execution on your machine; neither is represented as an already-running integration.

**Immediate sequence:** run the baseline, commit the real dependency lock, open/edit/save the fixture in PowerPoint, implement PR-01, and build the first three brand-approved showcase slides. That establishes both Office usability and the visual quality the project is meant to deliver.

## 14. Primary sources

Sources were inspected on 2026-09-15. Upstream commands may evolve; use the recorded checkout or re-audit a deliberate update. The architecture document contains the detailed source/commit register.

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
