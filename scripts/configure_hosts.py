#!/usr/bin/env python3
"""Install the approved personal policy and local Codex marketplace entry."""
import argparse
import datetime
import json
from pathlib import Path
import re
import shutil
import sys

from invocation_policy import host_policy_body

REPO = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--home', type=Path, default=Path.home(), help='Host root; use a scratch root for tests')
parser.add_argument('--policy-only', action='store_true', help='Update managed instruction blocks without marketplace changes')
args = parser.parse_args()
HOME_DIR = args.home.resolve()
backup = HOME_DIR / ".local/share/agent-skills/backups" / (datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-host-policy")


def save(path):
    if path.exists():
        dest = backup / path.relative_to(HOME_DIR)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


marketplace = HOME_DIR / ".agents/plugins/marketplace.json"
source_link = HOME_DIR / "plugins/caveman"
if not args.policy_only:
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
body = host_policy_body()
for path in (HOME_DIR / ".codex/AGENTS.md", HOME_DIR / ".claude/CLAUDE.md"):
    old = path.read_text() if path.exists() else ""
    block = start + "\n" + body + end
    new = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, old, flags=re.S) if start in old else old.rstrip() + "\n\n" + block + "\n"
    if new != old:
        save(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new)

print(json.dumps({"backup": str(backup) if backup.exists() else None, "policy_only": args.policy_only, "marketplace": str(marketplace), "plugin_source": str(source_link)}, indent=2))
