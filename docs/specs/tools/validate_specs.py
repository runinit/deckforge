#!/usr/bin/env python3
"""Validate this documentation pack. Does not run Deckforge application tests."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

REQUIRED_SECTIONS = [
    '## 1. Scope and non-goals',
    '## 2. File ownership and integration boundary',
    '## 3. Inputs, outputs and interface',
    '## 4. Requirements',
    '## 5. Implementation tasks',
    '## 6. Failure behavior',
    '## 7. Acceptance tests',
    '## 8. Verification commands and evidence',
    '## 9. Definition of done and handoff',
    '## 10. Source and decision traceability',
]
EXPECTED_PRS = {f'PR-{i:02d}' for i in range(9)} | {'PR-X1', 'PR-X2', 'PR-X3'}


def validate(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    try:
        manifest = json.loads((root / 'spec-manifest.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return {'status': 'FAIL', 'errors': [f'Manifest unreadable: {exc}']}
    specs = manifest.get('specs', [])
    ids = [s.get('id') for s in specs]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate spec IDs.')
    if len(specs) != 31:
        errors.append(f'Expected 31 specs; found {len(specs)}.')
    by_id = {s['id']: s for s in specs}
    paths: set[str] = set()
    all_ids: set[str] = set()
    for spec in specs:
        sid = spec['id']
        rel = spec.get('path', '')
        path = (root / rel).resolve()
        if not path.is_relative_to(root):
            errors.append(f'{sid}: path escapes spec root.')
            continue
        if rel in paths:
            errors.append(f'{sid}: duplicate spec file path.')
        paths.add(rel)
        if not path.is_file():
            errors.append(f'{sid}: missing file {rel}.')
            continue
        text = path.read_text(encoding='utf-8')
        if f'spec_id: {sid}\n' not in text:
            errors.append(f'{sid}: frontmatter identity mismatch.')
        if 'implementation_status: not_implemented_by_this_delivery' not in text:
            errors.append(f'{sid}: missing documentation-only implementation status.')
        for heading in REQUIRED_SECTIONS:
            if heading not in text:
                errors.append(f'{sid}: missing required section {heading}.')
        for dep in spec.get('dependsOn', []):
            if dep not in by_id:
                errors.append(f'{sid}: unknown dependency {dep}.')
            if dep == sid:
                errors.append(f'{sid}: self-dependency.')
        for key in ('requirementIds', 'taskIds', 'acceptanceIds'):
            values = spec.get(key, [])
            if not values:
                errors.append(f'{sid}: empty {key}.')
            for value in values:
                if value in all_ids:
                    errors.append(f'Duplicate requirement/task/test ID: {value}.')
                all_ids.add(value)
                if value not in text:
                    errors.append(f'{sid}: missing declared ID {value}.')

    state: dict[str, int] = {}
    order: list[str] = []
    def visit(sid: str, stack: list[str]) -> None:
        if state.get(sid) == 1:
            errors.append('Dependency cycle: ' + ' -> '.join(stack + [sid]))
            return
        if state.get(sid) == 2:
            return
        state[sid] = 1
        for dep in by_id[sid].get('dependsOn', []):
            if dep in by_id:
                visit(dep, stack + [sid])
        state[sid] = 2
        order.append(sid)
    for sid in by_id:
        visit(sid, [])

    prs = {pr for s in specs for pr in s.get('sourcePrs', [])}
    if prs != EXPECTED_PRS:
        errors.append(f'Original PR coverage mismatch: missing={sorted(EXPECTED_PRS-prs)}, extra={sorted(prs-EXPECTED_PRS)}.')

    local_links = 0
    md_files = sorted(root.rglob('*.md'))
    for path in md_files:
        text = path.read_text(encoding='utf-8')
        active_fence: str | None = None
        outside: list[str] = []
        for line in text.splitlines():
            fence = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
            if fence:
                marker = fence.group(1)
                if active_fence is None:
                    active_fence = marker
                elif marker[0] == active_fence[0] and len(marker) >= len(active_fence):
                    active_fence = None
                continue
            if active_fence is None:
                outside.append(line)
        if active_fence:
            errors.append(f'{path.relative_to(root)}: unclosed code fence.')
        for target in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)\)', '\n'.join(outside)):
            parsed = urlparse(target)
            if parsed.scheme or target.startswith('//'):
                continue
            # Fragment-only links are not checked for generated GitHub anchor semantics.
            target_path = unquote(parsed.path)
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            local_links += 1
            if not resolved.is_relative_to(root):
                errors.append(f'{path.relative_to(root)}: local link escapes bundle: {target}.')
            elif not resolved.exists():
                errors.append(f'{path.relative_to(root)}: broken local file link: {target}.')
    snapshots = 0
    for filename in ('ARCHITECTURE.md', 'DEVELOPMENT_PLAN.md'):
        path = root / 'references' / filename
        expected = manifest.get('sourceDigests', {}).get(filename)
        if not path.is_file():
            errors.append(f'Missing original source snapshot: {filename}.')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f'Original source snapshot hash mismatch: {filename}.')
        else:
            snapshots += 1
    return {
        'status': 'PASS' if not errors else 'FAIL',
        'scope': 'Documentation integrity only; no product or Office checks.',
        'specCount': len(specs),
        'markdownFileCount': len(md_files),
        'requirements': sum(len(s.get('requirementIds', [])) for s in specs),
        'tasks': sum(len(s.get('taskIds', [])) for s in specs),
        'acceptanceScenarios': sum(len(s.get('acceptanceIds', [])) for s in specs),
        'localFileLinksChecked': local_links,
        'sourceSnapshotsVerified': snapshots,
        'originalPrsCovered': sorted(prs),
        'topologicalOrder': order,
        'warnings': warnings,
        'errors': errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Emit the complete validation report as JSON.')
    args = parser.parse_args()
    result = validate(Path(__file__).resolve().parents[1])
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['status']}: documentation integrity")
        for field in ('specCount', 'requirements', 'tasks', 'acceptanceScenarios', 'localFileLinksChecked', 'sourceSnapshotsVerified'):
            if field in result:
                print(f'{field}: {result[field]}')
        for error in result.get('errors', []):
            print(f'ERROR: {error}', file=sys.stderr)
        print('Application implementation/tests and PowerPoint validation were not run by this command.')
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
