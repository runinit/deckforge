# Command availability and implementation ownership

This is the authoritative distinction between **existing starter commands**, **documentation-pack commands**, **optional experiments**, and **future product commands**. It does not add commands to `package.json` or install an executable.

## 1. Existing starter commands — RUN NOW

Run from the original `deckforge/` repository after installing its documented dependencies. Their presence was verified in the supplied archive; they have not been rerun as part of this documentation-only delivery.

| Command | Existing purpose | Limitation |
|---|---|---|
| `python3 scripts/doctor.py` | Report local tooling | Inventory, not installation or certification |
| `npm install` | Install starter dependency and create a real lockfile | Needs registry/network access unless already available |
| `npm test` | Run the existing smoke-schema tests | Does not test proposed production specs |
| `npm run smoke` | Generate the six-slide fixture | Synthetic original composition, not company branding |
| `npm run inspect` | Inspect fixture package/native objects | Fixed fixture contract, not general PPTX validation |
| `npm run check` | Tests + generation + fixture inspection | No automatic application/visual approval |
| `npm run preview` | Render actual fixture PPTX through local tools | Needs LibreOffice/Poppler; trusted fixture only |
| `node scripts/build-smoke.mjs examples/smoke-deck.json out/second-smoke` | Build the same fixture with explicit paths | Still the smoke schema |
| `python3 scripts/inspect-pptx.py out/second-smoke/deck.pptx` | Inspect that fixture | Still fixture-specific |
| `python3 scripts/render-local.py out/second-smoke/deck.pptx` | Render that fixture | Not a hardened importer/sandbox |

Prefer the real committed lockfile and `npm ci` after the first successful reviewed install. Keep upstream version changes separate from this spec decomposition. Existing platform installation instructions are preserved in the [baseline development plan](references/DEVELOPMENT_PLAN.md); this pack does not make new “latest version” claims.

## 2. Documentation-pack command — IMPLEMENTED IN THIS DELIVERY

After extracting the spec ZIP into the repository root:

```sh
python3 docs/specs/tools/validate_specs.py
```

For a machine-readable report:

```sh
python3 docs/specs/tools/validate_specs.py --json
```

This checks spec IDs, dependency existence/cycles, required sections, requirement/task/test IDs, local file links, code-fence balance and source snapshot hashes. It does **not** validate TypeScript, run product tests, install upstreams or open PowerPoint.

## 3. Shared development test command — TO IMPLEMENT

Owner: [DF-00](core/00-baseline-and-workspace.md).

```sh
npm run test:spec -- DF-01
```

Contract:

1. Look up the exact spec ID in the implemented application test mapping (`config/spec-tests.json`), not the documentation metadata.
2. Resolve explicit owned test paths safely; reject missing/empty/unknown selections.
3. Build required TypeScript packages using the project’s chosen locked toolchain when needed, then run the registered test files.
4. Report completed checks and unavailable application checks separately.
5. Exit nonzero for missing suites, failed prerequisites or failing required automated tests. Never return success because zero tests were selected.

Each implementation adds its own suite and mapping. Until both dispatcher and suite exist, the command is a future interface. Do not create 31 empty passing test scripts to satisfy the documentation.

Proposed supporting commands such as `npm run build` and `npm run typecheck` must be added and documented by DF-01 when the actual TypeScript packages are introduced. They are not in the original starter manifest.

## 4. Future product CLI — ALL TO IMPLEMENT

Owner of command routing: [DF-14](core/14-director-cli-and-agent-skill.md). The feature owner supplies the operation; DF-14 exposes it without duplicating behavior.

| Future command | Feature owner | Expected output / prerequisite |
|---|---|---|
| `deck init --job <private-job-directory>` | DF-02 | New private job manifest; refuses unsafe/conflicting root |
| `deck brand capture --inputs <private-reference-directory> --out <private-brand-pack>` | DF-03 | Candidate brand pack and source/authority report; not auto-approved |
| `deck plan --brief <file> --brand <approved-pack> --out <deck.json>` | DF-14 with DF-04/05/12 | Story/DeckSpec proposal, evidence/retention diff |
| `deck validate <deck.json>` | DF-01 | Structured validation result; exact pack schemas required |
| `deck gallery --deck <deck.json> --structures bridge,roadmap` | DF-06/10 | Real-content candidate previews; aliases resolve to exact registered IDs |
| `deck build <deck.json> --backend pptxgenjs --out <job>/build` | DF-07/08 | Immutable scene/render-plan/artifact bundle; no silent downgrade |
| `deck qa <job>/build --render libreoffice` | DF-11/17 | Gate report and final-PPTX render; explicit unavailable checks |
| `deck review <job>` | DF-16 | Local review session over canonical job state |
| `deck export <job> --require-approved` | DF-11/14 | Release artifact/manifest only when valid required receipts pass |

The friendly baseline `<job>/build` path is an operation target. The implementation resolves it to the immutable build storage described in [CONTRACTS.md](CONTRACTS.md), rather than overwriting a previously edited file.

Missing commands are not solved by copying slash-command syntax from another skill. The eventual `/deck` entrypoint is a host-specific skill wrapper around these operations, not an assumed installed binary.

## 5. Optional upstream experiments — EXISTING HELPERS, EXTERNAL EXECUTION

The supplied starter already includes these acquisition/print helpers. Their existence does not mean upstreams are installed or their tests have passed.

```sh
python3 scripts/fetch-upstreams.py --root "$HOME/04_Src/deckforge-lab" --only astra presentation-skill impeccable pptkit
python3 scripts/start-presenton-lab.py
```

The first command requires network access and creates source checkouts; it does not install or execute upstream code. The second is print-only without `--start`.

Actual engine/service experiments are governed by [DF-X1](experiments/01-pptkit-backend.md), [DF-X2](experiments/02-presenton-service-and-editor.md) and [DF-X3](experiments/03-isolated-research-critic.md). Use the [original setup commands](references/DEVELOPMENT_PLAN.md), selected pins and actual checkout manifests. Do not infer package versions or API schemas from this doc’s proposed adapter signatures.

## 6. Shell and path policy

Displayed shell commands use quoted paths and no Bash-specific heredocs, activation scripts, process substitution or `export NAME=value`. They can be entered in fish using the same arguments. API examples and pseudo-CLI contracts are marked proposed; they are not shell scripts.

Never run extraction over an existing `docs/specs` directory without reviewing conflicts. Do not reset a lab checkout, replace an existing container, overwrite a user-edited PPTX or publish a repository as an implicit setup step.
