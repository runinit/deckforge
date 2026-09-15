# Deckforge: Windows and native Office plan

A presentation compiler/design-pack system for company brand and voice, ambitious reusable slide compositions, and editable native PowerPoint. **Primary target: Windows 11 x64 with desktop PowerPoint, Excel and Word.** Word/Excel intake is optional; the first deliverable remains a branded PPTX.

This bundle contains the updated architecture/development plan, 33 implementation specs and the unchanged six-slide smoke starter. **The Office worker, production compiler, native template backend, CLI and source importers are planned, not implemented here.** No company brand assets, font binaries, Office software or upstream implementation is redistributed.

## Start here

| Document | Purpose |
|---|---|
| [Windows setup](docs/specs/WINDOWS_SETUP.md) | PowerShell setup, guarded extraction, private paths, baseline and manual Office checks |
| [Architecture](ARCHITECTURE.md) | System ownership, native Office boundary, design packs and editability |
| [Development plan](DEVELOPMENT_PLAN.md) | Setup, implementation backlog, beta experiments and commands |
| [Spec index](docs/specs/README.md) | 22 core specs, eight structure packs and three experiments |
| [Windows execution contract](docs/specs/WINDOWS_OFFICE.md) | Attended Office worker, COM ownership, native rendering, security and receipts |
| [Implementation order](docs/specs/IMPLEMENTATION_ORDER.md) | Baseline → contracts → native review → brand/showcase structures |
| [Change log](docs/specs/WINDOWS_CHANGELOG.md) | What changed from the prior Linux-oriented delivery |

## Current baseline on Windows

Run from the new extracted `deckforge` directory after installing native Node/Python. Stop if any command fails. Use `npm.cmd ci` only after a real reviewed lockfile exists.

```powershell
npm.cmd install
node --test .\tests\validate.test.mjs
node .\scripts\build-smoke.mjs .\examples\smoke-deck.json .\out\smoke
py -3 .\scripts\inspect-pptx.py .\out\smoke\deck.pptx
py -3 .\docs\specs\tools\validate_specs.py
```

The historical fixture requests Liberation Sans and contains six synthetic native slides. Record font availability/substitution in PowerPoint; a Windows-font fixture is a separate DF-00 task. The existing npm inspect/check/preview chains still call `python3`/LibreOffice; they have not been silently replaced by a native worker. Follow [command availability](docs/specs/COMMANDS.md).

For now, use PowerPoint manually on a copy to render, edit chart/table/text, save and reopen. Future native `deck doctor`, `deck qa --render powerpoint` and Office probe commands are explicitly TO IMPLEMENT. No Windows application test has been executed by this documentation update.

## Design and delivery boundaries

One final package writer per deck; actual PowerPoint rendering is distinct from SVG/HTML preview. The first showcase compositions are bridge, architecture layers and editorial hero. Charts/tables/critical labels must stay native rather than become decorative screenshots. Approved corporate brand rules outrank generic upstream design preferences.

Office runs in an attended signed-in desktop session. Public CI/WSL/Docker do not host the native Office worker. Preserve the operator's open documents, create immutable probe copies, reject unsafe input before Office, and keep private packs/customer data outside this public source tree.

Original starter code remains MIT licensed. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). [Historical test report](docs/LOCAL_TEST_REPORT.md) describes the earlier non-Windows run; [current documentation validation](docs/specs/VALIDATION_REPORT.md) is not product or Office acceptance.
