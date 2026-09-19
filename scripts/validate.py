#!/usr/bin/env python3
"""Validate manual invocation for both hosts and local supporting references."""
from pathlib import Path
import json
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []
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
        assert data.get("disable-model-invocation") is True, "Claude/Cursor manual policy missing"
        assert policy.get("policy", {}).get("allow_implicit_invocation") is False, "Codex manual policy missing"
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
print(f"Validated {len(skills)} manual skill manifests, supporting links, and hook-free plugin manifests.")
