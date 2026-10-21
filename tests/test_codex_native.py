import json
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from codex_native import (CodexReadClient, apply_agent_plan, config_path, default_choices,
                          load_choices, model_catalog, native_agent_plan, resolve_efforts, validate_choices)
from install import install

CATALOG = {name: {'model': name, 'supportedReasoningEfforts': [{'reasoningEffort': 'low'}, {'reasoningEffort': 'high'}],
                  'defaultReasoningEffort': 'low'} for name in ('test-code', 'test-review')}


class NativeAgentsTests(unittest.TestCase):
    def test_defaults_install_real_toml_and_repeat_without_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            preview = install(home, runtime='skip')
            self.assertFalse(any(home.iterdir()))
            self.assertEqual(preview['native_agents']['agents'], 23)
            result = install(home, True, runtime='skip')
            paths = list((home / '.codex/agents').glob('*.toml'))
            self.assertEqual(len(paths), 23)
            for path in paths:
                agent = tomllib.loads(path.read_text())
                self.assertEqual(path.stem, agent['name'])
                self.assertNotIn('model', agent)
                self.assertNotIn('{{PSTACK_ROOT}}', agent['developer_instructions'])
                self.assertIn(str(ROOT / 'pstack/docs/harness/codex.md'), agent['developer_instructions'])
            self.assertFalse(any(result['native_agents']['panels_use_distinct_models'].values()))
            self.assertEqual(install(home, True, runtime='skip')['actions'], [])

    def test_explicit_models_resolve_native_effort_and_panel_entries(self):
        choices = {'schema_version': 1, 'roles': {
            'feature, refactoring': [{'model': 'test-code'}],
            'interrogate reviewers': [{'model': 'test-code', 'effort': 'high'}, {'model': 'test-review'}]}}
        choices = resolve_efforts(validate_choices(choices, CATALOG), CATALOG)
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            plan = native_agent_plan(home, home / '.codex', choices, CATALOG)
            self.assertTrue(plan['panels']['interrogate reviewers'])
            apply_agent_plan(plan, home, home / 'backups', True)
            code = tomllib.loads((home / '.codex/agents/pstack-code.toml').read_text())
            reviewer = tomllib.loads((home / '.codex/agents/pstack-reviewer-1.toml').read_text())
            self.assertEqual((code['model'], code['model_reasoning_effort']), ('test-code', 'low'))
            self.assertEqual(reviewer['model_reasoning_effort'], 'high')

    def test_invalid_models_and_efforts_are_rejected_before_installation(self):
        for entry in ({'model': 'cursor-grok'}, {'model': 'test-code', 'effort': 'ultra'},
                      {'model': 'inherit-parent', 'effort': 'high'}, {'model': 'test-code', 'effort': []}):
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                validate_choices({'schema_version': 1, 'roles': {'bug-fix': [entry]}}, CATALOG)
        for config in ([], {}, {'schema_version': 1, 'roles': {'unknown': []}}):
            with self.subTest(config=config), self.assertRaises(ValueError):
                validate_choices(config, CATALOG)

    def test_modified_agents_stop_install_before_skills_or_shared_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            path = home / '.codex/agents/pstack-code.toml'
            path.parent.mkdir(parents=True)
            path.write_text('my personal agent')
            with self.assertRaisesRegex(ValueError, 'unmanaged native agent'):
                install(home, True, runtime='skip')
            self.assertFalse((home / '.agents').exists())
            self.assertFalse((home / '.codex/AGENTS.md').exists())
            self.assertEqual(path.read_text(), 'my personal agent')
            path.unlink()
            install(home, True, runtime='skip')
            path.write_text('my edits to the generated agent')
            with self.assertRaisesRegex(ValueError, 'Locally modified'):
                install(home, True, runtime='skip')
            self.assertEqual(path.read_text(), 'my edits to the generated agent')

    def test_panel_reduction_retires_only_unchanged_managed_agent_with_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            plan = native_agent_plan(home, home / '.codex')
            apply_agent_plan(plan, home, home / 'old-backup', True)
            extra = home / '.codex/agents/custom.toml'
            extra.write_text('unrelated')
            removed = home / '.codex/agents/pstack-reviewer-2.toml'
            original = removed.read_bytes()
            choices = default_choices()
            choices['roles']['interrogate reviewers'] = [{'model': 'inherit-parent'}]
            plan = native_agent_plan(home, home / '.codex', choices)
            self.assertTrue(removed.exists())
            apply_agent_plan(plan, home, home / 'new-backup', True)
            self.assertFalse(removed.exists())
            self.assertEqual((home / 'new-backup/.codex/agents/pstack-reviewer-2.toml').read_bytes(), original)
            self.assertEqual(extra.read_text(), 'unrelated')

    def test_saved_and_legacy_choices_are_never_silently_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            path = config_path(home)
            path.parent.mkdir(parents=True)
            legacy = path.with_suffix('.md')
            legacy.write_text('how explorer: my-model high')
            with self.assertRaisesRegex(ValueError, 'migrate'):
                load_choices(home, CATALOG)
            path.write_text(json.dumps({'schema_version': 1, 'roles': {'how explorer': [{'model': 'test-code'}]}}))
            self.assertEqual(load_choices(home, CATALOG)['roles']['how explorer'][0]['effort'], 'low')
            self.assertTrue(legacy.exists())

    def test_read_client_forbids_inference_and_paginates_catalog(self):
        with self.assertRaises(ValueError):
            CodexReadClient().call('turn/start', {})
        pages = [{'data': [CATALOG['test-code']], 'nextCursor': 'next'},
                 {'data': [CATALOG['test-review']], 'nextCursor': None}]
        class Client:
            def call(self, method, params):
                return pages.pop(0)
        self.assertEqual(set(model_catalog(Client())), set(CATALOG))

class NativeProtocolTests(unittest.TestCase):
    def test_jsonrpc_handshake_denies_server_requests_and_handles_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / 'fake-codex'
            executable.write_text('''#!/usr/bin/env python3
import json, sys
for line in sys.stdin:
    request = json.loads(line)
    method = request.get('method')
    if method == 'initialize':
        print(json.dumps({'id': request['id'], 'result': {}}), flush=True)
    elif method == 'model/list':
        print(json.dumps({'method': 'notice', 'params': {}}), flush=True)
        print(json.dumps({'id': 900, 'method': 'execute/write', 'params': {}}), flush=True)
        denial = json.loads(sys.stdin.readline())
        if denial.get('error', {}).get('code') != -32601:
            raise SystemExit(9)
        print(json.dumps({'id': request['id'], 'result': {'data': [], 'nextCursor': None}}), flush=True)
    elif method == 'thread/read':
        print(json.dumps({'id': request['id'], 'error': {'message': 'not found'}}), flush=True)
''')
            executable.chmod(0o755)
            with CodexReadClient(str(executable), timeout=2) as client:
                self.assertEqual(model_catalog(client), {})
                with self.assertRaisesRegex(RuntimeError, 'not found'):
                    client.call('thread/read', {'threadId': 'missing'})
            self.assertIsNotNone(client.process.poll())
