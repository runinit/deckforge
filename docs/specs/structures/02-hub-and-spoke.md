---
spec_id: DF-S02
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-03"]
depends_on: ["DF-06", "DF-07", "DF-08", "DF-09"]
---

# DF-S02 — Hub-and-spoke ecosystem composition

**Goal:** Explain ecosystem relationships around a dominant central service without implying connections or directions that the content does not establish.

**Baseline mapping:** PR-03. **Dependencies:** [DF-06](../core/06-structure-pack-sdk-and-registry.md), [DF-07](../core/07-layout-text-and-scene-compiler.md), [DF-08](../core/08-reference-pptx-writer.md), [DF-09](../core/09-native-charts-tables-and-connectors.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own `hub-spoke` pack 1.0.0. Variants: `radial-orbit` for compact symmetric networks and `split-orbit` for longer labels arranged on two sides.

## 2. File ownership and integration boundary

- `packs/core/hub-spoke/`
- `tests/structures/hub-spoke/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Content defines one hub node, 2–6 spoke nodes and explicit hub↔spoke edge records. Each edge has `from`, `to`, direction (`none`, `forward`, `both`) and optional label. Node and port IDs are stable.

No inferred edges are added. The brief/slide requiredCapabilities selects anchored edges or plain native lines; the pack does not silently relax anchoring. Decoration may include a faint orbit but cannot imply an additional real relationship.

## 4. Requirements


### DF-S02.R01 — Layout

Reserve title/footer bands; place hub in the diagram’s central emphasis region. For radial-orbit, use deterministic angular placement; for split-orbit, use two measured label columns with a central hub.


### DF-S02.R02 — Native labels

Hub and spoke text remain native. Approved vendor icons may be SVG/image assets, with text separately editable.


### DF-S02.R03 — Edges

Route edges behind nodes, reserve label regions and preserve direction. Arrowheads must reflect supplied semantics. Plain line mode is visibly disclosed when anchoring is not required.


### DF-S02.R04 — Selection

Use split-orbit when radial labels would collide or content approaches capacity. More than six spokes proposes a hierarchy/split, not smaller type.


### DF-S02.R05 — Visual hierarchy

Make the hub dominant through region/typography/emphasis, not by deleting spoke details. Avoid decorative orbit lines that could be read as missing data edges.


## 5. Implementation tasks

- [ ] **DF-S02.T01 — Implement radial geometry.** Place nodes with stable ordering and explicit orientation; create semantic edge routes.
- [ ] **DF-S02.T02 — Implement long-label variant.** Measure each side column and space edge exits to avoid crossings.
- [ ] **DF-S02.T03 — Add anchoring negotiation.** Test native-line and anchored requests independently through DF-09.
- [ ] **DF-S02.T04 — Review representative ecosystems.** Use synthetic service labels with and without approved icon assets.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `GRAPH_REFERENCE_INVALID` | Reject absent node/port IDs. |
| `HUB_CAPACITY` | Return a supported alternative. |
| `ANCHOR_UNVERIFIED` | Block required anchoring. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-S02.AC01 | Minimal | Hub plus two spokes with undirected edges. | No arrowheads are invented. |
| DF-S02.AC02 | Normal | Four spokes with mixed explicit directions. | Direction and labels match source. |
| DF-S02.AC03 | Dense | Six spokes with long labels. | Split-orbit or explicit split; no clipped labels. |
| DF-S02.AC04 | Required anchor | Request anchored edges on unsupported backend. | Build fails instead of drawing unanchored substitutes. |
| DF-S02.AC05 | Move node | In a supported anchor fixture, move a spoke and save/reopen. | Edge remains connected, or capability is withdrawn. |
| DF-S02.AC06 | Icon unavailable | Remove an optional vendor icon. | Readable native label remains; asset failure follows approved fallback policy. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-S02
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-S02 with explicit edge semantics and two variants. Native-line and anchored modes must remain different capabilities. Do not add decorative arrows that change the meaning.
```

## 10. Source and decision traceability

This spec decomposes Architecture §8.3; Development plan PR-03, F07. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
