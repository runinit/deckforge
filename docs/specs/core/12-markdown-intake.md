---
spec_id: DF-12
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-05"]
depends_on: ["DF-01", "DF-02", "DF-17"]
---

# DF-12 — Markdown intake and source-span preservation

**Goal:** Convert user notes and Markdown into traceable content candidates before any narrative restructuring or design work.

**Baseline mapping:** PR-05. **Dependencies:** [DF-01](01-semantic-contracts-and-migrations.md), [DF-02](02-job-store-evidence-and-assets.md), [DF-17](17-sandbox-security-and-privacy.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own deterministic Markdown extraction, explicit boundaries, speaker-note handling and source retention reports. Do not generate a final narrative automatically, fetch arbitrary links or execute embedded HTML/code.

## 2. File ownership and integration boundary

- `packages/ingest/src/markdown/`
- `packages/ingest/tests/markdown/`
- `examples/intake/markdown/`
- `packages/contracts/schemas/content-bundle.schema.json`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
extractMarkdown(input: ApprovedSourceHandle, policy: IntakePolicy): ExtractionResult<ContentBundle>;
```
A content bundle contains source IDs/hashes, block IDs, exact source spans, normalized text, table cells, media references and note blocks. Default boundaries: explicit standalone `---` outside fenced code; otherwise H2; H1 may identify a cover. The first front-matter block is metadata, not slide content.

## 4. Requirements


### DF-12.R01 — Exact lineage

Retain line ranges and original byte/text spans; normalize for display without destroying the original representation.


### DF-12.R02 — Reliable boundaries

Ignore horizontal-rule-like text inside code fences, tables and quoted examples. Provide a boundary mode override and report ambiguous structure.


### DF-12.R03 — Factual retention

Preserve numbers, quotes, lists, links, table values, names and notes. Mark extracted assertions provided-unverified until reviewed; local extraction is not source validation.


### DF-12.R04 — Safe markup

Treat raw HTML and code as inert source content. No script execution, resource loading or automatic traversal of relative images outside allowed roots.


### DF-12.R05 — Visible losses

Unsupported syntax is retained as source plus an extraction warning. No truncation of long sections; suggest candidate splits with source spans.


### DF-12.R06 — No implicit network

Register external links as references. Fetching, when explicitly authorized later, is a separate egress-controlled operation.


## 5. Implementation tasks

- [ ] **DF-12.T01 — Build bounded parser wrapper.** Apply byte/block limits and deterministic source IDs before parsing.
- [ ] **DF-12.T02 — Extract blocks.** Support headings, paragraphs, lists, fenced code, quotes, images, tables and explicit notes syntax.
- [ ] **DF-12.T03 — Build source mapping.** Keep normalized-to-original span mapping and register extracted assets through DF-02.
- [ ] **DF-12.T04 — Produce retention report.** Report extracted/unsupported blocks, boundary decisions, notes counts and any split proposals.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `INTAKE_LIMIT` | Reject before unbounded processing. |
| `MARKDOWN_AMBIGUOUS` | Return candidate boundaries and require a deterministic selection. |
| `SOURCE_ASSET_UNSAFE` | Keep a reference warning without loading it. |
| `UNSUPPORTED_MARKUP` | Preserve source and disclose limitation. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-12.AC01 | Fence boundary | Use `---` inside a fenced code sample. | It does not create a slide boundary. |
| DF-12.AC02 | Front matter | Start with YAML-style front matter. | Metadata is not misclassified as three slide boundaries. |
| DF-12.AC03 | Numeric fidelity | Extract percentages, negative values and mixed units. | Exact original lexemes and normalized values remain traceable. |
| DF-12.AC04 | Notes | Extract explicitly marked notes across several slides. | Notes map to intended content blocks with source spans. |
| DF-12.AC05 | Unsafe link | Reference a remote image and a local path escape. | No fetch; escaped local path rejected. |
| DF-12.AC06 | Dense section | Extract a very long technical section. | Content retained with a split candidate, not silently summarized. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-12
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-12 as safe content extraction only. Add source-span and retention tests before connecting the planner. No model provider, web fetch or automatic summary belongs in this change.
```

## 10. Source and decision traceability

This spec decomposes Development plan PR-05; Architecture §§5, 12. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
