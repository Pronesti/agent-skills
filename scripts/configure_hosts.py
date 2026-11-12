#!/usr/bin/env python3
"""Install the approved personal policy, the local Codex marketplace entry, and the shared global instructions."""
import argparse
import datetime
import json
from pathlib import Path
import re
import shutil

from global_instructions import (END, START, codex_home_path, imports_shared, link_claude,
                                 sync_instructions)
from invocation_policy import host_policy_body

REPO = Path(__file__).resolve().parents[1]
MARKETPLACE_ENTRY = {
    "name": "caveman",
    "source": {"source": "local", "path": "./plugins/caveman"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Productivity",
}


def plan_marketplace(path):
    """Return the marketplace JSON text with the Caveman entry upserted, or raise before any change."""
    if path.exists():
        payload = json.loads(path.read_text())
    else:
        payload = {"name": "personal", "interface": {"displayName": "Personal"}, "plugins": []}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    if not isinstance(payload.get("interface", {}), dict):
        raise ValueError(f"{path} field 'interface' must be an object")
    plugins = payload.setdefault("plugins", [])
    if not isinstance(plugins, list):
        raise ValueError(f"{path} field 'plugins' must be an array")
    for index, entry in enumerate(plugins):
        if isinstance(entry, dict) and entry.get("name") == MARKETPLACE_ENTRY["name"]:
            plugins[index] = MARKETPLACE_ENTRY
            break
    else:
        plugins.append(MARKETPLACE_ENTRY)
    return json.dumps(payload, indent=2) + "\n"


def replace_policy_block(path, old, block):
    if START not in old:
        return old.rstrip() + "\n\n" + block + "\n"
    if old.count(START) != 1 or old.count(END) != 1 or old.index(END) < old.index(START):
        raise ValueError(f"{path}: expected one {START} followed by one {END}; left untouched")
    return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, old, flags=re.S)


def configure(home, codex_home, configured_codex_home, policy_only):
    backup = home / ".local/share/agent-skills/backups" / (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-host-policy")

    def save(path):
        if path.exists():
            dest = backup / path.relative_to(home)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)

    marketplace = home / ".agents/plugins/marketplace.json"
    source_link = home / "plugins/caveman"
    if not policy_only:
        # Validate everything before the first change, so a failure leaves no partial state.
        if (source_link.exists() or source_link.is_symlink()) and \
                source_link.resolve() != REPO / "plugins/caveman":
            raise RuntimeError(f"Unmanaged plugin source at {source_link}")
        marketplace_text = plan_marketplace(marketplace)
        if not source_link.is_symlink():
            source_link.parent.mkdir(parents=True, exist_ok=True)
            source_link.symlink_to(REPO / "plugins/caveman", target_is_directory=True)
        if not marketplace.exists() or marketplace.read_text() != marketplace_text:
            save(marketplace)
            marketplace.parent.mkdir(parents=True, exist_ok=True)
            marketplace.write_text(marketplace_text)

    # A missing global file gets the complete shared template, not a policy-only fragment.
    instructions = sync_instructions(home, codex_home, apply=True, replace_existing=False)
    claude_path = home / ".claude/CLAUDE.md"
    claude = link_claude(home, configured_codex_home, apply=True)
    block = START + "\n" + host_policy_body() + END
    for path in (codex_home / "AGENTS.md", claude_path):
        old = path.read_text() if path.exists() else ""
        if path == claude_path and imports_shared(old, codex_home, claude_path.parent):
            continue  # Claude already receives the policy block through the import.
        new = replace_policy_block(path, old, block)
        if new != old:
            save(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(new)

    return {"backup": str(backup) if backup.exists() else None, "policy_only": policy_only,
            "marketplace": str(marketplace), "plugin_source": str(source_link),
            "instructions": {key: instructions[key] for key in ('target', 'changed')},
            "claude": claude}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, help='Host root; explicit scratch roots also isolate Codex from CODEX_HOME')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--policy-only', action='store_true', help='Update managed instruction blocks without marketplace changes')
    mode.add_argument('--sync-agents', action='store_true', help='Preview the shared global instructions for Codex and the Claude import; skips marketplace setup')
    parser.add_argument('--apply', action='store_true', help='Apply --sync-agents with a backup; otherwise sync only previews')
    parser.add_argument('--codex-home', type=Path, help='Codex directory for --sync-agents; overrides --home and CODEX_HOME')
    args = parser.parse_args()
    if (args.apply or args.codex_home is not None) and not args.sync_agents:
        parser.error('--apply and --codex-home require --sync-agents')
    home = (args.home or Path.home()).expanduser().resolve()
    configured_codex_home = codex_home_path(args.home, args.codex_home)
    codex_home = configured_codex_home.resolve()
    try:
        if args.sync_agents:
            result = sync_instructions(home, codex_home, args.apply)
            result['claude'] = link_claude(home, configured_codex_home, args.apply)
        else:
            result = configure(home, codex_home, configured_codex_home, args.policy_only)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f'Host configuration: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
