# Historical non-Windows execution record

**Scope warning for windows-office-1:** the original report below describes the earlier artifact-building environment only. It is not evidence of a Windows install, PowerShell execution, native PowerPoint rendering, Excel/Word automation or the new Office worker. The application source remains unchanged. Current documentation checks are in [VALIDATION_REPORT.md](../../VALIDATION_REPORT.md).

---

# Local execution report

**Date:** 2026-09-15.  
**Subject:** the original supplied smoke starter, not the complete proposed hybrid system.

## Environment

| Component | Observed |
|---|---|
| Node.js | 22.16.0 |
| npm | 10.9.2 |
| Python | 3.13.5 |
| PptxGenJS | Preinstalled 4.0.0 |
| LibreOffice | 25.2.3.2 |
| Poppler | `pdftoppm` available and executed |
| Demo font | Liberation Sans available locally; no font binary distributed |
| Network from execution runtime | Unavailable; separate web/GitHub research tools worked |

The local runtime used a symlink to the preinstalled PptxGenJS package. That link and `node_modules` are excluded from the archive. This is why the package version is exact but no untested lockfile is invented.

## Executed checks

| Check | Result | Scope |
|---|---|---|
| `npm test` | **PASS: 13/13** | Synthetic input validity, schema version, IDs, supported structures, notes, chart data/provenance/scale, density, table dimensions |
| `npm run smoke` | **PASS** | Six-slide native-PPTX generation |
| `npm run inspect` | **PASS** | Fixture-specific XML/relationship/object checks |
| Negative package probe | **PASS** | Removing the native chart part caused inspection failure |
| `npm run preview` | **PASS** | Fresh PDF and six PNG pages from actual generated PPTX |
| Contact-sheet inspection | **REVIEWED** | All six pages viewed; no obvious clipping or unintended overlap observed on this fixture |
| JS syntax checks | **PASS** | Supplied ESM source, script and tests |
| Python syntax compilation | **PASS** | Supplied Python helpers |
| Upstream fetch helper `--help` | **PASS** | Argument parsing only; no clone executed |
| Presenton helper print-only mode | **PASS** | Command plan emitted; Docker not launched |
| Tool inventory | **PASS** | Read-only local doctor ran |

## Structural output

```json
{
  "slides": 6,
  "text_boxes": 45,
  "native_shapes": 66,
  "native_tables": 1,
  "native_charts": 1,
  "pictures": 0,
  "notes": 6,
  "embedded_workbooks": 1
}
```

`native_shapes` counts `p:sp` elements, including text shapes; it is not a count of 66 additional diagram objects. A native chart and workbook are present, but the PowerPoint **Edit Data** operation has not been exercised.

## Not run

Clean online npm installation; upstream Git clone execution; upstream package installs/test suites; Impeccable installation; Presenton/Docker startup; PPTKit adapter/export; company brand or corporate-template intake; malicious-upload isolation testing; Windows/macOS Microsoft PowerPoint open/edit/save/reopen; general arbitrary-content generation; statistical visual-quality benchmarking.

The mock data and demo palette are synthetic. No claim is made that the fixture satisfies Ferroque's brand or represents the final intended aesthetic quality. It establishes a runnable native-editability baseline from which the visual packs and brand system can be built.

## Reproduction after download

```sh
npm install
npm run check
npm run preview
```

Record the newly generated lockfile and local versions. Raw PPTX SHA-256 values can change across builds because ZIP/package metadata may include timestamps. Compare normalized structures and rendered content rather than assuming byte-identical output.
