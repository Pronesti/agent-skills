#!/usr/bin/env python3
"""Update personal host policy, or sync the complete shared Codex instructions."""
import argparse
import datetime
import json
from pathlib import Path
import re
import shutil
import sys

from invocation_policy import host_policy_body
from codex_instructions import resolve_codex_home, sync_instructions

REPO = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--home', type=Path, help='Host root; explicit scratch roots also isolate Codex from CODEX_HOME')
mode = parser.add_mutually_exclusive_group()
mode.add_argument('--policy-only', action='store_true', help='Update managed instruction blocks without installing skills')
mode.add_argument('--sync-codex-agents', action='store_true', help='Preview the complete shared Codex AGENTS.md; skips Claude and marketplace setup')
parser.add_argument('--apply', action='store_true', help='Apply --sync-codex-agents with a backup; otherwise sync only previews')
parser.add_argument('--codex-home', type=Path, help='Codex directory for --sync-codex-agents; overrides --home and CODEX_HOME')
args = parser.parse_args()
if (args.apply or args.codex_home is not None) and not args.sync_codex_agents:
    parser.error('--apply and --codex-home require --sync-codex-agents')
HOME_DIR = (args.home or Path.home()).expanduser().resolve()
if args.sync_codex_agents:
    try:
        codex_home = resolve_codex_home(args.home, args.codex_home)
        result = sync_instructions(HOME_DIR, codex_home, args.apply)
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

print(json.dumps({"backup": str(backup) if backup.exists() else None,
                  "policy_only": True}, indent=2))
