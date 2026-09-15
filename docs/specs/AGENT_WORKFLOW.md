# Coding-agent workflow

## 1. Read only the necessary context

Start with the target spec, [CONTRACTS.md](CONTRACTS.md), [COMMANDS.md](COMMANDS.md) and the relevant dependency specs. Read the original architecture when a decision is unclear. Do not load all 31 specs or all upstream skills into every task.

The real repository and executed tests determine implementation status. The manifest in this pack describes planned ownership and dependencies; it is not an implementation-completion ledger.

## 2. Task protocol

1. Inspect the current checkout and existing work before changing files. Read `AGENTS.md`; do not overwrite local edits or assume the starter is untouched.
2. Check the target spec dependencies and implemented command availability. Run the relevant existing baseline tests and record actual outcomes.
3. Select a bounded subset of numbered tasks. State the exact files/contracts that will change and the acceptance cases those tasks cover.
4. Implement one vertical slice; add meaningful fixtures. Preserve schema/renderer/privacy boundaries and original regression coverage.
5. Run the implemented tests. Missing suites and unavailable tools remain NOT_RUN, not PASS.
6. Report changed files, completed task IDs, test logs, unresolved requirements and the next dependency-ready task. Do not claim the whole spec is complete because one helper or showcase works.

## 3. First task: baseline

From the actual project root, paste:

```text
Read AGENTS.md and docs/specs/core/00-baseline-and-workspace.md.
Read docs/specs/COMMANDS.md and references/STARTER_INVENTORY.md beneath docs/specs.

Implement DF-00 only. Start by inspecting existing edits and running the original
smoke tests. Preserve the synthetic input, source and semantics. Create a real
reviewed dependency lock only when installation can run; do not fabricate an
online-install result. Add the explicit spec-test dispatcher and its own tests.
Unknown IDs, missing suites and empty selections must fail.

Do not publish a repository, reset upstream checkouts, start Docker, install all
skills, copy corporate files, or change the PptxGenJS version in this task.

Deliver changed-file summary, completed DF-00 task IDs and actual test evidence.
Record unavailable application checks as NOT_RUN. Stop before implementing DF-01.
```

## 4. Second task: semantic contracts

```text
Read AGENTS.md, docs/specs/CONTRACTS.md and
 docs/specs/core/01-semantic-contracts-and-migrations.md.
Confirm DF-00 prerequisites in the real checkout; do not infer them from docs.

Implement DF-01 only: strict production contracts, stable IDs, schema validation,
canonicalization and an explicit migration from the existing smoke input.
Preserve original files and distinguish the smoke schema from DeckSpec 1.0.
Choose and lock one schema/typechecking approach. Use exact shared field names.

Add tests for unknown fields, duplicate/broken references, non-finite values,
structure-content mismatches, identity preservation and loss-report behavior.
Do not create empty packages for the rest of the architecture, add model SDKs,
create a UI or integrate Presenton/PPTKit in this change.

Return completed requirement/task IDs, test evidence, design decisions and
remaining limits. Stop before writing the general compiler.
```

## 5. Reusable task template

Replace the bracketed task identifiers deliberately; this is a prompt template, not a shell command.

```text
Target: [spec ID and Markdown path]
Task scope: [specific numbered task IDs]

Read this spec, CONTRACTS.md, COMMANDS.md and only relevant dependency specs.
Inspect current repository state and preserve unrelated work.

Implement only the stated tasks. Coordinate shared-schema/root-package/registry
changes rather than silently modifying another workstream's contract. Use one
PPTX writer, native essential content, reviewed brand rules and private job roots.
No execution of model-generated code; no hidden remote calls or package installs.

Run the acceptance tests applicable to this slice plus the existing smoke
regression when affected. Report PASS/FAIL/WARN/NOT_RUN honestly. Include final
PPTX rendering and application-review state only when export behavior is involved.

Return:
- Changed paths and completed task/requirement IDs.
- Commands executed and results, fixture/environment hashes where applicable.
- Unimplemented or blocked acceptance cases.
- Contract changes requiring coordinator review.
- One bounded next task.
```

## 6. Review and merge discipline

A contributor owns only the paths listed in its spec, subject to coordinated shared-file changes. New dependency pins, schema fields, capability claims, corpus entries and public assets need explicit review. A working screenshot does not justify bypassing native data, provenance or Office checks.

Merge criteria are feature-specific: an interface-only change can be complete without rendering, while a writer/pack change needs its actual output inspected. Manual PowerPoint/brand approval cannot be fabricated by a coding agent. No source/provider credentials or private brand examples belong in public test evidence.

## 7. Completion report template

```text
Spec / task slice:
Commit / branch:
Changed files:
Requirements completed:
Acceptance cases passed:
Acceptance cases failed:
Checks NOT_RUN and why:
Final artifact / scene / environment hashes, where applicable:
Known limitations:
Shared-contract decisions needing review:
Next bounded task:
```
