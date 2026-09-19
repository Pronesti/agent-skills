#!/usr/bin/env python3
"""Install the approved personal policy and local Codex marketplace entry."""
import datetime
import json
from pathlib import Path
import re
import shutil
import sys

REPO = Path(__file__).resolve().parents[1]
HOME_DIR = Path.home()
backup = HOME_DIR / ".local/share/agent-skills/backups" / (datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-host-policy")


def save(path):
    if path.exists():
        dest = backup / path.relative_to(HOME_DIR)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


marketplace = HOME_DIR / ".agents/plugins/marketplace.json"
source_link = HOME_DIR / "plugins/caveman"
if source_link.exists() or source_link.is_symlink():
    if source_link.resolve() != REPO / "plugins/caveman":
        raise RuntimeError(f"Unmanaged plugin source at {source_link}")
else:
    source_link.parent.mkdir(parents=True, exist_ok=True)
    source_link.symlink_to(REPO / "plugins/caveman", target_is_directory=True)

save(marketplace)
sys.path.insert(0, str(HOME_DIR / ".codex/skills/.system/plugin-creator/scripts"))
from create_basic_plugin import update_marketplace_json
update_marketplace_json(marketplace, None, "caveman", "AVAILABLE", "ON_INSTALL", "Productivity", True)

start = "<!-- personal-skill-policy:start -->"
end = "<!-- personal-skill-policy:end -->"
body = """## Personal workflow skills

Use personal workflow skills only when I explicitly select them. Apply the workflow to the requested task; session-wide modes require an explicit request. Perform ordinary coding, debugging, planning, review, and writing using native capabilities.

Read a selected workflow's declared supporting references as needed. Treat other workflow names in skills, generated plans, and handoffs as optional suggestions for me, not automatic activation instructions. The grill-me alias includes grilling; grill-with-docs includes grilling and domain documentation.

Preserve project runtime, integration, verification, and delivery requirements. Application-required built-in skills still follow the host's instructions.
"""
for path in (HOME_DIR / ".codex/AGENTS.md", HOME_DIR / ".claude/CLAUDE.md"):
    old = path.read_text() if path.exists() else ""
    block = start + "\n" + body + end
    new = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, old, flags=re.S) if start in old else old.rstrip() + "\n\n" + block + "\n"
    if new != old:
        save(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new)

print(json.dumps({"backup": str(backup), "marketplace": str(marketplace), "plugin_source": str(source_link)}, indent=2))
