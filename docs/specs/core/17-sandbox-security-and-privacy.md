---
spec_id: DF-17
status: proposed
implementation_status: not_implemented_by_this_delivery
source_prs: ["PR-04", "PR-05", "PR-08"]
depends_on: ["DF-02"]
---

# DF-17 — Sandbox, privacy and controlled external services

**Goal:** Constrain untrusted files, HTML, plugins and external-model access before real company material enters those paths.

**Baseline mapping:** PR-04, PR-05, PR-08. **Dependencies:** [DF-02](02-job-store-evidence-and-assets.md)

**Read first:** [shared contracts](../CONTRACTS.md), [command availability](../COMMANDS.md), and [implementation order](../IMPLEMENTATION_ORDER.md). This is an implementation specification, not a claim that the component exists. DF-00 extends an existing starter; all new behavior below remains planned.

## 1. Scope and non-goals

Own security policy, worker isolation, input resource limits, sanitization, egress decisions and publication rules. Basic filesystem confinement is DF-02. This task does not certify all upstream dependencies as safe or rely on a local URL as proof of privacy.

## 2. File ownership and integration boundary

- `packages/security/src/`
- `packages/security/tests/`
- `workers/office/`
- `workers/browser/`
- `config/security-policy.example.json`
- `tests/fixtures/security/`

These are proposed ownership paths, not a list of files already present. Create a package only when implementing its boundary. Changes to shared schemas require DF-01 review; updates to root scripts/dependencies/test mappings must be coordinated with DF-00. A spec may add its own test registration, but may not silently rewrite another component’s contract.

## 3. Inputs, outputs and interface

Proposed policy contains source/expanded-byte/entry/time/process limits, allowed file types, forbidden XML/entity/executable content, permitted source roots, output scope, allowed network destinations and provider data classifications.

Initial proposed test defaults: 50 MiB uploaded package, 250 MiB total expanded data, 10,000 ZIP entries, 100:1 per-entry expansion ratio, 120-second extraction timeout and 180-second render timeout. These are starting project limits, not measured safe maxima; make them configurable and test both sides of each boundary.

## 4. Requirements


### DF-17.R01 — Worker isolation

Run converters/browsers as non-root with disposable writable workdir, bounded CPU/memory/time, read-only source copy and networking denied. No home directory, SSH keys, host Docker socket or public-repository secrets mounted.


### DF-17.R02 — Preflight

Enforce archive quotas while streaming, path confinement, XML DTD/entity restrictions, media type checks and relationship allowlists. Reject macros/executable content in the first product.


### DF-17.R03 — Separate egress

Fetch/model/image/telemetry stages require an explicit allowlist and sensitivity policy. No provider call from the compiler or document renderer; no silent fallback to another remote provider.


### DF-17.R04 — No code from model output

Model responses are schema-validated data/proposals. Do not eval, shell-expand or import model-generated code in a job worker.


### DF-17.R05 — Logging and publication

Use IDs/digests and sanitized diagnostics. Scan public artifacts/CI uploads for private paths, names, keys and disallowed assets; `.gitignore` is not the enforcement boundary.


### DF-17.R06 — Research services

Bind experiments to loopback, use synthetic inputs and isolated volumes. A self-hosted app can still call external services; record configured egress explicitly.


### DF-17.R07 — Failure containment

Time/memory/format failures terminate only the job worker, preserve a sanitized incident report and do not publish partial success.


## 5. Implementation tasks

- [ ] **DF-17.T01 — Define threat/egress model.** List inputs, trusted components and capabilities with defaults denying unnecessary access.
- [ ] **DF-17.T02 — Build workers.** Create isolated renderer/parser contracts with controlled files and structured results, without mandating one cloud provider.
- [ ] **DF-17.T03 — Add malicious fixtures.** Test archive traversal, entity expansion, huge decompression, external image/relationship loading and model-output injection.
- [ ] **DF-17.T04 — Add egress/publication checks.** Simulate unapproved endpoints and private metadata leaking into notes, logs, previews and package manifests.
- [ ] **DF-17.T05 — Document exceptions.** Allow explicit per-job override of resource limits with evidence; do not silently weaken macro or arbitrary-code policy.

Implement in this order unless a listed dependency needs a documented change. Keep each commit testable. Do not interpret the whole spec as permission to implement unrelated roadmap items.

## 6. Failure behavior

| Diagnostic | Required behavior |
|---|---|
| `SECURITY_POLICY_DENIED` | Stop the operation without exposing secrets. |
| `WORKER_RESOURCE_LIMIT` | Return the exceeded bound and safe next action. |
| `UNSAFE_DOCUMENT` | Reject executable/unsupported active content. |
| `EGRESS_DENIED` | Do not retry through a different provider. |

Return stable diagnostic codes plus affected IDs/JSON pointers. Command adapters map them to the common exit-code policy. Never turn an unsupported, failed or unexecuted check into PASS.

## 7. Acceptance tests

Every row is a test requirement, **not an executed result**. Implement deterministic fixtures where possible; record application/human checks separately.

| Test ID | Scenario | Exercise | Expected result |
|---|---|---|---|
| DF-17.AC01 | Host file read | Source HTML attempts to read host home/keys. | Not mounted or accessible; worker report has no leaked contents. |
| DF-17.AC02 | Network request | Office relationship or HTML image targets the network. | Denied and recorded without fetching. |
| DF-17.AC03 | ZIP/XML abuse | Use traversal, excessive compression and external entity fixtures. | Rejected or killed within configured limits. |
| DF-17.AC04 | Model code | Return a field containing executable code or shell substitution. | Rejected as schema/data; never executed. |
| DF-17.AC05 | Private note leak | Generated notes include a confidential full path. | Publication/privacy gate fails. |
| DF-17.AC06 | Timeout | Hang a rendering worker. | Worker terminates, job remains failed/not released, other jobs unaffected. |
| DF-17.AC07 | Provider classification | Try to send confidential content to an unapproved provider. | No request is sent. |

## 8. Verification commands and evidence

**Available now in the original starter:**
```sh
npm test
```

For changes that affect the original renderer, also run the existing `npm run check` and, when available, `npm run preview`. These validate the smoke baseline, not all requirements in this spec.

**TO IMPLEMENT — after the spec-test dispatcher and this suite exist:**
```sh
npm run test:spec -- DF-17
```

Record the exact command, commit, runtime/dependency versions, fixture hashes and PASS/FAIL/WARN/NOT_RUN status. See [command lifecycle](../COMMANDS.md). A missing suite or missing Office application is not a passing result.

## 9. Definition of done and handoff

All requirements have implementation or a documented explicit blocker. Required tests have evidence, public examples contain only synthetic/permitted material, and the original smoke workflow still behaves as documented. Export-related work includes a final-artifact inspection and honest Office-review state; interface-only work does not fabricate those artifacts.

Return changed-file summary, completed task IDs, test evidence, remaining limitations and the next dependency-ready task. Use [the agent workflow](../AGENT_WORKFLOW.md) to bound the assignment.

**Focused coding-agent assignment:**

```text
Implement DF-17 before arbitrary-file or third-party-service handling. Use synthetic hostile fixtures. Test actual denial rather than only presence of config flags; do not put company material in experimental workers.
```

## 10. Source and decision traceability

This spec decomposes Architecture §12; Development plan PR-05, §8, §11 F11–F12. See the bundled [architecture baseline](../references/ARCHITECTURE.md) and [development-plan baseline](../references/DEVELOPMENT_PLAN.md). Those documents contain the original upstream source register and audit pins. Proposed APIs, capacity limits and new test cases here are project decisions, not claims about currently implemented upstream APIs. No new upstream audit or application implementation is claimed by this spec pack.
