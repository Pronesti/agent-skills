#!/usr/bin/env python3
"""Opt-in authenticated native-agent/model/history smoke test in disposable profiles."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import queue

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from codex_native import CodexReadClient, model_catalog
from codex_history import list_history, read_history


def main():
    auth = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')) / 'auth.json'
    if not auth.is_file():
        raise RuntimeError('Smoke test requires an authenticated CLI auth.json; no credentials are requested or printed')
    with tempfile.TemporaryDirectory(prefix='pstack-native-smoke-') as scratch:
        home = (Path(scratch) / 'home').resolve()
        project = (Path(scratch) / 'fixture').resolve()
        project.mkdir()
        (home / '.codex').mkdir(parents=True)
        shutil.copy2(auth, home / '.codex/auth.json')
        # Do not inherit the desktop's task/tool bridge into a standalone CLI test.
        env = {key: value for key, value in os.environ.items() if not key.startswith('CODEX_')}
        env.update(HOME=str(home), CODEX_HOME=str(home / '.codex'))
        source = 'def total(values):\n    # Add all the values.\n    return sum(values)\n'
        (project / 'totals.py').write_text(source)
        with CodexReadClient(env=env) as client:
            catalog = model_catalog(client)
        parent = next((m for m in catalog.values() if m.get('isDefault')), next(iter(catalog.values())))
        worker = next((m for m in catalog.values() if 'luna' in m['model']), parent)
        effort = worker['defaultReasoningEffort']
        choices = Path(scratch) / 'choices.json'
        choices.write_text(json.dumps({'schema_version': 1, 'roles': {
            'how explorer': [{'model': worker['model'], 'effort': effort}]}}))
        for command in (
            [sys.executable, str(ROOT / 'scripts/pstack_codex.py'), '--home', str(home),
             'configure', '--choices', str(choices), '--apply'],
            [sys.executable, str(ROOT / 'scripts/install.py'), '--home', str(home), '--apply', '--runtime', 'skip']):
            subprocess.run(command, env=env, text=True, capture_output=True, check=True, timeout=30)
        prompt = '''This is an authorized isolated verification fixture for the agent-skills repository.
Do not edit files. Invoke native custom agent pstack-how-explorer to explain how totals.py
computes its result, and pstack-comment-sicko to review comments in that file. Use their
configured agent types and model settings, send read-only scoped briefs and the fixture
path, wait for both results, and report actual findings with file/line citations. Each
delegate performs only its assigned role without further delegation. Do not simulate
agent invocations. If a type is unavailable report the exact error. Create no goals or
automations and send no messages to people.'''
        # Keep one app-server connection so live native child metadata is visible.
        with CodexReadClient(env=env) as client:
            started = client._request('thread/start', {'cwd': str(project), 'model': parent['model'],
                                      'approvalPolicy': 'never', 'sandbox': 'read-only'})
            thread_id = started['thread']['id']
            client._request('turn/start', {'threadId': thread_id,
                            'input': [{'type': 'text', 'text': prompt + '\nLeave both completed agents open for runtime verification.'}]})
            events = []
            deadline = time.monotonic() + 240
            while True:
                try:
                    event = client.messages.get(timeout=max(0, deadline - time.monotonic()))
                except queue.Empty as exc:
                    raise RuntimeError('Native workflow did not complete within its test budget') from exc
                if event is None:
                    raise RuntimeError('Native workflow disconnected')
                events.append(event)
                if 'id' in event and 'method' in event:
                    client._send({'id': event['id'], 'error': {'code': -32601, 'message': 'Read-only test; no approval granted'}})
                if event.get('method') == 'turn/completed' and event['params'].get('threadId') == thread_id:
                    if event['params']['turn']['status'] != 'completed':
                        raise RuntimeError('Native workflow failed')
                    break
            loaded = client._request('thread/loaded/list', {})['data']
            records = [client.call('thread/read', {'threadId': identifier, 'includeTurns': False})['thread']
                       for identifier in loaded]
            agents = {t.get('agentRole'): t for t in records if t.get('agentRole')}
            expected = {'pstack-how-explorer', 'pstack-comment-sicko'}
            if not expected <= set(agents):
                (Path(tempfile.gettempdir()) / 'pstack-native-smoke-debug.json').write_text(
                    json.dumps({'events': events, 'threads': records}, indent=2))
                raise RuntimeError(f'Native runtime did not confirm both agent roles: {sorted(agents)}')
            explorer = agents['pstack-how-explorer']
            if (explorer.get('model'), explorer.get('reasoningEffort')) != (worker['model'], effort):
                raise RuntimeError('The native agent did not use its configured model and reasoning effort')
            selected = read_history(client, [str(project)], thread_id, limit=1)
            if not selected['all_returned_turns_full']:
                raise RuntimeError('Native persisted history did not include full items')
            for role in expected:
                if str(Path(agents[role]['cwd']).resolve()) != str(project):
                    raise RuntimeError('A native agent left the fixture project')
                evidence = read_history(client, [str(project)], agents[role]['id'], limit=3)
                messages = ' '.join(str(item.get('text', '')) for turn in evidence['turns']
                                    for item in turn['items'] if item.get('type') == 'agentMessage')
                if 'totals.py' not in messages:
                    raise RuntimeError(f'{role}: no actual fixture citation in native output')
                if role == 'pstack-how-explorer' and 'sum' not in messages:
                    raise RuntimeError('Explorer did not explain the fixture calculation')
                if role == 'pstack-comment-sicko' and not any(word in messages.lower() for word in ('redund', 'delet', 'remov', 'kill')):
                    raise RuntimeError('Comment reviewer did not identify the redundant fixture comment')
        if (project / 'totals.py').read_text() != source or list(project.iterdir()) != [project / 'totals.py']:
            raise RuntimeError('The read-only fixture changed')
        return {'status': 'passed', 'agents_verified_in_native_history': sorted(expected),
                'explicit_model': explorer['model'], 'explicit_effort': explorer['reasoningEffort'],
                'native_history_full_items': selected['all_returned_turns_full'],
                'fixture_unchanged': True, 'profile': 'disposable; removed after verification'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
