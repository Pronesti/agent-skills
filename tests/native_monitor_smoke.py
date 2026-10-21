#!/usr/bin/env python3
"""Opt-in real upstream watcher test with a local forge fixture, no live PR calls."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from codex_monitor import run_monitor


def main(bun):
    with tempfile.TemporaryDirectory(prefix='pstack-monitor-smoke-') as temporary:
        temp = Path(temporary)
        project, package = temp / 'project', temp / 'package'
        project.mkdir()
        scripts = package / 'pstack/skills/poteto-mode/scripts'
        shutil.copytree(ROOT / 'pstack/skills/poteto-mode/scripts', scripts,
                        ignore=shutil.ignore_patterns('node_modules'))
        subprocess.run(['git', 'init', '-q', str(project)], check=True)
        subprocess.run(['git', '-C', str(project), 'remote', 'add', 'origin',
                        'https://github.com/example/project.git'], check=True)
        commands = temp / 'bin'
        commands.mkdir()
        gh = commands / 'gh'
        gh.write_text('''#!/usr/bin/env python3
import json, sys
if sys.argv[1:3] != ['pr', 'view']:
    raise SystemExit(9)
print(json.dumps({'mergeable': 'MERGEABLE', 'mergeStateStatus': 'CLEAN',
'reviewDecision': 'APPROVED', 'headRefOid': 'abc', 'headRefName': 'feature',
'baseRefName': 'main', 'state': 'MERGED', 'mergedAt': '2026-10-21T12:00:00Z', 'isDraft': False}))
''')
        gh.chmod(0o755)
        previous_path = os.environ['PATH']
        try:
            os.environ['PATH'] = str(commands) + os.pathsep + previous_path
            first = run_monitor('https://github.com/example/project/pull/7', project,
                                temp / 'state', True, bun, package)
            repeated = run_monitor('https://github.com/example/project/pull/7', project,
                                   temp / 'state', True, bun, package)
        finally:
            os.environ['PATH'] = previous_path
        assert first['notify'] and first['stop']
        assert repeated['stop'] and not repeated['notify']
        return {'status': 'passed', 'watcher_verdict': first['snapshot']['kind'],
                'first_notification': True, 'duplicate_notification': False,
                'stop_requested': True, 'live_forge_calls': 0, 'persistent_automations_created': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bun', default=shutil.which('bun'))
    args = parser.parse_args()
    if not args.bun:
        parser.error('Bun is required; pass --bun /path/to/bun')
    print(json.dumps(main(args.bun), indent=2))
