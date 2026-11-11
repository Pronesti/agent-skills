import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import global_instructions
sys.path.pop(0)


class GlobalInstructionsTests(unittest.TestCase):
    def test_bootstrap_preserves_a_file_created_during_installation(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            target = home / '.codex/AGENTS.md'
            original = b'Instructions created concurrently\r\n'
            link = os.link

            def create_before_link(source, destination):
                target.write_bytes(original)
                return link(source, destination)

            with patch.object(global_instructions.os, 'link', side_effect=create_before_link):
                result = global_instructions.sync_instructions(
                    home, target.parent, apply=True, replace_existing=False,
                )
            self.assertTrue(result['preserved'])
            self.assertFalse(result['changed'])
            self.assertIsNone(result['backup'])
            self.assertEqual(result['diff'], '')
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(list(target.parent.iterdir()), [target])
            self.assertFalse((home / '.local').exists())

    def run_sync(self, home, *flags, env=None, success=True):
        command = [sys.executable, str(ROOT / 'scripts/configure_hosts.py')]
        if home is not None:
            command += ['--home', str(home)]
        result = subprocess.run(
            command + ['--sync-agents', *flags],
            capture_output=True, text=True, env=env,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        return result

    def test_fresh_preview_writes_nothing_and_two_homes_get_identical_files(self):
        with tempfile.TemporaryDirectory() as temp:
            homes = [Path(temp).resolve() / name for name in ('computer', 'vm')]
            for home in homes:
                preview = self.run_sync(home)
                self.assertFalse(preview['applied'])
                self.assertTrue(preview['changed'])
                self.assertIsNone(preview['backup'])
                self.assertIn('+## Git workflow', preview['diff'])
                self.assertFalse(home.exists())
                applied = self.run_sync(home, '--apply')
                self.assertTrue(applied['applied'])
                self.assertTrue(applied['changed'])
                self.assertIsNone(applied['backup'])
                self.assertTrue(applied['claude']['changed'])
                self.assertIn(f"@{home / '.codex/AGENTS.md'}",
                              (home / '.claude/CLAUDE.md').read_text())
                self.assertFalse((home / '.agents').exists())
                self.assertFalse((home / 'plugins').exists())
            files = [home / '.codex/AGENTS.md' for home in homes]
            self.assertEqual(files[0].read_bytes(), files[1].read_bytes())
            content = files[0].read_text()
            self.assertIn('`caveman:surgical-patch`', content)
            self.assertIn('Use one feature branch created from `main`', content)
            self.assertEqual(content.count('<!-- personal-skill-policy:start -->'), 1)
            self.assertNotIn('{{PERSONAL_SKILL_POLICY}}', content)

    def test_preview_backup_replacement_and_repeat_preserve_expected_state(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            target = home / '.codex/AGENTS.md'
            target.parent.mkdir()
            old = 'Local instructions: español\r\n'.encode('utf-8')
            target.write_bytes(old)
            target.chmod(0o600)
            claude = home / '.claude/CLAUDE.md'
            claude.parent.mkdir()
            claude.write_text('Claude instructions')
            preview = self.run_sync(home)
            self.assertIn('-Local instructions: español', preview['diff'])
            self.assertEqual(target.read_bytes(), old)
            self.assertFalse((home / '.local').exists())
            applied = self.run_sync(home, '--apply')
            backup = Path(applied['backup'])
            self.assertEqual(backup.read_bytes(), old)
            self.assertTrue(backup.is_relative_to(home / '.local/share/agent-skills/backups'))
            self.assertNotIn(b'Local instructions', target.read_bytes())
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            self.assertEqual(claude.read_text(), 'Claude instructions')
            before = target.stat()
            repeated = self.run_sync(home, '--apply')
            self.assertFalse(repeated['changed'])
            self.assertIsNone(repeated['backup'])
            self.assertEqual(repeated['diff'], '')
            self.assertEqual(target.stat().st_mtime_ns, before.st_mtime_ns)
            self.assertEqual(target.stat().st_ino, before.st_ino)

    def test_override_blocks_preview_and_apply_without_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            target = home / '.codex/AGENTS.md'
            target.parent.mkdir()
            target.write_text('Existing instructions')
            override = target.with_name('AGENTS.override.md')
            override.write_text('Override instructions')
            for flags in ((), ('--apply',)):
                result = self.run_sync(home, *flags, success=False)
                self.assertIn('AGENTS.override.md', result.stderr)
                self.assertEqual(target.read_text(), 'Existing instructions')
                self.assertEqual(override.read_text(), 'Override instructions')
                self.assertFalse((home / '.local').exists())

    def test_existing_or_broken_symlink_is_not_followed_or_replaced(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve() / 'home'
            source = Path(temp).resolve() / 'other.md'
            source.write_text('Unrelated file')
            target = home / '.codex/AGENTS.md'
            target.parent.mkdir(parents=True)
            target.symlink_to(source)
            result = self.run_sync(home, '--apply', success=False)
            self.assertIn('symlink', result.stderr)
            self.assertTrue(target.is_symlink())
            self.assertEqual(source.read_text(), 'Unrelated file')
            source.unlink()
            result = self.run_sync(home, '--apply', success=False)
            self.assertIn('symlink', result.stderr)
            self.assertTrue(target.is_symlink())
            self.assertFalse(source.exists())
            self.assertFalse((home / '.local').exists())

    def test_directory_collision_is_left_untouched(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            target = home / '.codex/AGENTS.md'
            target.mkdir(parents=True)
            result = self.run_sync(home, '--apply', success=False)
            self.assertIn('regular file', result.stderr)
            self.assertTrue(target.is_dir())
            self.assertFalse((home / '.local').exists())

    def test_codex_home_environment_and_explicit_home_isolation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            profile = root / 'custom-codex'
            env = dict(os.environ, CODEX_HOME=str(profile))
            preview = self.run_sync(None, env=env)
            self.assertEqual(preview['target'], str(profile / 'AGENTS.md'))
            self.assertFalse(profile.exists())
            isolated = root / 'isolated-home'
            applied = self.run_sync(isolated, '--apply', env=env)
            self.assertEqual(applied['target'], str(isolated / '.codex/AGENTS.md'))
            self.assertFalse(profile.exists())

    def test_explicit_codex_home_and_backup_outside_home(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            home = root / 'home'
            profile = root / 'profile'
            profile.mkdir()
            target = profile / 'AGENTS.md'
            target.write_text('Custom profile instructions')
            env = dict(os.environ, CODEX_HOME=str(root / 'ignored-profile'))
            result = self.run_sync(home, '--codex-home', str(profile), '--apply', env=env)
            self.assertEqual(result['target'], str(target))
            backup = Path(result['backup'])
            self.assertEqual(backup.read_text(), 'Custom profile instructions')
            self.assertTrue(backup.is_relative_to(home / '.local/share/agent-skills/backups'))
            self.assertFalse((home / '.codex').exists())
            self.assertFalse((root / 'ignored-profile').exists())

    def test_sync_options_cannot_accidentally_trigger_legacy_configuration(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve() / 'home'
            for flags in (['--apply'], ['--codex-home', str(home / '.codex')],
                          ['--sync-agents', '--policy-only']):
                result = subprocess.run(
                    [sys.executable, str(ROOT / 'scripts/configure_hosts.py'),
                     '--home', str(home), *flags], capture_output=True, text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(home.exists())

    def test_policy_only_refresh_does_not_change_synced_global_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            self.run_sync(home, '--apply')
            target = home / '.codex/AGENTS.md'
            content = target.read_bytes()
            subprocess.run(
                [sys.executable, str(ROOT / 'scripts/configure_hosts.py'),
                 '--home', str(home), '--policy-only'],
                check=True, capture_output=True, text=True,
            )
            self.assertEqual(target.read_bytes(), content)

    def test_invalid_template_fails_before_any_host_changes(self):
        start, end, token = (global_instructions.START, global_instructions.END,
                             global_instructions.TOKEN)
        templates = ['', f'{start}\n{end}', f'{start}\n{token}\n{token}\n{end}',
                     f'{end}\n{start}\n{token}', f'{start}\n{token}\nExtra policy\n{end}']
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            template = root / 'config/AGENTS.md'
            template.parent.mkdir(parents=True)
            home = root / 'home'
            for content in templates:
                with self.subTest(content=content):
                    template.write_text(content)
                    with self.assertRaises(ValueError):
                        global_instructions.sync_instructions(home, home / '.codex', True, root)
                    self.assertFalse(home.exists())

    def test_failed_atomic_replace_preserves_original_and_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            target = home / '.codex/AGENTS.md'
            target.parent.mkdir()
            target.write_text('Existing instructions')
            with patch.object(Path, 'replace', side_effect=OSError('disk failure')):
                with self.assertRaisesRegex(OSError, 'disk failure'):
                    global_instructions.sync_instructions(home, target.parent, True)
            self.assertEqual(target.read_text(), 'Existing instructions')
            backups = list((home / '.local/share/agent-skills/backups').glob('*/AGENTS.md'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), target.read_bytes())
            self.assertEqual(list(target.parent.iterdir()), [target])

    def test_claude_import_is_created_once_and_existing_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            codex_home = home / '.codex'
            preview = global_instructions.link_claude(home, codex_home)
            self.assertTrue(preview['changed'])
            self.assertFalse((home / '.claude').exists())
            global_instructions.link_claude(home, codex_home, apply=True)
            claude = home / '.claude/CLAUDE.md'
            content = claude.read_text()
            self.assertIn(f"@{codex_home / 'AGENTS.md'}", content)
            self.assertTrue(global_instructions.imports_shared(content, codex_home))
            repeated = global_instructions.link_claude(home, codex_home, apply=True)
            self.assertFalse(repeated['changed'])
            self.assertTrue(repeated['imports_shared'])
            claude.write_text('Own Claude instructions')
            kept = global_instructions.link_claude(home, codex_home, apply=True)
            self.assertFalse(kept['changed'])
            self.assertFalse(kept['imports_shared'])
            self.assertEqual(claude.read_text(), 'Own Claude instructions')

    def test_policy_only_skips_claude_file_that_imports_shared_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            self.run_sync(home, '--apply')
            claude = home / '.claude/CLAUDE.md'
            before = claude.read_bytes()
            subprocess.run(
                [sys.executable, str(ROOT / 'scripts/configure_hosts.py'),
                 '--home', str(home), '--policy-only'],
                check=True, capture_output=True, text=True,
            )
            self.assertEqual(claude.read_bytes(), before)
            self.assertNotIn('personal-skill-policy', claude.read_text())


if __name__ == '__main__':
    unittest.main()
