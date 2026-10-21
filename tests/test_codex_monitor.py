import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from codex_monitor import monitor_plan, monitor_record, run_monitor

TARGET = 'https://github.com/example/project/pull/7'
CONTEXT = {'owner': 'example', 'repo': 'project', 'number': 7}


def snapshot(kind='WAITING', **fields):
    terminal = kind in ('READY', 'COMPLETE', 'BLOCKER', 'TIMEOUT', 'STATUS')
    data = {'schemaVersion': 1, 'mode': 'single', 'kind': kind, 'terminal': terminal,
            'sequence': 1, 'observedAt': 'now'}
    if terminal:
        data['exitCode'] = 0 if kind in ('READY', 'COMPLETE', 'STATUS') else 5 if kind == 'TIMEOUT' else 2
    if kind == 'WAITING':
        data.update(frontier=CONTEXT, reason={'kind': 'pending-checks', 'pending': [{'name': 'test'}]})
    elif kind == 'READY':
        data['scope'] = {'kind': 'single', 'pr': {'kind': 'ready-pr', 'context': CONTEXT}}
    elif kind == 'BLOCKER':
        data['blocker'] = {'kind': 'merge-conflicts', 'pr': CONTEXT}
    data.update(fields)
    return data


class NativeMonitoringTests(unittest.TestCase):
    def test_plan_is_targeted_bounded_and_does_not_schedule_anything(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            subprocess.run(['git', 'init', '-q', str(project)], check=True)
            subprocess.run(['git', '-C', str(project), 'remote', 'add', 'origin', 'git@github.com:example/project.git'], check=True)
            plan = monitor_plan(TARGET, project, 'background')
            self.assertEqual(plan['native_execution'], 'heartbeat')
            self.assertEqual(plan['command'][-2:], ['--timeout', '45'])
            self.assertIn('stay quiet', plan['prompt'])
            self.assertIn('Do not merge', plan['prompt'])
            check = monitor_plan(TARGET, project, 'check')
            self.assertIn('--status-only', check['command'])
            self.assertIsNone(monitor_plan(TARGET, project, 'threads-only')['command'])
            with self.assertRaisesRegex(ValueError, 'project origin'):
                monitor_plan('https://github.com/another/repo/pull/9', project, 'drive')
            with self.assertRaises(ValueError):
                monitor_plan(TARGET + '?command=bad', project, 'background')

    def test_pending_is_quiet_and_timestamp_churn_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            project, state = Path(temp), Path(temp) / 'state'
            preview = monitor_record(TARGET, project, snapshot(), state)
            self.assertFalse(state.exists())
            self.assertFalse(preview['notify'])
            monitor_record(TARGET, project, snapshot(), state, True)
            result = monitor_record(TARGET, project, snapshot(sequence=9, observedAt='later'), state, True)
            self.assertFalse(result['notify'])
            self.assertFalse(result['stop'])
            self.assertEqual(os.stat(result['state_path']).st_mode & 0o777, 0o600)
            self.assertFalse(monitor_record('https://github.com/Example/Project/pull/7', project, snapshot(), state)['notify'])
            progress = snapshot(reason={'kind': 'pending-checks', 'pending': [{'name': 'test', 'description': 'running for another minute'}]})
            self.assertFalse(monitor_record(TARGET, project, progress, state, True)['notify'])

    def test_blocker_and_terminal_notify_once_without_merging(self):
        with tempfile.TemporaryDirectory() as temp:
            project, state = Path(temp), Path(temp) / 'state'
            monitor_record(TARGET, project, snapshot(), state, True)
            self.assertTrue(monitor_record(TARGET, project, snapshot('BLOCKER'), state, True)['notify'])
            self.assertFalse(monitor_record(TARGET, project, snapshot('BLOCKER'), state, True)['notify'])
            ready = monitor_record(TARGET, project, snapshot('READY'), state, True)
            self.assertTrue(ready['notify'])
            self.assertTrue(ready['stop'])
            self.assertFalse(monitor_record(TARGET, project, snapshot('READY'), state, True)['notify'])

    def test_pending_timeout_is_not_a_failure_or_a_semantic_change(self):
        with tempfile.TemporaryDirectory() as temp:
            project, state = Path(temp), Path(temp) / 'state'
            monitor_record(TARGET, project, snapshot(), state, True)
            timed = snapshot('TIMEOUT', reason={'kind': 'pending-checks', 'pending': [{'name': 'test'}]})
            with self.assertRaisesRegex(ValueError, 'verifiable PR context'):
                monitor_record(TARGET, project, timed, state)
            result = monitor_record(TARGET, project, timed, state, True, verified_command=True)
            self.assertFalse(result['notify'])
            self.assertFalse(result['stop'])

    def test_closed_without_merge_stops_the_monitor(self):
        with tempfile.TemporaryDirectory() as temp:
            project, state = Path(temp), Path(temp) / 'state'
            verdict = snapshot('BLOCKER', exitCode=6, blocker={
                'kind': 'merge-gate', 'pr': CONTEXT, 'reason': 'closed-without-merge'})
            result = monitor_record(TARGET, project, verdict, state, True)
            self.assertTrue(result['stop'])
            self.assertTrue(result['notify'])

    def test_wrong_target_or_malformed_snapshot_preserves_state(self):
        with tempfile.TemporaryDirectory() as temp:
            project, state = Path(temp), Path(temp) / 'state'
            original = monitor_record(TARGET, project, snapshot(), state, True)
            before = Path(original['state_path']).read_bytes()
            for verdict in ({'kind': 'READY'}, snapshot(frontier={**CONTEXT, 'number': 9}),
                            snapshot('READY', terminal=False), snapshot('READY', exitCode=7)):
                with self.subTest(verdict=verdict), self.assertRaises(ValueError):
                    monitor_record(TARGET, project, verdict, state, True)
                self.assertEqual(Path(original['state_path']).read_bytes(), before)

    def test_runner_uses_argument_vector_and_verifies_exit_status(self):
        with tempfile.TemporaryDirectory() as temp:
            project, state = Path(temp), Path(temp) / 'state'
            plan = {'project': str(project), 'command': ['/watcher', '--pr', '7', '--timeout', '45']}
            verdict = snapshot('READY')
            response = subprocess.CompletedProcess([], 0, json.dumps(verdict), '')
            with patch('codex_monitor.monitor_plan', return_value=plan), patch('codex_monitor.subprocess.run', return_value=response) as run:
                result = run_monitor(TARGET, project, state, True, bun='/runtime/bun')
                self.assertTrue(result['stop'])
                self.assertEqual(run.call_args.args[0], ['/runtime/bun', *plan['command']])
                self.assertEqual(run.call_args.kwargs['timeout'], 55)
            response = subprocess.CompletedProcess([], 1, json.dumps(verdict), 'failure')
            with patch('codex_monitor.monitor_plan', return_value=plan), patch('codex_monitor.subprocess.run', return_value=response):
                with self.assertRaises(RuntimeError):
                    run_monitor(TARGET, project, state)
