"""Project-scoped native history reads without opening or resuming chats."""
from pathlib import Path
import subprocess

SOURCES = ['cli', 'vscode', 'exec', 'appServer']


def project_paths(project, include_worktrees=False):
    project = project.expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError('History project must be a directory')
    paths = {str(project)}
    if include_worktrees:
        result = subprocess.run(['git', '-C', str(project), 'worktree', 'list', '--porcelain', '-z'],
                                capture_output=True, text=True, check=True, timeout=5)
        for field in result.stdout.split('\0'):
            if field.startswith('worktree '):
                paths.add(str(Path(field[9:]).resolve()))
    return sorted(paths)


def in_project(thread, paths):
    cwd = thread.get('cwd')
    return isinstance(cwd, str) and str(Path(cwd).resolve()) in paths


def list_history(client, paths, limit=20, cursor=None, search=None, archived=False, exclude=None):
    if not paths or not 1 <= limit <= 100:
        raise ValueError('History needs an explicit project and limit between 1 and 100')
    params = {'cwd': paths, 'limit': limit, 'sortKey': 'updated_at',
              'sortDirection': 'desc', 'sourceKinds': SOURCES, 'archived': archived,
              'useStateDbOnly': True}
    if cursor:
        params['cursor'] = cursor
    if search:
        params['searchTerm'] = search
    if exclude:
        params['excludedThreadIds'] = [exclude]
    page = client.call('thread/list', params)
    rows = page['data']
    # Never disclose even metadata if a backend ignores the project filter.
    if any(not in_project(row, paths) for row in rows):
        raise ValueError('Codex returned history outside the selected project; response withheld')
    return {'project_paths': paths, 'archived': archived,
            'evidence': 'metadata-only', 'threads': [
                {key: row.get(key) for key in ('id', 'name', 'preview', 'cwd', 'updatedAt', 'status')}
                for row in rows if row['id'] != exclude],
            'next_cursor': page.get('nextCursor')}


def read_history(client, paths, thread_id, limit=3, cursor=None):
    if not paths or not 1 <= limit <= 100:
        raise ValueError('History needs an explicit project and limit between 1 and 100')
    thread = client.call('thread/read', {'threadId': thread_id, 'includeTurns': False})['thread']
    if not in_project(thread, paths):
        raise ValueError('Thread does not belong to the selected project; turns were not read')
    params = {'threadId': thread_id, 'limit': limit, 'itemsView': 'full', 'sortDirection': 'desc'}
    if cursor:
        params['cursor'] = cursor
    page = client.call('thread/turns/list', params)
    return {'thread_id': thread_id, 'cwd': thread['cwd'],
            'evidence': 'persisted-items', 'turns': page['data'],
            'next_cursor': page.get('nextCursor'),
            'all_returned_turns_full': all(turn.get('itemsView') == 'full' for turn in page['data']),
            'limitations': 'Persisted items only; omitted/compacted history and unrecorded events are not reconstructed.'}
