"""Render the shared global instructions, install them for Codex, and wire Claude to import them."""
import datetime
import difflib
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile

from atomic_files import write_atomic
from invocation_policy import host_policy_body

REPO = Path(__file__).resolve().parents[1]
START = '<!-- personal-skill-policy:start -->'
END = '<!-- personal-skill-policy:end -->'
TOKEN = '{{PERSONAL_SKILL_POLICY}}'
CLAUDE_HEADER = ('<!-- Claude loads the shared global instructions through this import. '
                 'Edit config/AGENTS.md in the agent-skills repository, not this file. -->')


def codex_home_path(home=None, codex_home=None):
    """The selected Codex directory as an absolute path that keeps symlinks as written."""
    if codex_home is None:
        codex_home = (home / '.codex' if home is not None else
                      Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex'))
    return Path(os.path.abspath(codex_home.expanduser()))


def resolve_codex_home(home=None, codex_home=None):
    return codex_home_path(home, codex_home).resolve()


def render_instructions(root=REPO):
    template = root / 'config/AGENTS.md'
    content = template.read_text(encoding='utf-8')
    if any(content.count(marker) != 1 for marker in (START, END, TOKEN)):
        raise ValueError(f'{template}: expected one policy block and one {TOKEN} placeholder')
    if f'{START}\n{TOKEN}\n{END}' not in content:
        raise ValueError(f'{template}: policy block must contain only {TOKEN}')
    return content.replace(TOKEN, host_policy_body(root).rstrip())


def sync_instructions(home, codex_home, apply=False, root=REPO, *, replace_existing=True):
    target = codex_home / 'AGENTS.md'
    override = codex_home / 'AGENTS.override.md'
    if not replace_existing and (target.exists() or target.is_symlink()
                                 or override.exists() or override.is_symlink()):
        return {'applied': apply, 'changed': False, 'target': str(target),
                'backup': None, 'diff': '', 'preserved': True}
    if override.exists() or override.is_symlink():
        raise ValueError(f'{override} takes precedence over AGENTS.md; resolve the override before syncing')
    if target.is_symlink():
        raise ValueError(f'{target} is a symlink; move it aside before installing a regular file')
    if target.exists() and not target.is_file():
        raise ValueError(f'{target} is not a regular file; left untouched')

    new = render_instructions(root).encode('utf-8')
    old = target.read_bytes() if replace_existing and target.exists() else b''
    changed = new != old
    diff = ''.join(difflib.unified_diff(
        old.decode('utf-8').splitlines(keepends=True),
        new.decode('utf-8').splitlines(keepends=True),
        fromfile=str(target), tofile='shared global instructions',
    ))
    backup = None
    if apply and changed:
        mode = stat.S_IMODE(target.stat().st_mode) if replace_existing and target.exists() else 0o644
        if replace_existing and target.exists():
            backup_root = home / '.local/share/agent-skills/backups'
            backup_root.mkdir(parents=True, exist_ok=True)
            stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup_dir = Path(tempfile.mkdtemp(prefix=f'{stamp}-agents-', dir=backup_root))
            backup = backup_dir / 'AGENTS.md'
            shutil.copy2(target, backup)
        if not replace_existing and (override.exists() or override.is_symlink()):
            changed, diff = False, ''
        # Create-only mode never replaces a file that appeared after preflight.
        elif not write_atomic(target, new, mode, replace=replace_existing):
            changed, diff = False, ''
    return {'applied': apply, 'changed': changed, 'target': str(target),
            'backup': str(backup) if backup else None, 'diff': diff,
            'preserved': not replace_existing and not changed}


def claude_import_line(codex_home):
    """The Claude Code import that loads the shared instructions from the Codex file.

    Pass the Codex directory as configured (see codex_home_path), so a symlinked
    directory stays a symlink in the import instead of freezing its current target.
    """
    target = Path(os.path.abspath(codex_home / 'AGENTS.md'))
    try:
        return '@~/' + str(target.relative_to(Path.home()))
    except ValueError:
        return '@' + str(target)


IMPORT = re.compile(r'(?<![\w`])@([^\s`]+)')


def imports_shared(text, codex_home, base_dir):
    """Whether Claude memory text imports the shared AGENTS.md.

    Claude resolves a relative import against the directory of the importing file.
    """
    target = (codex_home / 'AGENTS.md').resolve()
    for match in IMPORT.finditer(text):
        path = Path(match.group(1)).expanduser()
        if not path.is_absolute():
            path = base_dir / path
        if path.resolve() == target:
            return True
    return False


def link_claude(home, codex_home, apply=False):
    """Create ~/.claude/CLAUDE.md as an import of the shared instructions when it is missing.

    An existing file is never changed; the result reports whether it already imports them.
    Nothing is created while only AGENTS.override.md exists, because the import would
    point at a missing file.
    """
    target = home / '.claude/CLAUDE.md'
    shared = codex_home / 'AGENTS.md'
    override = codex_home / 'AGENTS.override.md'
    if target.exists() or target.is_symlink():
        text = target.read_text(encoding='utf-8') if target.is_file() else ''
        return {'target': str(target), 'changed': False, 'applied': apply,
                'imports_shared': imports_shared(text, codex_home, target.parent)}
    if not (shared.exists() or shared.is_symlink()) and (override.exists() or override.is_symlink()):
        return {'target': str(target), 'changed': False, 'applied': apply, 'imports_shared': False,
                'skipped': f'{override} replaces AGENTS.md for Codex; no shared file to import'}
    content = (CLAUDE_HEADER + '\n' + claude_import_line(codex_home) + '\n').encode('utf-8')
    if apply and not write_atomic(target, content, 0o644, replace=False):
        return link_claude(home, codex_home, apply)
    return {'target': str(target), 'changed': True, 'applied': apply, 'imports_shared': True}
