---
spec_id: DF-03
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-02"]
depends_on: ["DF-01", "DF-02"]
---

# DF-03 — Private brand capture, approval and token resolution

**Goal:** Turn actual approved company material into a versioned brand pack that permits visually varied presentations without inventing company identity.

**Baseline mapping:** PR-02. **Dependencies:** [DF-01](01-semantic-contracts-and-migrations.md), [DF-02](02-job-store-evidence-and-assets.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own candidate brand rules, source authority, approval, co-branding, font requirements and deterministic token resolution. Human approval is required for company rules. Do not scrape connected company accounts or provision font binaries automatically.

## 2. File ownership and integration boundary

- `packages/brand/src/capture/`
- `packages/brand/src/resolve/`
- `packages/brand/tests/`
- `packs/brands/demo/`
- `packages/contracts/schemas/brand.schema.json`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed API:
```ts
captureBrand(sources: BrandSourceBundle): BrandCandidate;
validateBrand(pack: unknown): ValidationResult<BrandSpec>;
resolveBrand(pack: ApprovedBrandPack, brief: Brief, overrides: ApprovedOverride[]): ResolvedBrand;
```
Private pack files: `manifest.json`, `visual.tokens.json`, `layout-policy.json`, `voice.md`, `terminology.json`, `fonts.manifest.json`, `evidence/brand-decisions.json`, and approved asset/template references. The public demo pack is clearly marked synthetic.

## 4. Requirements


### DF-03.R01 — Authority and approval

Track each rule as official, observed, proposed or deprecated, with source locator, confidence where inferred, and a separate reviewer approval. An observed old deck does not override an official guide.


### DF-03.R02 — Visual coverage

Capture typography roles, palette pairings, spacing, image treatment, diagram style, density, logo clearspace, disclaimers, layout preferences and rejected examples—not only color values.


### DF-03.R03 — Three treatments

Define executive-editorial, technical-diagram and keynote-impact treatments using the same approved identity. A treatment can change composition but cannot introduce unapproved fonts, logos or factual claims.


### DF-03.R04 — Conflict resolution

Apply policy precedence from CONTRACTS.md. Surface contradictory protected rules; do not choose a compromise brand color or delete mandatory copy to fit a layout.


### DF-03.R05 — Co-branding

Allow customer marks only through an explicit combination policy defining placement, relative size, color use and protected identity. Missing permission or rules blocks that treatment.


### DF-03.R06 — Font handling

Record local font names, weights, licensing/install instructions and fingerprints. Resolve actual files for measurement at runtime; missing required fonts are diagnostics, never silently substituted.


## 5. Implementation tasks

- [ ] **DF-03.T01 — Capture source inventory.** Create a candidate manifest from explicitly supplied material, recording authority and version. Keep files in the external private root.
- [ ] **DF-03.T02 — Create demo and candidate packs.** Use the synthetic demo to exercise tokens and schema. Produce a private candidate pack without labeling it approved.
- [ ] **DF-03.T03 — Implement resolver.** Expand token aliases, reject cycles/unknown tokens and apply approved exceptions with review records.
- [ ] **DF-03.T04 — Build approval workflow.** Present three treatments with identical content plus a rule-by-rule diff. Approval binds the exact pack and preview digests.
- [ ] **DF-03.T05 — Test leakage.** Inspect notes, HTML, source labels, logs and release manifests for unrelated private references.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `BRAND_UNAPPROVED` | Allow a watermarked draft only when policy permits; block approved release. |
| `BRAND_CONFLICT` | List rule IDs requiring resolution. |
| `FONT_MISSING` | Stop affected layouts or request an explicit approved fallback. |
| `TOKEN_CYCLE` | Return the alias chain. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-03.AC01 | No corporate input | Capture with no supplied company guide/template. | Only a demo or incomplete candidate is produced; no Ferroque defaults are invented. |
| DF-03.AC02 | Conflicting guides | Two official sources disagree on a protected font. | Resolver returns a conflict needing an authority decision. |
| DF-03.AC03 | Token cycle | A token ultimately references itself. | Validation fails before layout. |
| DF-03.AC04 | Approval freshness | Change one palette token after approval. | The prior approval is invalidated. |
| DF-03.AC05 | Brand variety | Render the same brief in three approved treatments. | Composition differs while protected identity stays identical. |
| DF-03.AC06 | Co-brand denial | Add a customer mark with no co-brand policy. | No automatic logo combination is exported. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-03
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-03 using only the demo pack until approved private material is explicitly provided. Build candidate/approval separation, deterministic resolution and three-treatment support. Do not pretend smoke colors represent Ferroque.
```

## 10. Source and decision traceability

This spec decomposes Architecture §7; Development plan PR-02. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
