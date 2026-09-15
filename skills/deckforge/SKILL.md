---
name: deckforge
description: Develop and test this hybrid native-PowerPoint presentation framework. This checkout currently contains a smoke renderer, not the complete presentation product.
---

Read ARCHITECTURE.md and DEVELOPMENT_PLAN.md before changing behavior.

Use one orchestrator. Do not load all upstream presentation skills as co-equal instructions.
Keep brand and customer inputs outside the public repository. The smoke palette is not Ferroque branding.
Run `npm test`, `npm run smoke`, and `npm run inspect` after renderer changes.
Run `npm run preview` when LibreOffice and Poppler are available; inspect all six pages.
Treat a missing check as NOT RUN. Never call the output Office-approved without a PowerPoint edit/save receipt.
Do not replace native text, data tables, or charts with full-slide images to make a failing layout pass.
Future task commands listed in the plan do not exist until explicitly implemented and tested.
