#!/usr/bin/env python3
"""Validate personal entrypoints, provenance, and the complete pinned pstack snapshot."""
import hashlib
import json
from pathlib import Path
import re
import sys
import tomllib
import yaml

from invocation_policy import automatic_skills
from codex_instructions import render_instructions
from codex_native import default_choices, render_agents, role_definitions

ROOT = Path(__file__).resolve().parents[1]
errors = []
try:
    render_instructions()
    automatic_entries = automatic_skills()
    for name, content in render_agents(default_choices()).items():
        data = tomllib.loads(content)
        assert data['name'] == Path(name).stem
        assert data['description'] and data['developer_instructions']
        assert '{{PSTACK_ROOT}}' not in content
    for role in role_definitions().values():
        assert (ROOT / 'pstack/skills' / role['workflow'] / 'SKILL.md').is_file()
except (ValueError, KeyError, OSError, AssertionError) as exc:
    sys.exit(str(exc))
automatic_paths = {entry['local_path'] for entry in automatic_entries}
skills = sorted((ROOT / 'skills').glob('*/SKILL.md'))
lock = json.loads((ROOT / 'upstreams.json').read_text())
locked_paths = [entry['local_path'] for entry in lock['skills']]
actual_paths = {str(path.parent.relative_to(ROOT)) for path in skills}
if len(set(locked_paths)) != len(locked_paths) or set(locked_paths) != actual_paths:
    errors.append('upstreams.json: duplicate or missing skill provenance')
upstream_skills = {path.parent.name for path in (ROOT / 'pstack/skills').glob('*/SKILL.md')}
if {path.parent.name for path in skills} != upstream_skills:
    errors.append('Personal entrypoints differ from the complete upstream public skill set')
if set(lock['sources']) != {'pstack'} or any(e['source'] != 'pstack' for e in lock['skills']):
    errors.append('The personal catalog must contain only pstack')
for entry in lock['skills']:
    if entry['revision'] != lock['sources'][entry['source']]['revision']:
        errors.append(f"{entry['name']}: source revision differs from provenance lock")
    upstream = ROOT / entry['path'] / 'SKILL.md'
    if not upstream.is_file() or upstream.parent.name != entry['name']:
        errors.append(f"{entry['name']}: invalid upstream workflow")
    local = ROOT / entry['local_path'] / 'SKILL.md'
    if local.is_file():
        link = f"../../{entry['path']}/SKILL.md"
        if f']({link})' not in local.read_text():
            errors.append(f"{entry['name']}: entrypoint does not load its upstream workflow")

for name, checksum in lock['upstream_files'].items():
    path = ROOT / name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != checksum:
        errors.append(f'{name}: pinned upstream file is missing or changed')
expected = set(lock['upstream_files']) | {'pstack/docs/harness/codex.md'}
actual = {str(p.relative_to(ROOT)) for p in (ROOT / 'pstack').rglob('*')
          if p.is_file() and '__pycache__' not in p.parts and 'node_modules' not in p.parts}
if actual != expected:
    errors.append(f'Unexpected or missing pstack files: {sorted(actual ^ expected)}')
for path in skills:
    content = path.read_text()
    try:
        data = yaml.safe_load(content.split('---', 2)[1])
        policy = yaml.safe_load((path.parent / 'agents/openai.yaml').read_text())
        assert data['name'] == path.parent.name, 'name differs from directory'
        assert isinstance(data['description'], str) and data['description'].strip(), 'missing description'
        automatic = str(path.parent.relative_to(ROOT)) in automatic_paths
        assert data.get('disable-model-invocation') is (not automatic), 'invocation differs from allowlist'
        assert policy.get('policy', {}).get('allow_implicit_invocation') is automatic, 'Codex invocation differs from allowlist'
        assert '../../pstack/docs/harness/codex.md' in content, 'Codex adapter is unreachable'
    except (ValueError, KeyError, AssertionError, OSError, yaml.YAMLError) as exc:
        errors.append(f'{path}: {exc}')
    if re.search(r'^(<<<<<<<|=======|>>>>>>>)', content, re.M):
        errors.append(f'{path}: unresolved merge')
    for target in re.findall(r'\]\(([^)]+)\)', content):
        if target.startswith(('../', 'references/')) and not (path.parent / target).exists():
            errors.append(f'{path}: missing supporting reference {target}')
for path in [ROOT / 'pstack/docs/harness/codex.md', *(ROOT / 'docs/codex').glob('*.md')]:
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if target.startswith(('../', './')) and not (path.parent / target).exists():
            errors.append(f'{path}: missing native integration reference {target}')
if errors:
    sys.exit('\n'.join(errors))
print(f'Validated {len(skills)} pstack entrypoints, {len(lock["upstream_files"])} unchanged upstream files, native agent TOML/roles, supporting links, provenance and invocation policy.')
