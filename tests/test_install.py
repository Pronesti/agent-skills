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
    def test_local_update_preserves_existing_global_instructions_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            target = home / '.codex/AGENTS.md'
            target.parent.mkdir()
            original = ('# Personal instructions: español\r\n'
                        'Ask before creating another checkout.\r\n'
                        '<!-- personal-skill-policy:start -->\r\n'
                        'My existing policy\r\n'
                        '<!-- personal-skill-policy:end -->\r\n'
                        '<!-- lerd:begin -->\r\nLocal Lerd guidance\r\n'
                        '<!-- lerd:end -->\r\n').encode('utf-8')
            target.write_bytes(original)
            target.chmod(0o600)
            claude = home / '.claude/CLAUDE.md'
            claude.parent.mkdir()
            claude.write_bytes(b'Existing Claude instructions\r\n')
            initial = target.stat()
            for apply in (False, True, True):
                result = installer.install(home, apply=apply, runtime='skip')
                self.assertFalse(result['instructions']['changed'])
                self.assertIsNone(result['instructions']['backup'])
                self.assertEqual(result['instructions']['diff'], '')
                self.assertEqual(target.read_bytes(), original)
                self.assertEqual(target.stat().st_ino, initial.st_ino)
                self.assertEqual(target.stat().st_mtime_ns, initial.st_mtime_ns)
                self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            self.assertTrue((home / '.agents/skills/grilling').is_symlink())
            self.assertTrue((home / '.claude/skills/grilling').is_symlink())
            applied = subprocess.run(
                ['/bin/bash', str(installer.REPO / 'install.sh'), '--home', str(home),
                 '--runtime', 'skip'], capture_output=True, text=True, check=True,
            )
            self.assertTrue(json.loads(applied.stdout)['instructions']['preserved'])
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(claude.read_bytes(), b'Existing Claude instructions\r\n')
            self.assertEqual(target.stat().st_mtime_ns, initial.st_mtime_ns)
            self.assertFalse((home / '.local').exists())

    def test_local_update_preserves_override_and_symlink_targets(self):
        for kind in ('override', 'symlink', 'broken-symlink'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                home = Path(temp).resolve()
                target = home / '.codex/AGENTS.md'
                target.parent.mkdir()
                if kind == 'override':
                    protected = target.with_name('AGENTS.override.md')
                    protected.write_text('Local override')
                else:
                    protected = home / 'personal-instructions.md'
                    if kind == 'symlink':
                        protected.write_text('Personal instructions')
                    target.symlink_to(protected)
                for apply in (False, True):
                    result = installer.install(home, apply=apply, runtime='skip')
                    self.assertFalse(result['instructions']['changed'])
                    if kind == 'override':
                        self.assertFalse(target.exists())
                        self.assertEqual(protected.read_text(), 'Local override')
                    else:
                        self.assertTrue(target.is_symlink())
                        if kind == 'symlink':
                            self.assertEqual(protected.read_text(), 'Personal instructions')
                        else:
                            self.assertFalse(protected.exists())
                self.assertTrue((home / '.agents/skills/grilling').is_symlink())
                self.assertFalse((home / '.local').exists())

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

    def test_fresh_install_reports_no_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            self.assertIsNone(installer.install(home, runtime='skip')['backup'])
            self.assertIsNone(installer.install(home, True, runtime='skip')['backup'])
            self.assertFalse((home / '.local').exists())

    def test_stale_link_sweep_compares_real_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            home = root / 'home'
            alias = root / 'repo-alias'
            alias.symlink_to(installer.REPO, target_is_directory=True)
            other = root / 'other-checkout/skills/grilling'
            other.mkdir(parents=True)
            old_root = home / '.codex/skills'
            old_root.mkdir(parents=True)
            (old_root / 'grilling').symlink_to(alias / 'skills/grilling')
            (old_root / 'foreign').symlink_to(other)
            installer.install(home, True, runtime='skip')
            self.assertFalse((old_root / 'grilling').exists() or (old_root / 'grilling').is_symlink())
            self.assertTrue((old_root / 'foreign').is_symlink())

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

    def test_explicit_instruction_sync_preview_backup_and_repeat(self):
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
            preview = installer.install(home, runtime='skip', sync_agents=True)
            self.assertTrue(preview['instructions']['changed'])
            self.assertIn('-Local instructions: español', preview['instructions']['diff'])
            self.assertEqual(target.read_bytes(), old)
            self.assertFalse((home / '.agents').exists())
            self.assertFalse((home / '.local').exists())

            applied = installer.install(home, apply=True, runtime='skip', sync_agents=True)
            self.assertEqual(Path(applied['instructions']['backup']).read_bytes(), old)
            self.assertIn('## Working with me', target.read_text())
            self.assertIn('~/.config/agent-skills/runtime.md', target.read_text())
            self.assertNotIn('{{PERSONAL_SKILL_POLICY}}', target.read_text())
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            self.assertEqual(claude.read_text(), 'Existing Claude instructions')
            before = target.stat()
            repeated = installer.install(home, apply=True, runtime='skip', sync_agents=True)
            self.assertFalse(repeated['instructions']['changed'])
            self.assertIsNone(repeated['instructions']['backup'])
            self.assertEqual(repeated['actions'], [])
            self.assertEqual(target.stat().st_mtime_ns, before.st_mtime_ns)
            self.assertEqual(target.stat().st_ino, before.st_ino)

    def test_explicit_sync_rejects_unsafe_targets_before_skill_changes(self):
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
                        installer.install(home, apply=apply, runtime='skip', sync_agents=True)
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
                command = [sys.executable, str(installer.REPO / 'scripts/install.py'),
                           '--runtime', 'skip', '--apply', *flags]
                result = subprocess.run(
                    command,
                    capture_output=True, text=True, env=env, check=True,
                )
                data = json.loads(result.stdout)
                self.assertEqual(data['instructions']['target'], str(profile / 'AGENTS.md'))
                self.assertTrue((profile / 'AGENTS.md').is_file())
                self.assertTrue((destination / '.agents/skills/grilling').is_symlink())
                if mode != 'environment':
                    self.assertFalse(environment_profile.exists())
                if mode in ('home', 'codex-home'):
                    self.assertFalse(host.exists())
                target = profile / 'AGENTS.md'
                original = b'My checkout rule\r\n<!-- lerd:begin -->\r\nLocal runtime guidance\r\n'
                target.write_bytes(original)
                preserved = subprocess.run(command, capture_output=True, text=True, env=env, check=True)
                self.assertTrue(json.loads(preserved.stdout)['instructions']['preserved'])
                self.assertEqual(target.read_bytes(), original)
                synced = subprocess.run(command + ['--sync-agents'],
                                        capture_output=True, text=True, env=env, check=True)
                sync_result = json.loads(synced.stdout)['instructions']
                self.assertTrue(sync_result['changed'])
                self.assertEqual(Path(sync_result['backup']).read_bytes(), original)
                self.assertIn('## Working with me', target.read_text())


if __name__ == "__main__":
    unittest.main()
