#!/usr/bin/env python3
"""Opt-in local Presenton experiment. No company data or provider keys are supplied.

Default is print-only. --start pulls the selected image, resolves its digest, and
starts a loopback-bound container with a dedicated Docker volume. Docker and the
image require independent review. This script was syntax-checked, not deployed.
"""
import argparse
import json
import shlex
import shutil
import subprocess
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--start', action='store_true', help='Actually pull and start; otherwise print a plan only')
p.add_argument('--image', default='ghcr.io/presenton/presenton:latest')
p.add_argument('--port', type=int, default=5001)
p.add_argument('--name', default='deckforge-presenton-lab')
a = p.parse_args()
if not 1024 <= a.port <= 65535:
    p.error('Use an unprivileged port between 1024 and 65535')
if not a.name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in a.name):
    p.error('Container name must contain only letters, numbers, underscores or hyphens')
volume = a.name + '-data'
def run_args(image):
    return ['docker', 'run', '-d', '--name', a.name, '-p', f'127.0.0.1:{a.port}:80',
            '-v', f'{volume}:/app_data', '-e', 'MEM0_ENABLED=false',
            '-e', 'DISABLE_IMAGE_GENERATION=true', '-e', 'WEB_GROUNDING=false', image]
if not a.start:
    print('PRINT ONLY — no pull, installation, container or model call was performed.')
    print(shlex.join(['docker', 'pull', a.image]))
    print('Resolve RepoDigest, then run:')
    print(shlex.join(run_args('ghcr.io/presenton/presenton@sha256:<resolved-digest>')))
    print('Add --start to execute. Configure authentication and a provider in the local UI.')
    raise SystemExit(0)
if not shutil.which('docker'):
    p.exit(1, 'Docker is not installed/on PATH. Install it independently; no system changes made.\n')
try:
    existing = subprocess.run(['docker', 'container', 'inspect', a.name], capture_output=True, timeout=30)
    if existing.returncode == 0:
        p.exit(1, f'Container {a.name} already exists; it will not be replaced.\n')
    subprocess.run(['docker', 'pull', a.image], check=True, timeout=900)
    info = json.loads(subprocess.check_output(['docker', 'image', 'inspect', a.image], text=True, timeout=30))[0]
    digests = info.get('RepoDigests') or []
    if not digests:
        p.exit(1, 'No repository digest found; refusing to run an unrecorded image.\n')
    digest = next((d for d in digests if d.startswith('ghcr.io/presenton/presenton@')), digests[0])
    command = run_args(digest)
    container_id = subprocess.check_output(command, text=True, timeout=60).strip()
    root = Path(__file__).resolve().parents[1] / 'out' / 'lab'
    root.mkdir(parents=True, exist_ok=True)
    record = {'requestedImage': a.image, 'resolvedImage': digest, 'imageId': info.get('Id'),
              'containerId': container_id, 'name': a.name, 'volume': volume,
              'address': f'http://127.0.0.1:{a.port}', 'providerConfigured': False,
              'status': 'started-not-health-verified'}
    (root / 'presenton-image.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))
except (subprocess.SubprocessError, json.JSONDecodeError, OSError) as exc:
    p.exit(1, f'Presenton experiment failed: {exc}. No existing container was replaced.\n')
