import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
spec.loader.exec_module(installer)
sys.path.pop(0)


class InstallationTests(unittest.TestCase):
    def test_nested_repository_directory_is_not_a_managed_checkout_root(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'keep'
            target.symlink_to(installer.REPO / 'tests/skills/keep')
            self.assertIsNone(installer.git_common_dir(installer.REPO / 'tests'))
            self.assertFalse(installer.managed_link(target))

    def test_pstack_replaces_only_repository_links_and_repeat_is_empty(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            unrelated = home / 'unrelated/skills/keep'
            unrelated.mkdir(parents=True)
            (unrelated / 'SKILL.md').write_text('external skill')
            old_links = []
            for host in ('.agents', '.claude', '.codex', '.cursor'):
                location = home / host / 'skills'
                location.mkdir(parents=True)
                stale = location / 'removed-skill'
                stale.symlink_to(installer.REPO / 'skills/removed-skill')
                old_links.append(stale)
                (location / 'keep').symlink_to(unrelated)
                copy = location / 'personal-copy'
                copy.mkdir()
                (copy / 'SKILL.md').write_text('personal edits')
            expected = {p.name for p in (installer.REPO / 'skills').iterdir()
                        if (p / 'SKILL.md').is_file()}
            self.assertEqual(len(expected), 56)
            self.assertNotIn('benny', expected)
            preview = installer.install(home, runtime='skip')
            self.assertEqual(preview['skills'], len(expected))
            self.assertTrue(all(p.is_symlink() for p in old_links))
            self.assertFalse((home / '.local').exists())
            applied = installer.install(home, True, runtime='skip')
            for old in old_links:
                self.assertFalse(old.is_symlink())
                saved = Path(applied['backup']) / old.relative_to(home)
                self.assertTrue(saved.is_symlink())
                self.assertEqual(saved.readlink(), installer.REPO / 'skills/removed-skill')
            for host in ('.agents', '.claude'):
                for name in expected:
                    installed = home / host / 'skills' / name
                    self.assertEqual(installed.resolve(), installer.REPO / 'skills' / name)
                    canonical = installed.resolve()
                    self.assertTrue((canonical / '../../pstack/skills' / name / 'SKILL.md').is_file())
            for host in ('.agents', '.claude', '.codex', '.cursor'):
                location = home / host / 'skills'
                self.assertEqual((location / 'keep').resolve(), unrelated)
                self.assertEqual((location / 'personal-copy/SKILL.md').read_text(), 'personal edits')
            self.assertEqual(installer.install(home, True, runtime='skip')['actions'], [])

    def test_sibling_worktree_migration_and_unrelated_same_name_collision(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            sibling = home / 'sibling-checkout'
            target = home / '.agents/skills/how'
            target.parent.mkdir(parents=True)
            target.symlink_to(sibling / 'skills/how')
            common = installer.git_common_dir(installer.REPO)
            def same_repository(root):
                return common if root in (sibling, installer.REPO) else None
            with patch.object(installer, 'git_common_dir', side_effect=same_repository):
                preview = installer.install(home, runtime='skip')
                self.assertTrue(preview['actions'])
                self.assertEqual(target.readlink(), sibling / 'skills/how')
                result = installer.install(home, True, runtime='skip')
            self.assertEqual(target.resolve(), installer.REPO / 'skills/how')
            saved = Path(result['backup']) / '.agents/skills/how'
            self.assertEqual(saved.readlink(), sibling / 'skills/how')

        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            foreign = home / 'other-repository/skills/how'
            foreign.mkdir(parents=True)
            target = home / '.agents/skills/how'
            target.parent.mkdir(parents=True)
            target.symlink_to(foreign)
            with self.assertRaisesRegex(RuntimeError, 'Unmanaged collision'):
                installer.install(home, True, runtime='skip')
            self.assertEqual(target.resolve(), foreign)
            self.assertFalse((home / '.codex').exists())
            self.assertFalse((home / '.local').exists())

    def test_migration_preserves_old_copy_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            existing = home / ".agents/skills/how"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text("local customization")
            lock = home / ".agents/.skill-lock.json"
            lock.write_text(json.dumps({"skills": {"how": {"source": "mattpocock/skills"}, "unrelated": {"source": "someone/else"}}}))
            old = home / ".codex/skills/how"
            old.parent.mkdir(parents=True)
            old.symlink_to(installer.REPO / "skills/how")
            preview = installer.install(home, runtime='skip')
            self.assertFalse(existing.is_symlink())
            self.assertTrue(preview["actions"])
            result = installer.install(home, True, runtime='skip')
            self.assertEqual(existing.resolve(), installer.REPO / "skills/how")
            self.assertFalse(old.is_symlink())
            self.assertEqual((Path(result["backup"]) / ".agents/skills/how/SKILL.md").read_text(), "local customization")
            self.assertIn("unrelated", json.loads(lock.read_text())["skills"])
            self.assertNotIn("how", json.loads(lock.read_text())["skills"])
            self.assertEqual(installer.install(home, True, runtime='skip')["actions"], [])

    def test_unmanaged_collision_changes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            collision = home / ".claude/skills/poteto-mode"
            collision.mkdir(parents=True)
            (collision / "SKILL.md").write_text("unrelated installation")
            with self.assertRaisesRegex(RuntimeError, "Unmanaged collision"):
                installer.install(home, True, runtime='skip')
            self.assertFalse((home / ".agents/skills").exists())
            self.assertFalse((home / ".codex/AGENTS.md").exists())
            self.assertEqual((collision / "SKILL.md").read_text(), "unrelated installation")

    def test_shared_instructions_preview_backup_and_repeat(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            target = home / '.codex/AGENTS.md'
            target.parent.mkdir()
            old = 'Local instructions: español\r\n'.encode('utf-8')
            target.write_bytes(old)
            target.chmod(0o600)
            claude = home / '.claude/CLAUDE.md'
            claude.parent.mkdir()
            claude.write_text('Existing Claude instructions')
            preview = installer.install(home, runtime='skip')
            self.assertTrue(preview['codex_agents']['changed'])
            self.assertIn('-Local instructions: español', preview['codex_agents']['diff'])
            self.assertEqual(target.read_bytes(), old)
            self.assertFalse((home / '.agents').exists())
            self.assertFalse((home / '.local').exists())

            applied = installer.install(home, apply=True, runtime='skip')
            self.assertEqual(Path(applied['codex_agents']['backup']).read_bytes(), old)
            self.assertIn('## Working with me', target.read_text())
            self.assertIn('~/.config/agent-skills/runtime.md', target.read_text())
            self.assertNotIn('{{PERSONAL_SKILL_POLICY}}', target.read_text())
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            self.assertEqual(claude.read_text(), 'Existing Claude instructions')
            before = target.stat()
            repeated = installer.install(home, apply=True, runtime='skip')
            self.assertFalse(repeated['codex_agents']['changed'])
            self.assertIsNone(repeated['codex_agents']['backup'])
            self.assertEqual(repeated['actions'], [])
            self.assertEqual(target.stat().st_mtime_ns, before.st_mtime_ns)
            self.assertEqual(target.stat().st_ino, before.st_ino)

    def test_unsafe_codex_targets_stop_before_skill_changes(self):
        for conflict in ('override', 'symlink', 'directory'):
            with self.subTest(conflict=conflict), tempfile.TemporaryDirectory() as temp:
                home = Path(temp).resolve()
                target = home / '.codex/AGENTS.md'
                target.parent.mkdir()
                if conflict == 'override':
                    target.with_name('AGENTS.override.md').write_text('Local override')
                elif conflict == 'symlink':
                    target.symlink_to(home / 'missing.md')
                else:
                    target.mkdir()
                for apply in (False, True):
                    with self.assertRaises(ValueError):
                        installer.install(home, apply=apply, runtime='skip')
                    self.assertFalse((home / '.agents').exists())
                    self.assertFalse((home / '.claude').exists())
                    self.assertFalse((home / '.local').exists())

    def test_cli_codex_directory_precedence_and_scratch_isolation(self):
        for mode in ('default', 'environment', 'home', 'codex-home'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                root = Path(temp).resolve()
                host = root / 'host-home'
                environment_profile = root / 'environment-profile'
                env = dict(os.environ, HOME=str(host), CODEX_HOME=str(environment_profile))
                flags = []
                destination = host
                profile = environment_profile
                if mode == 'default':
                    env.pop('CODEX_HOME')
                    profile = host / '.codex'
                elif mode in ('home', 'codex-home'):
                    destination = root / 'scratch-home'
                    flags += ['--home', str(destination)]
                    profile = destination / '.codex'
                    if mode == 'codex-home':
                        profile = root / 'explicit-profile'
                        flags += ['--codex-home', str(profile)]
                result = subprocess.run(
                    [sys.executable, str(installer.REPO / 'scripts/install.py'),
                     '--runtime', 'skip', '--apply', *flags],
                    capture_output=True, text=True, env=env, check=True,
                )
                data = json.loads(result.stdout)
                self.assertEqual(data['codex_agents']['target'], str(profile / 'AGENTS.md'))
                self.assertTrue((profile / 'AGENTS.md').is_file())
                self.assertTrue((destination / '.agents/skills/how').is_symlink())
                if mode != 'environment':
                    self.assertFalse(environment_profile.exists())
                if mode in ('home', 'codex-home'):
                    self.assertFalse(host.exists())


if __name__ == "__main__":
    unittest.main()
