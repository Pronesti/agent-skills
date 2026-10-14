"""Render and explicitly install the repository's complete global Codex instructions."""
import datetime
import difflib
import os
from pathlib import Path
import shutil
import stat
import tempfile

from invocation_policy import host_policy_body

REPO = Path(__file__).resolve().parents[1]
START = '<!-- personal-skill-policy:start -->'
END = '<!-- personal-skill-policy:end -->'
TOKEN = '{{PERSONAL_SKILL_POLICY}}'


def resolve_codex_home(home=None, codex_home=None):
    if codex_home is None:
        codex_home = (home / '.codex' if home is not None else
                      Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex'))
    return codex_home.expanduser().resolve()


def render_instructions(root=REPO):
    template = root / 'config/codex/AGENTS.md'
    content = template.read_text(encoding='utf-8')
    if any(content.count(marker) != 1 for marker in (START, END, TOKEN)):
        raise ValueError(f'{template}: expected one policy block and one {TOKEN} placeholder')
    if f'{START}\n{TOKEN}\n{END}' not in content:
        raise ValueError(f'{template}: policy block must contain only {TOKEN}')
    return content.replace(TOKEN, host_policy_body(root).rstrip())


def sync_instructions(home, codex_home, apply=False, root=REPO):
    target = codex_home / 'AGENTS.md'
    override = codex_home / 'AGENTS.override.md'
    if override.exists() or override.is_symlink():
        raise ValueError(f'{override} takes precedence over AGENTS.md; resolve the override before syncing')
    if target.is_symlink():
        raise ValueError(f'{target} is a symlink; move it aside before installing a regular file')
    if target.exists() and not target.is_file():
        raise ValueError(f'{target} is not a regular file; left untouched')

    new = render_instructions(root).encode('utf-8')
    old = target.read_bytes() if target.exists() else b''
    changed = new != old
    diff = ''.join(difflib.unified_diff(
        old.decode('utf-8').splitlines(keepends=True),
        new.decode('utf-8').splitlines(keepends=True),
        fromfile=str(target), tofile='shared Codex instructions',
    ))
    backup = None
    if apply and changed:
        mode = stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o644
        if target.exists():
            backup_root = home / '.local/share/agent-skills/backups'
            backup_root.mkdir(parents=True, exist_ok=True)
            stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup_dir = Path(tempfile.mkdtemp(prefix=f'{stamp}-codex-agents-', dir=backup_root))
            backup = backup_dir / 'AGENTS.md'
            shutil.copy2(target, backup)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.AGENTS.md-', delete=False) as output:
                temporary = Path(output.name)
                output.write(new)
            temporary.chmod(mode)
            temporary.replace(target)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    return {'applied': apply, 'changed': changed, 'target': str(target),
            'backup': str(backup) if backup else None, 'diff': diff}
