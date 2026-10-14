import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
spec.loader.exec_module(installer)
sys.path.pop(0)


class InstallationTests(unittest.TestCase):
    def test_migration_preserves_old_copy_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            existing = home / ".agents/skills/grilling"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text("local customization")
            lock = home / ".agents/.skill-lock.json"
            lock.write_text(json.dumps({"skills": {"grilling": {"source": "mattpocock/skills"}, "unrelated": {"source": "someone/else"}}}))
            old = home / ".codex/skills/grilling"
            old.parent.mkdir(parents=True)
            old.symlink_to(installer.REPO / "skills/grilling")
            preview = installer.install(home, runtime='skip')
            self.assertFalse(existing.is_symlink())
            self.assertTrue(preview["actions"])
            result = installer.install(home, True, runtime='skip')
            self.assertEqual(existing.resolve(), installer.REPO / "skills/grilling")
            self.assertFalse(old.is_symlink())
            self.assertEqual((Path(result["backup"]) / ".agents/skills/grilling/SKILL.md").read_text(), "local customization")
            self.assertIn("unrelated", json.loads(lock.read_text())["skills"])
            self.assertNotIn("grilling", json.loads(lock.read_text())["skills"])
            self.assertEqual(installer.install(home, True, runtime='skip')["actions"], [])

    def test_unmanaged_collision_changes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            collision = home / ".claude/skills/writing-plans"
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
                self.assertTrue((destination / '.agents/skills/grilling').is_symlink())
                if mode != 'environment':
                    self.assertFalse(environment_profile.exists())
                if mode in ('home', 'codex-home'):
                    self.assertFalse(host.exists())


if __name__ == "__main__":
    unittest.main()
