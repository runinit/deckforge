#!/usr/bin/env python3
"""Read-only local tool inventory. Does not install tools or call a model."""
import json
import shutil
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
checks = {}
for name, args in {
    'node': ['--version'], 'npm': ['--version'], 'python3': ['--version'],
    'git': ['--version'], 'soffice': ['--version'], 'pdftoppm': ['-v'],
    'docker': ['--version'],
}.items():
    executable = shutil.which(name)
    if not executable:
        checks[name] = {'status': 'MISSING', 'optional': name in ('soffice', 'pdftoppm', 'docker')}
        continue
    try:
        result = subprocess.run([executable, *args], capture_output=True, text=True, timeout=15)
        checks[name] = {'status': 'FOUND' if result.returncode == 0 else 'ERROR',
                        'version': (result.stdout + result.stderr).strip().splitlines()[0]}
    except (subprocess.SubprocessError, IndexError) as exc:
        checks[name] = {'status': 'ERROR', 'detail': str(exc)}
if shutil.which('fc-match'):
    result = subprocess.run(['fc-match', '-f', '%{family}\n', 'Liberation Sans'], capture_output=True, text=True, timeout=15)
    checks['demo-font'] = {'requested': 'Liberation Sans', 'resolved': result.stdout.strip(),
                           'status': 'MATCH' if 'Liberation Sans' in result.stdout else 'SUBSTITUTED'}
else:
    checks['demo-font'] = {'status': 'NOT_CHECKED', 'detail': 'fontconfig not available; confirm manually'}
checks['project'] = {'root': str(root), 'lockfile': (root/'package-lock.json').exists(),
                     'note': 'FOUND is inventory, not a compatibility or security certification.'}
print(json.dumps(checks, indent=2))
