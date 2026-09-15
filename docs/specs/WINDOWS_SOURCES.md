# Windows and native Office source register

**Checked:** 2026-09-15. These Microsoft sources support the added platform/API facts. The worker design, job limits, default versions, approval rules and test thresholds are Deckforge design decisions, not promises made by Microsoft. No Windows or Office code was executed in this documentation revision. Earlier third-party repository pins are retained from the prior audit and were not re-audited here.

| ID | Official source | Supported fact / use |
|---|---|---|
| W01 | [Office automation deployment considerations](https://support.microsoft.com/en-us/visio/considerations-for-server-side-automation-of-office) | Office expects an interactive user/profile; unattended non-interactive/server-side automation is not supported. |
| W02 | [Presentations.Open](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.presentations.open) | File, read-only, untitled-copy and window parameters; returns a Presentation. |
| W03 | [Slide.Export](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.slide.export) | Native slide graphics export with explicit pixel dimensions. |
| W04 | [Presentation.ExportAsFixedFormat](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.presentation.exportasfixedformat) | Native PDF/XPS export; static output, missing-font and IRM/label options. |
| W05 | [TextRange2.BoundHeight](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.textrange2.boundheight) | Text bounding geometry in points; text bounds differ from the containing frame. |
| W06 | [ChartData.Activate](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.chartdata.activate) | Activate chart data before reading its Workbook property. |
| W07 | [Presentation.SaveCopyAs](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.presentation.savecopyas) | Save a presentation copy without modifying the original. |
| W08 | [PowerPoint AutomationSecurity](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.application.automationsecurity) | Macro-disabling mode for programmatic opens; DisplayAlerts does not suppress security warnings. |
| W09 | [ConnectorFormat.BeginConnect](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.connectorformat.beginconnect) | Connect actual shapes at valid connection sites; BeginConnect/EndConnect behavior. |
| W10 | [Slides.AddSlide](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.slides.addslide) and [CustomLayout](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.customlayout) | Add slides using an existing native custom layout; inspect design/layout objects. |
| W11 | [Excel Workbooks.Open](https://learn.microsoft.com/en-us/office/vba/api/excel.workbooks.open) | Read-only and external-link update controls. |
| W12 | [Excel AutomationSecurity](https://learn.microsoft.com/en-us/office/vba/api/excel.application.automationsecurity) | Macro disabling has an Excel 4.0 macro exception; reject macro-bearing input rather than relying only on this flag. |
| W13 | [Excel Range.Value2](https://learn.microsoft.com/en-us/office/vba/api/excel.range.value2) | Cell values differ from formatted display text; date/currency values require explicit interpretation. |
| W14 | [Word Documents.Open](https://learn.microsoft.com/en-us/office/vba/api/word.documents.open), [Revisions](https://learn.microsoft.com/en-us/office/vba/api/word.document.revisions), [ExportAsFixedFormat](https://learn.microsoft.com/en-us/office/vba/api/word.document.exportasfixedformat) | Native document open, revision inventory and optional reference PDF export. |
| W15 | [PowerShell installation on Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/install-powershell-on-windows) | PowerShell 7 installs alongside Windows PowerShell 5.1; WinGet installation. |
| W16 | [powershell.exe command line](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe?view=powershell-5.1) | Explicit -STA, -NoProfile and -File worker invocation. |
| W17 | [WinGet install](https://learn.microsoft.com/en-us/windows/package-manager/winget/install) | Exact ID, source and version selection. |
| W18 | [Windows filenames and namespaces](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file) | Reserved names/characters, default case-insensitivity, path and reparse-point concerns. |

Office APIs are documented with VBA examples; the planned worker invokes the same automation object model through a bounded PowerShell/COM adapter. This register does not claim arbitrary sample code is already a tested Deckforge adapter. API availability, Office edition/build, installed fonts, locale and company policy must be recorded on the actual workstation.
