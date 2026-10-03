#!/usr/bin/env python3
"""Validate selective invocation for both hosts and local supporting references."""
from pathlib import Path
import json
import re
import sys
import yaml

from invocation_policy import automatic_skills

ROOT = Path(__file__).resolve().parents[1]
errors = []
try:
    automatic_entries = automatic_skills()
except (ValueError, KeyError, OSError) as exc:
    print(f"invocation-policy.json: {exc}")
    sys.exit(1)
automatic_paths = {entry['local_path'] for entry in automatic_entries}
skills = list((ROOT / "skills").glob("*/SKILL.md")) + list((ROOT / "plugins/caveman/skills").glob("*/SKILL.md"))
lock = json.loads((ROOT / "upstreams.json").read_text())
locked_paths = [entry["local_path"] for entry in lock["skills"]]
actual_paths = {str(path.parent.relative_to(ROOT)) for path in skills}
if len(set(locked_paths)) != len(locked_paths) or set(locked_paths) != actual_paths:
    errors.append("upstreams.json: duplicate or missing skill provenance")
for entry in lock["skills"]:
    if entry["revision"] != lock["sources"][entry["source"]]["revision"]:
        errors.append(f"{entry['name']}: source revision differs from provenance lock")
for path in skills:
    text = path.read_text()
    try:
        data = yaml.safe_load(text.split("---", 2)[1])
        policy = yaml.safe_load((path.parent / "agents/openai.yaml").read_text())
        assert data["name"] == path.parent.name, "name differs from directory"
        assert isinstance(data["description"], str) and data["description"].strip(), "missing description"
        automatic = str(path.parent.relative_to(ROOT)) in automatic_paths
        assert data.get("disable-model-invocation") is (not automatic), "Claude/Cursor invocation differs from allowlist"
        assert policy.get("policy", {}).get("allow_implicit_invocation") is automatic, "Codex invocation differs from allowlist"
        if automatic:
            entry = next(e for e in automatic_entries if e['local_path'] == str(path.parent.relative_to(ROOT)))
            expected_name = ('caveman:' if 'plugins/caveman/' in entry['local_path'] else '') + data['name']
            assert entry['name'] == expected_name, "allowlist name differs from skill identity"
            assert 'Manual workflow:' not in data['description'], "automatic description still says manual"
            assert 'only when the user explicitly selects' not in text and 'Use only when explicitly selected' not in text, "automatic body still requires explicit selection"
    except (ValueError, KeyError, AssertionError, OSError, yaml.YAMLError) as exc:
        errors.append(f"{path}: {exc}")
    if re.search(r"^(<<<<<<<|=======|>>>>>>>)", text, re.M):
        errors.append(f"{path}: unresolved merge")
    if "REQUIRED SUB-SKILL:" in text or "ACTIVE EVERY RESPONSE" in text:
        errors.append(f"{path}: automatic workflow/persistence instruction")
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("http", "#", "mailto:", "/")) or any(x in target for x in ("<", ">", "$", " ")):
            continue
        if target.endswith(".md") and target.startswith(("../", "references/")):
            if not (path.parent / target).exists():
                errors.append(f"{path}: missing supporting reference {target}")
for manifest in (ROOT / "plugins/caveman/.codex-plugin/plugin.json", ROOT / "plugins/caveman/.claude-plugin/plugin.json"):
    data = json.loads(manifest.read_text())
    if data.get("name") != "caveman" or "hooks" in data:
        errors.append(f"{manifest}: wrong identity or automatic hooks")
if (ROOT / "plugins/caveman/hooks/hooks.json").exists():
    errors.append("Caveman hooks/hooks.json would register automatic hooks")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"Validated {len(skills)} skill manifests ({len(automatic_paths)} automatic, {len(skills) - len(automatic_paths)} manual), supporting links, and hook-free plugin manifests.")
