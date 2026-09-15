# Deckforge — audited architecture and executable starter

An open-source **presentation design/compilation framework** concept: approved company brand and voice, attractive reusable structures, native PowerPoint, and explicit beta-engine experiments.

This delivery includes the design and development plans plus a small native-PPTX smoke harness. **It is not the completed hybrid product.** No Astra implementation, company brand assets, font binaries or upstream repositories are redistributed here.

## Read first

- [Architecture and audit](ARCHITECTURE.md): integration corrections, reuse/fork decisions, source pins, data contracts, design packs, editability, template limits and QA.
- [Development plan](DEVELOPMENT_PLAN.md): setup commands, agent integration, upstream experiments, PR backlog, acceptance fixtures and future CLI contract.
- [Local test report](docs/LOCAL_TEST_REPORT.md): what was actually executed and what remains unverified.

## Run the native baseline

Requires Node 22+, npm and Python 3. LibreOffice and Poppler are optional for preview.

```sh
python3 scripts/doctor.py
npm install
npm run check
npm run preview
```

`npm install` needs network and creates the first real lockfile. The local execution used preinstalled PptxGenJS 4.0.0; a clean registry install was not performed. Commit your resulting lockfile, then use `npm ci` for subsequent reproduction.

The output is `out/smoke/deck.pptx`: six synthetic slides with native text/shapes, one chart, one table and speaker notes. The supplied chart fixture accepts values from 0 to 100 because its demonstration axis is fixed to that range.

The preview helper renders the actual file through LibreOffice. It does not certify Microsoft PowerPoint compatibility. A human should edit a heading, table cell and chart data, save/reopen, and check for repair warnings.

## Useful implemented commands

```sh
npm test
npm run smoke
npm run inspect
npm run preview
python3 scripts/fetch-upstreams.py --help
python3 scripts/start-presenton-lab.py
```

The last command is **print-only**. Add `--start` only when intentionally launching the optional local Docker experiment. No provider credentials are included.

There is no `deck` executable yet. Future commands in the development plan are marked **TO IMPLEMENT**. The included skill is a development guide for the repository, not an autonomous finished-deck generator.

## Boundaries

The core plans use one final PPTX writer per deck, while allowing different composition providers and decorative artwork. Essential text, charts and tables must not silently become images. The first implementation track includes visually ambitious structures; it is not limited to bullet templates.

Keep corporate templates, private brand rules, client inputs and proprietary fonts outside this public repository. The example palette is not a Ferroque brand specification.

Original starter code is MIT licensed. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency and upstream provenance boundaries.
