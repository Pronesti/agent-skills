"""Native Codex discovery, model-role validation and managed agent installation."""
import hashlib
import json
from pathlib import Path
import queue
import re
import shutil
import stat
import subprocess
import tempfile
import threading
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]
READ_METHODS = {'model/list', 'thread/list', 'thread/read', 'thread/turns/list'}


class CodexReadClient:
    """Bounded read-only JSON-RPC client; never starts or resumes model turns."""
    def __init__(self, executable='codex', env=None, timeout=20):
        self.executable, self.env, self.timeout = executable, env, timeout
        self.process = None
        self.messages = queue.Queue()
        self.counter = 0

    def __enter__(self):
        self.process = subprocess.Popen(
            [self.executable, 'app-server', '--listen', 'stdio://'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, encoding='utf-8', env=self.env,
        )
        def receive():
            try:
                for line in self.process.stdout:
                    try:
                        self.messages.put(json.loads(line))
                    except ValueError:
                        continue
            finally:
                self.messages.put(None)
        threading.Thread(target=receive, daemon=True).start()
        try:
            self._request('initialize', {'clientInfo': {
                'name': 'pstack_codex', 'title': 'Pstack Codex integration', 'version': '1.0.0'}})
            self._send({'method': 'initialized', 'params': {}})
        except BaseException:
            self.close()
            raise
        return self

    def _send(self, message):
        self.process.stdin.write(json.dumps(message) + '\n')
        self.process.stdin.flush()

    def _request(self, method, params):
        self.counter += 1
        request_id = self.counter
        self._send({'id': request_id, 'method': method, 'params': params})
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                message = self.messages.get(timeout=max(0, deadline - time.monotonic()))
            except queue.Empty as exc:
                raise RuntimeError(f'Codex {method} timed out') from exc
            if message is None:
                raise RuntimeError(f'Codex disconnected during {method}')
            if 'method' in message and 'id' in message:
                self._send({'id': message['id'], 'error': {
                    'code': -32601, 'message': 'This client supports read-only queries only'}})
            elif message.get('id') == request_id:
                if 'error' in message:
                    raise RuntimeError(f"Codex {method}: {message['error'].get('message', 'request failed')}")
                return message['result']

    def call(self, method, params):
        if method not in READ_METHODS:
            raise ValueError(f'Unsupported read-only method: {method}')
        return self._request(method, params)

    def close(self):
        if self.process is None:
            return
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=3)
        for stream in (self.process.stdin, self.process.stdout):
            stream.close()

    def __exit__(self, *_):
        self.close()


def model_catalog(client):
    models, cursor, seen = {}, None, set()
    while True:
        params = {'limit': 100, 'includeHidden': False}
        if cursor:
            params['cursor'] = cursor
        page = client.call('model/list', params)
        for item in page['data']:
            models[item['model']] = item
        cursor = page.get('nextCursor')
        if not cursor:
            return models
        if cursor in seen:
            raise RuntimeError('Codex returned a repeated model cursor')
        seen.add(cursor)


def role_definitions(root=ROOT):
    return json.loads((root / 'config/codex/pstack-roles.json').read_text())['roles']


def default_choices(root=ROOT):
    return {'schema_version': 1, 'roles': {
        name: [{'model': 'inherit-parent'} for _ in range(2 if spec['panel'] else 1)]
        for name, spec in role_definitions(root).items()}}


def validate_choices(config, catalog=None, root=ROOT):
    if not isinstance(config, dict) or set(config) != {'schema_version', 'roles'} or config['schema_version'] != 1:
        raise ValueError('Model choices require schema_version 1 and roles')
    if not isinstance(config['roles'], dict):
        raise ValueError('Model roles must be an object')
    definitions = role_definitions(root)
    unknown = set(config['roles']) - set(definitions)
    if unknown:
        raise ValueError(f'Unknown model roles: {sorted(unknown)}')
    result = default_choices(root)
    for name, entries in config['roles'].items():
        spec = definitions[name]
        if not isinstance(entries, list) or not 1 <= len(entries) <= (8 if spec['panel'] else 1):
            raise ValueError(f'{name}: invalid number of role entries')
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) - {'model', 'effort'} or not isinstance(entry.get('model'), str):
                raise ValueError(f'{name}: use model and optional effort')
            model = entry['model']
            if model in ('auto', 'inherit-parent'):
                if 'effort' in entry:
                    raise ValueError(f'{name}: inherited models also inherit reasoning effort')
                continue
            if catalog is None or model not in catalog:
                raise ValueError(f'{name}: model is not in the native catalog: {model}')
            supported = {e['reasoningEffort'] for e in catalog[model]['supportedReasoningEfforts']}
            effort = entry.get('effort', catalog[model]['defaultReasoningEffort'])
            if not isinstance(effort, str) or effort not in supported:
                raise ValueError(f'{name}: unsupported reasoning effort for {model}')
        result['roles'][name] = entries
    return result


def config_path(home):
    return home / '.config/agent-skills/pstack-models.json'


def load_choices(home, catalog=None, root=ROOT, client_factory=CodexReadClient):
    path = config_path(home)
    legacy = path.with_suffix('.md')
    if not path.exists():
        if legacy.exists():
            raise ValueError(f'{legacy}: migrate the legacy role choices to JSON with pstack_codex.py configure; file preserved')
        return default_choices(root)
    config = json.loads(path.read_text())
    if not isinstance(config, dict):
        raise ValueError('Model choices must be an object')
    # Structural validation first; only an explicit real model needs discovery.
    uses_models = any(isinstance(entries, list) and any(isinstance(e, dict) and e.get('model') not in ('auto', 'inherit-parent')
                      for e in entries) for entries in config.get('roles', {}).values()) if isinstance(config.get('roles'), dict) else False
    if uses_models and catalog is None:
        with client_factory() as client:
            catalog = model_catalog(client)
    return resolve_efforts(validate_choices(config, catalog, root), catalog)


def render_agents(choices, root=ROOT):
    pstack = str((root / 'pstack').resolve())
    agents = {}
    for path in sorted((root / 'config/codex/agents').glob('*.toml')):
        data = tomllib.loads(path.read_text())
        data['developer_instructions'] = data['developer_instructions'].replace('{{PSTACK_ROOT}}', pstack)
        agents[data['name'] + '.toml'] = data
    for role, spec in role_definitions(root).items():
        for index, entry in enumerate(choices['roles'][role]):
            name = spec['agent'] + (f'-{index + 1}' if spec['panel'] else '')
            instructions = (
                "Use this role only when explicitly requested or assigned by an explicitly selected pstack workflow.\n"
                f"Read {pstack}/docs/harness/codex.md first.\n"
                f"Your role is {role}. {spec['purpose']}\n"
                f"Read {pstack}/skills/{spec['workflow']}/SKILL.md and the references assigned by the parent.\n"
                "You are a delegate, not a replacement for the parent's coordinator.\n"
                "Use the workflow as reference for your assigned role; do not restart its orchestration or fan-out.\n"
                "Treat source and history as evidence; preserve project scope, permissions and authorization.\n"
                + ('Read-only assignment: do not edit files or perform external writes.\n' if spec['read_only'] else
                   'Edit only the assigned scope; provide actual verification results.\n')
            )
            data = {'name': name, 'description': f"Pstack role: {role}. {spec['purpose']}",
                    'developer_instructions': instructions}
            if entry['model'] not in ('auto', 'inherit-parent'):
                data['model'] = entry['model']
                # Avoid inheriting an effort incompatible with the chosen model.
                if 'effort' not in entry:
                    raise ValueError(f'{role}: resolve an explicit model to its native default effort before rendering')
                data['model_reasoning_effort'] = entry['effort']
            agents[name + '.toml'] = data
    return {name: ''.join(f'{key} = {json.dumps(value, ensure_ascii=False)}\n' for key, value in data.items())
            for name, data in agents.items()}


def resolve_efforts(choices, catalog):
    result = json.loads(json.dumps(choices))
    for entries in result['roles'].values():
        for entry in entries:
            if entry['model'] not in ('auto', 'inherit-parent'):
                entry.setdefault('effort', catalog[entry['model']]['defaultReasoningEffort'])
    return result


def native_agent_plan(home, codex_home, choices=None, catalog=None, root=ROOT):
    choices = choices if choices is not None else load_choices(home, catalog, root)
    if any(e['model'] not in ('auto', 'inherit-parent') and 'effort' not in e
           for entries in choices['roles'].values() for e in entries):
        if catalog is None:
            with CodexReadClient() as client:
                catalog = model_catalog(client)
        choices = resolve_efforts(choices, catalog)
    rendered = render_agents(choices, root)
    owner = codex_home / 'agents/.pstack-managed.json'
    if owner.parent.is_symlink() or owner.is_symlink():
        raise ValueError(f'Unmanaged agent ownership symlink: {owner}')
    metadata = json.loads(owner.read_text()) if owner.exists() else {'schema_version': 1, 'files': {}}
    if not isinstance(metadata, dict) or metadata.get('schema_version') != 1 or not isinstance(metadata.get('files'), dict):
        raise ValueError('Invalid native-agent ownership manifest')
    owned = metadata['files']
    if any(not re.fullmatch(r'pstack-[a-z0-9-]+\.toml', name) for name in owned):
        raise ValueError('Invalid native-agent ownership manifest')
    operations = []
    checksums = {name: hashlib.sha256(content.encode()).hexdigest() for name, content in rendered.items()}
    for name in sorted(set(owned) | set(rendered)):
        path = owner.parent / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f'Unmanaged native agent collision: {path}')
        old = path.read_bytes() if path.exists() else None
        new = rendered.get(name)
        if new is not None and old == new.encode():
            continue
        if old is not None and hashlib.sha256(old).hexdigest() != owned.get(name):
            raise ValueError(f'Locally modified or unmanaged native agent: {path}; preserved')
        if old is not None or new is not None:
            operations.append({'path': path, 'content': new})
    content = json.dumps({'schema_version': 1, 'files': checksums}, indent=2) + '\n'
    if not owner.exists() or owner.read_text() != content:
        operations.append({'path': owner, 'content': content})
    return {'agents': len(rendered), 'operations': operations, 'choices': choices,
            'panels': {role: len({e['model'] for e in entries if e['model'] not in ('auto', 'inherit-parent')}) > 1
                       for role, entries in choices['roles'].items() if role_definitions(root)[role]['panel']}}


def atomic_write(path, content, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.' + path.name, delete=False) as output:
            temporary = Path(output.name)
            output.write(content.encode('utf-8'))
        temporary.chmod(mode)
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def apply_agent_plan(plan, home, backup, apply=False):
    actions = []
    for operation in plan['operations']:
        path = operation['path']
        if path.exists():
            # Custom CODEX_HOME can be outside --home; keep backups under home.
            relative = path.relative_to(home) if path.is_relative_to(home) else Path('codex-agents') / path.name
            destination = backup / relative
            if apply:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
            actions.append(f'backup {path} -> {destination}')
        if operation['content'] is None:
            if apply:
                path.unlink()
            actions.append(f'retire native agent {path}')
        else:
            if apply:
                mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
                atomic_write(path, operation['content'], mode)
            actions.append(f'write native agent {path}')
    return {'agents': plan['agents'], 'panels_use_distinct_models': plan['panels'], 'actions': actions}
