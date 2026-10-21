from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from codex_history import list_history, project_paths, read_history


class Client:
    def __init__(self, responses):
        self.responses, self.calls = list(responses), []
    def call(self, method, params):
        self.calls.append((method, params))
        return self.responses.pop(0)


class NativeHistoryTests(unittest.TestCase):
    def test_list_preserves_project_pagination_archive_and_exclusions(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = project_paths(Path(temp))
            client = Client([{'data': [{'id': 'other', 'cwd': paths[0], 'name': 'Saved task', 'preview': 'evidence'},
                                       {'id': 'current', 'cwd': paths[0]}], 'nextCursor': 'page2'}])
            result = list_history(client, paths, cursor='page1', search='topic', archived=True, exclude='current')
            self.assertEqual([t['id'] for t in result['threads']], ['other'])
            self.assertEqual(result['next_cursor'], 'page2')
            params = client.calls[0][1]
            self.assertEqual(params['cwd'], paths)
            self.assertEqual(params['cursor'], 'page1')
            self.assertTrue(params['archived'])
            self.assertEqual(params['searchTerm'], 'topic')
            self.assertTrue(params['useStateDbOnly'])

    def test_foreign_history_is_withheld_even_if_server_ignores_filter(self):
        client = Client([{'data': [{'id': 'foreign', 'cwd': '/other/project', 'preview': 'private'}]}])
        with self.assertRaisesRegex(ValueError, 'response withheld'):
            list_history(client, ['/my/project'])

    def test_read_checks_scope_before_loading_any_turns(self):
        client = Client([{'thread': {'id': 'foreign', 'cwd': '/other/project'}}])
        with self.assertRaisesRegex(ValueError, 'turns were not read'):
            read_history(client, ['/my/project'], 'foreign')
        self.assertEqual([method for method, _ in client.calls], ['thread/read'])

    def test_read_keeps_full_native_items_and_reports_partial_history(self):
        client = Client([{'thread': {'id': 't', 'cwd': '/my/project'}},
                         {'data': [{'id': 'turn', 'itemsView': 'full', 'items': [
                             {'id': 'tool', 'type': 'commandExecution', 'aggregatedOutput': 'observed value'}]}],
                          'nextCursor': 'older'}])
        result = read_history(client, ['/my/project'], 't', limit=2, cursor='newer')
        self.assertTrue(result['all_returned_turns_full'])
        self.assertEqual(result['turns'][0]['items'][0]['aggregatedOutput'], 'observed value')
        self.assertEqual(result['next_cursor'], 'older')
        self.assertEqual(client.calls[1][1]['itemsView'], 'full')
        self.assertEqual(client.calls[1][1]['cursor'], 'newer')
        self.assertIn('not reconstructed', result['limitations'])
