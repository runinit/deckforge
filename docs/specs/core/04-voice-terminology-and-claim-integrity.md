---
spec_id: DF-04
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-02"]
depends_on: ["DF-01", "DF-03"]
---

# DF-04 — Voice, terminology and claim-preserving rewrites

**Goal:** Produce company-appropriate headlines and notes without turning qualified facts into promises or importing another customer’s narrative.

**Baseline mapping:** PR-02. **Dependencies:** [DF-01](01-semantic-contracts-and-migrations.md), [DF-03](03-brand-capture-and-resolution.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own voice-rule representation, deterministic text lint, approved/rejected pairs and rewrite proposals. Do not make an LLM a mandatory runtime dependency or silently rewrite content during layout fitting.

## 2. File ownership and integration boundary

- `packages/brand/src/voice/`
- `packages/brand/tests/voice/`
- `packages/contracts/schemas/rewrite-proposal.schema.json`
- `examples/voice/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
lintVoice(text: TextFragment, rules: ApprovedVoiceRules): VoiceFinding[];
validateRewrite(before: TextFragment, proposal: RewriteProposal, evidence: EvidenceIndex): RewriteReview;
applyRewrite(deck: DeckSpec, proposal: ApprovedRewrite, expectedRevision: number): DeckPatch;
```
Each proposal names the content ID, before/after text, reason, relevant rule IDs, preserved evidence IDs and claim-change classification. Numeric/unit/qualifier checks are deterministic where possible; uncertain semantic equivalence is REVIEW_REQUIRED.

## 4. Requirements


### DF-04.R01 — Protected facts

Lock numbers, units, names, product versions, dates, negation and qualifiers unless an approved correction explicitly changes them. Detect “may reduce” becoming “will eliminate”.


### DF-04.R02 — Different checks

Separate brand preference, terminology correctness and claim fidelity. A strong brand score cannot compensate for a changed claim.


### DF-04.R03 — Operational voice

Store preferred and rejected phrases with reasons and audience applicability. Headlines should state a point when evidence supports it; do not fabricate benefits merely to avoid a topic heading.


### DF-04.R04 — User review

A rewrite is a proposed patch. Changes to quotes, legal text, customer names, technical claims or assumptions require explicit review before application.


### DF-04.R05 — Private examples

Retrieve only from the selected brand and allowed customer context; examples are style evidence, not reusable customer facts.


### DF-04.R06 — No shrink rewrite

Layout may request a shorter alternative with an explanation, but cannot apply that text automatically.


## 5. Implementation tasks

- [ ] **DF-04.T01 — Represent voice rules.** Implement terminology aliases, preferred constructions, banned phrases, protected strings and paired examples with source IDs.
- [ ] **DF-04.T02 — Build deterministic lint.** Check exact product spelling, forbidden placeholders, required qualifiers and token-preservation invariants.
- [ ] **DF-04.T03 — Build proposal validation.** Compare before/after facts, attach uncertainty warnings and generate a reviewable diff.
- [ ] **DF-04.T04 — Integrate approved patch.** Apply only an approved proposal against the expected revision; invalidate narrative/content review receipts as appropriate.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `CLAIM_CHANGED` | Return protected token/qualification differences. |
| `VOICE_REVIEW_REQUIRED` | Keep as a proposal; do not guess semantic equivalence. |
| `PROTECTED_TEXT` | Require explicit authorized correction. |
| `REVISION_CONFLICT` | Regenerate the proposal from current content. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-04.AC01 | Changed guarantee | Rewrite “may reduce operating effort” as “eliminates operating effort”. | Flag claim strengthening; block automatic application. |
| DF-04.AC02 | Changed magnitude | Rewrite 500 users as 5,000 or 10% as 10 percentage points. | Reject numeric/unit mismatch even if prose sounds better. |
| DF-04.AC03 | Protected quotation | A stylistic rewrite alters an attributed quotation. | Requires explicit quote correction; never passes as a normal voice edit. |
| DF-04.AC04 | Terminology alias | Replace an approved deprecated product label with its approved display alias. | Record a rule-based suggestion, preserving source terminology in provenance. |
| DF-04.AC05 | Audience variation | Produce executive and technical wording for the same approved claim. | Evidence and qualification remain; reviewer can accept either wording. |
| DF-04.AC06 | Stale proposal | Apply a rewrite against a newer source revision. | Conflict returned; no replacement of user edits. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-04
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-04 as lint and patch validation first. Use synthetic approved/rejected pairs. Preserve facts and qualifiers independently of voice preference; do not add an unattended writer.
```

## 10. Source and decision traceability

This spec decomposes Architecture §§6.1, 7, 11; Development plan PR-02, PR-04. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
