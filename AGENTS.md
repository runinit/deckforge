# Deckforge development contract

Read ARCHITECTURE.md, DEVELOPMENT_PLAN.md and docs/specs/README.md. The active target is Windows 11 x64 with native desktop Office. docs/specs/CONTRACTS.md and docs/specs/WINDOWS_OFFICE.md own shared interfaces/platform rules; archived pre-Windows plans are historical only.

The bundle supplies an original smoke starter and planning documents, not a completed application. Application code/dependencies were not ported by this documentation revision. Use docs/specs/COMMANDS.md to separate implemented baseline commands from future interfaces. Prefer native Windows PowerShell/Node/Python setup; do not assume WSL tools or Linux paths.

Start with DF-00, then DF-01. Build DF-20 through the admitted private-job/security boundary; do not create ad-hoc COM calls throughout the renderer. Office operations are attended, normal-privilege, allowlisted and serialized. Never use SYSTEM/service/headless CI, arbitrary model-generated code, execution-policy bypass, global process kills or security-policy changes. Refuse uncertain application ownership.

Keep one final PPTX writer and immutable source/probe artifacts. Preserve native essential content and exact evidence/notes. Never overwrite manually edited customer PPTX files. Record native render, inspection, edit/save, human review and missing checks separately. Linux or SVG results cannot be labeled Windows PowerPoint acceptance.

Use the pinned prototype dependency before deliberate fixture-tested upgrades. Review and commit real lockfiles; do not fabricate installation evidence. Preserve historical fixture/font behavior; add an explicitly named Windows-font variant. Do not distribute fonts, company assets, credentials, private logs or customer data. Keep upstream checkouts external and no automatic provider uploads.

Implement bounded slices from the 33 specs. Preserve stable IDs, test first, keep new tasks unchecked until evidence exists, and report NOT_RUN for unavailable checks. The first visual milestone remains bridge + architecture layers + editorial hero.
