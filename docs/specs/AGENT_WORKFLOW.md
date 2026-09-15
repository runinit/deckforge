# Coding-agent workflow for the Windows target

Read [active architecture](references/ARCHITECTURE.md), [active development plan](references/DEVELOPMENT_PLAN.md), [shared contracts](CONTRACTS.md), [Windows setup](WINDOWS_SETUP.md), [Windows Office execution](WINDOWS_OFFICE.md) and the chosen component spec. Archived pre-Windows plans are historical records, not setup instructions.

## Assignment 1: reproduce and prepare the baseline

```text
Implement DF-00 only, for native Windows 11 x64 development with PowerShell 7,
Node and Python. Read the six-slide starter before changing anything.

Inventory actual tools and native desktop Office without assuming licensing or
successful automation from COM registration. Use explicit Node and py commands
because the legacy npm inspect/check/preview scripts retain python3/LibreOffice
assumptions. Add tested portable launchers and a reviewed real dependency lock
where network access is available. Preserve the original fixture and create a
separate Windows-font variant only after an explicit font choice.

Do not implement a COM worker, agent runtime, web UI, or general Office authoring
in this patch. Do not lower script/security policy, install fonts or Office
without authorization, or overwrite unrelated files. On a non-Windows host,
record Windows/Office steps as NOT_RUN instead of substituting Linux results.

Run the existing 13 validator tests and available structural smoke checks.
Deliver changed-file summary, commands/results, pending native observations,
and the exact next DF-01 task. Update command availability only for code that
actually exists and has been checked.
```

## Assignment 2: semantic and Windows transport contracts

```text
Implement DF-01 after DF-00. Keep DeckSpec, BrandSpec and ResolvedScene portable.
Create strict schemas/types, stable semantic IDs, migration rules and the closed
OfficeRequest/OfficeResult types described in WINDOWS_OFFICE.md. Keep semantic
IDs separate from Windows physical filenames. Add negative tests and preserve
the original smoke input through an explicit adapter.

Do not put COM calls, renderer coordinates or arbitrary executable expressions
in the semantic source. Do not add Word/Excel source intake, templates or a UI.
Report unrun Windows and Office checks explicitly. Hand off DF-02 next.
```

## Assignment 3: first native PowerPoint slice

```text
Implement the first DF-20 slice only after DF-01, private job storage DF-02 and
the relevant DF-17 admission/security contract are available.

Build a strict local file request/result worker boundary, PowerShell STA host,
ownership checks and deadlines. Start with mock tests, passive inventory and
read-only native PowerPoint PNG/PDF rendering of admitted synthetic fixtures.
One attended interactive desktop job at a time; no service, Docker, SYSTEM,
public CI, arbitrary model code or global taskkill. Refuse uncertain ownership
and preserve the user’s open/unsaved documents. Never bypass Trust Center,
Protected View, sensitivity restrictions or execution policy.

Do not add chart mutations, native template assembly or Word/Excel intake in
this first patch. Verify exact unchanged source hashes, output slide mapping,
reference cleanup and per-check results. PowerPoint open success does not
establish human no-repair review, edit/save behavior or aesthetic acceptance.
```

## Assignment 4: visual milestone

Once DF-06/07/08 and native read-only review work, implement one of DF-S01, DF-S03 or DF-S08. Use the original/permitted composition contract, an explicit demo or approved company pack and both planned variants. Render minimal/normal/dense/long-label cases in PowerPoint. Keep essential content native; never shrink below policy or change a claim to fit. Record aesthetic review separately from geometry/package checks.

## Reusable bounded-task prompt

```text
Implement <SPEC-ID>, slice <named slice>, from the current checkout.
Read AGENTS.md, docs/specs/CONTRACTS.md, docs/specs/WINDOWS_OFFICE.md and the spec.
Confirm dependencies and current command availability before editing.
Preserve stable requirement/task/acceptance IDs; do not complete adjacent specs.

Use native Windows paths/processes for Office work. Keep inputs immutable and
private, one final package writer, and all native operations behind DF-20.
Use exact PASS/FAIL/WARN/NOT_RUN outcomes with artifact/environment bindings.
Do not fabricate a font, brand rule, approval, clean install or Office result.

Return changed files, implemented requirement IDs, exact tests/results, known
limitations, and the next bounded task. New interfaces remain planned until
code and their required evidence exist.
```

## Evidence and scope checks

The user requested a Windows-native plan, not permission to modify their workstation remotely. Installation and app launches happen only in the authorized execution environment. Keep secrets and customer documents out of public logs. A requested code review cannot authorize actual file mutation in Office. A test-run request for synthetic probes authorizes only the named copies.

No separate agent resets the shared repair budget. Original historical Linux test results stay historical. Product testing on Windows, native application behavior, and human acceptance are separate from documentation validation.
