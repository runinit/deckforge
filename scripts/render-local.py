#!/usr/bin/env python3
"""Local LibreOffice preview for a trusted generated fixture. NOT Office certification."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('pptx', type=Path)
a = p.parse_args()
src = a.pptx.resolve()
for exe in ['soffice', 'pdftoppm']:
    if not shutil.which(exe):
        p.exit(1, f'Missing {exe}; see DEVELOPMENT_PLAN.md\n')
if not src.is_file():
    p.exit(1, f'Missing {src}\n')
out = src.parent / 'preview'
try:
    # Fresh conversion output avoids falsely accepting a stale PDF from an earlier run.
    with tempfile.TemporaryDirectory(prefix='deckforge-render-') as d:
        temp = Path(d)
        profile = temp / 'profile'
        converted = temp / 'converted'
        converted.mkdir()
        subprocess.run(['soffice', f'-env:UserInstallation={profile.as_uri()}', '--headless',
                        '--convert-to', 'pdf', '--outdir', str(converted), str(src)],
                       check=True, timeout=120)
        pdf = converted / (src.stem + '.pdf')
        if not pdf.is_file() or not pdf.stat().st_size:
            p.exit(1, 'LibreOffice returned without creating a fresh PDF\n')
        subprocess.run(['pdftoppm', '-scale-to', '1600', '-png', str(pdf), str(converted/'slide')],
                       check=True, timeout=120)
        pages = sorted(converted.glob('slide-*.png'))
        if not pages:
            p.exit(1, 'No preview pages were produced\n')
        out.mkdir(exist_ok=True)
        # These names are generated artifacts, not user input files.
        for old in out.glob('slide-*.png'):
            old.unlink()
        shutil.copy2(pdf, out/pdf.name)
        for page in pages:
            shutil.copy2(page, out/page.name)
        (out/'render.json').write_text(json.dumps({
            'renderer': 'LibreOffice + pdftoppm', 'pages': len(pages),
            'inputSha256': hashlib.sha256(src.read_bytes()).hexdigest(),
            'status': 'rendered-not-office-approved',
        }, indent=2) + '\n')
except (subprocess.SubprocessError, OSError) as exc:
    p.exit(1, f'Preview failed: {exc}\n')
print(out)
