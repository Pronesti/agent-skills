#!/usr/bin/env python3
"""Native pstack agents, model choices, scoped history and monitoring helpers."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import sys

from codex_instructions import resolve_codex_home
from codex_native import (CodexReadClient, ROOT, apply_agent_plan, atomic_write, config_path,
                          default_choices, model_catalog, native_agent_plan, resolve_efforts,
                          validate_choices)
from codex_history import list_history, project_paths, read_history
from codex_monitor import monitor_plan, monitor_record, run_monitor


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, help='Scratch/installation home; isolates CODEX_HOME when explicit')
    parser.add_argument('--codex-home', type=Path)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('models', help='Read the native available-model catalog')
    commands.add_parser('defaults', help='Print editable inheriting role choices')
    setup = commands.add_parser('configure', help='Validate role choices and preview native agent files')
    setup.add_argument('--choices', required=True, type=Path)
    setup.add_argument('--apply', action='store_true')
    agents = commands.add_parser('agents', help='Preview/sync native agents using saved choices')
    agents.add_argument('--apply', action='store_true')
    history = commands.add_parser('history', help='Read project-scoped persisted history through native APIs')
    history.add_argument('action', choices=('list', 'read'))
    history.add_argument('--project', type=Path, required=True)
    history.add_argument('--include-worktrees', action='store_true')
    history.add_argument('--thread')
    history.add_argument('--search')
    history.add_argument('--archived', action='store_true')
    history.add_argument('--exclude-thread')
    history.add_argument('--cursor')
    history.add_argument('--limit', type=int, default=3)
    for name in ('monitor-plan', 'monitor-record', 'monitor-run'):
        monitor = commands.add_parser(name)
        monitor.add_argument('--project', type=Path, required=True)
        monitor.add_argument('--pr', required=True)
        if name == 'monitor-plan':
            monitor.add_argument('--mode', choices=('check', 'drive', 'background', 'threads-only'), required=True)
        else:
            monitor.add_argument('--apply', action='store_true', help='Record the observation in local state')
        if name == 'monitor-record':
            monitor.add_argument('--snapshot', type=Path, required=True)
        if name == 'monitor-run':
            monitor.add_argument('--bun', default='bun')
    args = parser.parse_args(argv)
    home = (args.home or Path.home()).expanduser().resolve()
    codex_home = resolve_codex_home(args.home, args.codex_home)
    if args.command == 'models':
        with CodexReadClient() as client:
            return {'models': list(model_catalog(client).values())}
    if args.command == 'defaults':
        return default_choices()
    if args.command in ('configure', 'agents'):
        choices, catalog = None, None
        if args.command == 'configure':
            config = json.loads(args.choices.read_text())
            with CodexReadClient() as client:
                catalog = model_catalog(client)
            choices = resolve_efforts(validate_choices(config, catalog), catalog)
        plan = native_agent_plan(home, codex_home, choices, catalog)
        path = config_path(home)
        if choices is not None:
            if path.is_symlink() or (path.exists() and not path.is_file()):
                raise ValueError(f'Unsafe model configuration target: {path}')
            content = json.dumps(choices, indent=2) + '\n'
            if not path.exists() or path.read_text() != content:
                plan['operations'].append({'path': path, 'content': content})
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = home / '.local/share/agent-skills/backups' / (stamp + '-native-agents')
        result = apply_agent_plan(plan, home, backup, args.apply)
        result.update(applied=args.apply, model_config=str(path), choices=plan['choices'])
        return result
    if args.command == 'history':
        paths = project_paths(args.project, args.include_worktrees)
        with CodexReadClient() as client:
            if args.action == 'read':
                if not args.thread:
                    raise ValueError('history read requires --thread')
                return read_history(client, paths, args.thread, args.limit, args.cursor)
            return list_history(client, paths, args.limit, args.cursor, args.search,
                                args.archived, args.exclude_thread)
    if args.command == 'monitor-plan':
        return monitor_plan(args.pr, args.project, args.mode)
    state = home / '.local/state/agent-skills/monitors'
    if args.command == 'monitor-run':
        return run_monitor(args.pr, args.project, state, args.apply, args.bun)
    return monitor_record(args.pr, args.project, json.loads(args.snapshot.read_text()), state, args.apply)


if __name__ == '__main__':
    try:
        print(json.dumps(main(), indent=2))
    except (ValueError, KeyError, OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f'Pstack Codex: {exc}', file=sys.stderr)
        sys.exit(1)
