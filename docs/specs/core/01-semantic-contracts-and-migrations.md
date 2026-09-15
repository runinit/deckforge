---
spec_id: DF-01
status: proposed
platform_revision: windows-office-1
primary_platform: windows-native-office
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-01"]
depends_on: ["DF-00"]
---

# DF-01 — Semantic contracts, identity and schema migration

**Goal:** Create the versioned, engine-independent document contract that every planner, pack and backend must consume.

**Baseline mapping:** PR-01. **Dependencies:** [DF-00](00-baseline-and-workspace.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.


**Windows/Office revision:** [execution contract](../WINDOWS_OFFICE.md) and [PowerShell setup](../WINDOWS_SETUP.md) apply to this component. PowerPoint is the primary application-validation path; new worker features remain planned.

## 1. Scope and non-goals

Own JSON schemas, exported TypeScript types, validation, canonicalization and explicit migration. Do not choose layouts, invoke a model, render a deck or treat upstream IR as our public file format.

## 2. File ownership and integration boundary

- `packages/contracts/src/`
- `packages/contracts/schemas/`
- `packages/contracts/package.json`
- `packages/contracts/tests/`
- `scripts/migrate-smoke.mjs (new)`
- `examples/contracts/ (new)`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API, not implemented by this specification:
```ts
validateDeck(input: unknown, registry: StructureSchemaRegistry): ValidationResult<DeckSpec>;
validateScene(input: unknown): ValidationResult<ResolvedScene>;
canonicalizeDeck(deck: DeckSpec): Uint8Array;
migrateSmoke(input: unknown): MigrationResult<DeckSpec>;
```
Use the exact envelope and shared names in [CONTRACTS.md](../CONTRACTS.md). `SlideSpec.content` is validated by the selected exact structure version, not passed through as unchecked JSON. Schema source is authoritative; generated types must not drift from it.

## 4. Requirements


### DF-01.R01 — Strict validation

Require schemaVersion, stable IDs, exact pack/brand references and canvas units. Reject unknown envelope fields, missing discriminators, non-finite values, duplicate IDs and broken cross-references.


### DF-01.R02 — Meaning before geometry

DeckSpec contains semantic content, claims, datasets and selected structures. Absolute coordinates, engine-specific options, executable source and scripts are forbidden in semantic content.


### DF-01.R03 — Stable identity

Preserve slide/content/node IDs through reorder and re-layout. User-visible labels and array positions must not be the only identity. Structural splits retain an explicit derived-from mapping.


### DF-01.R04 — Canonicalization

Sort object keys, preserve meaningful array order, encode deterministically and hash with SHA-256. Do not equate raw PPTX ZIP byte equality with scene equality.


### DF-01.R05 — Version transitions

An incompatible schemaVersion fails with a migration suggestion. Migration produces a new file and report; it never overwrites source input or fabricates approved evidence/brand decisions.


### DF-01.R06 — Platform-neutral semantics

Keep Windows paths, COM dispatch objects and Office numeric enums out of DeckSpec. Add closed OfficeRequest/OfficeResult, environment/profile and application-receipt schemas owned by the shared contract; use logical artifact IDs and relative locations.

### DF-01.R07 — Office operation validation

Reject arbitrary script text/member names and unsupported worker operations. Canonical hashing ignores transport encoding differences only through a versioned rule; raw input hashes remain separate.

## 5. Implementation tasks

- [ ] **DF-01.T01 — Freeze public envelopes.** Implement DeckSpec, SourceManifest, EvidenceRecord, AssetRecord, BrandReference, DesignIntent, ResolvedScene, RenderPlan and diagnostics from the shared contract.
- [ ] **DF-01.T02 — Add validator coverage.** Select and lock one schema implementation; generate or verify TypeScript types in CI. Validate each discriminated element and cross-reference after schema shape validation.
- [ ] **DF-01.T03 — Migrate the synthetic input.** Write an explicit adapter from all six smoke slide types. Give demo facts synthetic status and a demo brand identity; unsupported fields appear in the migration report.
- [ ] **DF-01.T04 — Add roundtrip and identity fixtures.** Serialize/parse DeckSpec, reorder slides, change a label and split a slide. Verify IDs and evidence lineage remain correct.

- [ ] **DF-01.T05 — Define Office boundary schemas.** Coordinate DF-20 envelope/result and application-evidence fields in CONTRACTS/WINDOWS_OFFICE. Add safe filename mappings for semantic IDs containing colons without restricting otherwise valid logical IDs.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `SCHEMA_INVALID` | Return JSON-pointer diagnostics without partial rendering. |
| `SCHEMA_VERSION_UNSUPPORTED` | List the explicit available migration, or fail. |
| `REFERENCE_MISSING` | Identify owner ID and missing target. |
| `MIGRATION_LOSS` | Require review of a loss report before promotion. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-01.AC01 | Unknown fields | Submit `{backendOptions: {script: "..."}}` in a semantic slide. | Validation rejects it at a precise JSON pointer; nothing is executed. |
| DF-01.AC02 | Structure discriminator | Declare bridge with dashboard-shaped content. | Validation fails against bridge content schema. |
| DF-01.AC03 | Reference integrity | Reference an absent source, asset, evidence record or dataset. | Validation returns all relevant broken references in one result. |
| DF-01.AC04 | Identity preservation | Reorder two slides and rewrite a title without changing its meaning. | Existing semantic IDs remain stable. |
| DF-01.AC05 | Smoke migration | Migrate original input to a new output, preserving the original file. | All six roles, notes and synthetic numbers appear; no field is silently discarded. |
| DF-01.AC06 | Determinism | Canonicalize equal objects with different object-key insertion order. | Equal canonical digest; a meaningful array reorder changes the digest. |

### Windows-native acceptance additions

| ID | Scenario | Given / action | Required result |
|---|---|---|---|
| DF-01.AC07 | Logical ID on NTFS | Serialize a node ID containing a colon. | ID survives unchanged; storage uses a safe mapped name, not raw NTFS syntax. |
| DF-01.AC08 | Host code in a request | Submit an unknown operation or PowerShell expression field. | Schema rejects it before a worker or shell is launched. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```powershell
node --test .\tests\validate.test.mjs
```

For original-renderer changes, run `node scripts/build-smoke.mjs` then `py -3 scripts/inspect-pptx.py out/smoke/deck.pptx` on Windows. Legacy npm check/preview chains still use python3/LibreOffice until DF-00/DF-20 are implemented. Follow [Windows setup](../WINDOWS_SETUP.md); native render/edit receipts are separate from this unchanged smoke harness.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```powershell
npm.cmd run test:spec -- DF-01
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-01 after DF-00. Deliver schemas, types, validation, canonicalization and a smoke-input migration with tests. Do not implement a renderer or speculative provider SDK. Keep sample API signatures aligned with CONTRACTS.md.
```

## 10. Source and decision traceability

This spec decomposes Development plan PR-01 details; Architecture §6. See the bundled [active architecture](../references/ARCHITECTURE.md) and [active development plan](../references/DEVELOPMENT_PLAN.md). Those documents retain upstream audit pins and incorporate the Windows platform decision; unchanged pre-Windows sources are in the references archive. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. The Windows platform/API additions cite [official Microsoft sources](../WINDOWS_SOURCES.md); previous donor pins are retained without a new donor audit. Application/Office implementation and Windows execution are not claimed by this specification revision.
