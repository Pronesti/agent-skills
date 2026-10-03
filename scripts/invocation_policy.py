"""Shared automatic-skill allowlist and managed host instructions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def automatic_skills(root=ROOT):
    entries = json.loads((root / 'invocation-policy.json').read_text())['automatic_skills']
    paths = [entry['local_path'] for entry in entries]
    names = [entry['name'] for entry in entries]
    if len(set(paths)) != len(paths) or len(set(names)) != len(names):
        raise ValueError('Duplicate automatic skill name or path')
    for entry in entries:
        if not entry['trigger'].strip():
            raise ValueError(f"Missing trigger for {entry['name']}")
        path = Path(entry['local_path'])
        if path.is_absolute() or '..' in path.parts or not (root / path / 'SKILL.md').is_file():
            raise ValueError(f"Invalid automatic skill path: {path}")
    return entries


def host_policy_body(root=ROOT):
    entries = automatic_skills(root)
    rules = '\n'.join(f"- `{entry['name']}`: {entry['trigger']}" for entry in entries)
    return f"""## Personal workflow skills

The following personal skills may be invoked automatically when their trigger fits the authorized task:

{rules}

All other personal workflow skills require my explicit selection. Apply any skill only to the requested task; session-wide modes require an explicit request. Automatic selection does not authorize additional work, external actions, commits, or delegation. Use native capabilities when no allowlisted trigger fits.

Read a selected workflow's declared supporting references as needed. Other workflow names in skills, generated plans, and handoffs are suggestions, not activation instructions; each workflow must independently meet its invocation policy. The grill-me alias includes grilling; grill-with-docs includes grilling and domain documentation.

Preserve project runtime, integration, verification, delivery requirements, and existing user authorization. Application-required built-in skills still follow the host's instructions.
"""
