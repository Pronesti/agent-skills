#!/usr/bin/env python3
"""Install the approved personal policy and local Codex marketplace entry."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import sys

from invocation_policy import host_policy_body
from codex_instructions import sync_instructions

REPO = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--home', type=Path, help='Host root; explicit scratch roots also isolate Codex from CODEX_HOME')
mode = parser.add_mutually_exclusive_group()
mode.add_argument('--policy-only', action='store_true', help='Update managed instruction blocks without marketplace changes')
mode.add_argument('--sync-codex-agents', action='store_true', help='Preview the complete shared Codex AGENTS.md; skips Claude and marketplace setup')
parser.add_argument('--apply', action='store_true', help='Apply --sync-codex-agents with a backup; otherwise sync only previews')
parser.add_argument('--codex-home', type=Path, help='Codex directory for --sync-codex-agents; overrides --home and CODEX_HOME')
args = parser.parse_args()
if (args.apply or args.codex_home is not None) and not args.sync_codex_agents:
    parser.error('--apply and --codex-home require --sync-codex-agents')
HOME_DIR = (args.home or Path.home()).expanduser().resolve()
if args.sync_codex_agents:
    codex_home = args.codex_home
    if codex_home is None:
        codex_home = HOME_DIR / '.codex' if args.home is not None else Path(os.environ.get('CODEX_HOME') or HOME_DIR / '.codex')
    try:
        result = sync_instructions(HOME_DIR, codex_home.expanduser().resolve(), args.apply)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Codex instructions: {exc}\n')
    print(json.dumps(result, indent=2))
    sys.exit(0)
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
