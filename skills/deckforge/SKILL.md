---
name: deckforge
description: Implement and review the Deckforge Windows-native presentation framework from its architecture and component specs. Use for work on this repository; this is not a finished arbitrary-deck generation skill.
---

# Deckforge development workflow

Read AGENTS.md, ARCHITECTURE.md, DEVELOPMENT_PLAN.md and docs/specs/README.md from the repository root. Then read docs/specs/CONTRACTS.md, docs/specs/WINDOWS_OFFICE.md, docs/specs/COMMANDS.md and the requested component spec. Follow the bounded assignments in docs/specs/AGENT_WORKFLOW.md.

Use Windows 11 x64, native Windows Node/Python and PowerShell as the initial target. The existing six-slide fixture is a regression baseline; the native Office host and application interfaces remain TO IMPLEMENT until delivered. Do not claim native PowerPoint behavior from SVG, LibreOffice, mocks, COM registration or documentation checks.

Preserve one package writer, native essential labels/data, approved brand authority and original sources. Native Office operations belong only to DF-20's allowlisted attended worker. No service/container/SYSTEM execution, arbitrary COM expressions, global process kills, security bypass or overwrite of user-edited documents. Use separate immutable probe copies and exact receipt hashes.

Begin with the requested spec only. Run existing tests and add slice-specific acceptance. Report actual commands/results and NOT_RUN checks. Keep private brand packs, customer inputs, fonts and credentials out of the public repository and optional external services.
