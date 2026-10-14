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
import runtime_profile
import install as installer
sys.path.pop(0)


class RuntimeDetectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.home = self.root / 'home'
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.target = self.home / '.config/agent-skills/runtime.md'
        environment = patch.dict(os.environ, {'PATH': str(self.bin)})
        environment.start()
        self.addCleanup(environment.stop)

    def executable(self, name):
        path = self.bin / name
        path.write_text('#!/bin/sh\nexit 99\n')
        path.chmod(0o755)
        return path

    def yerd_shims(self):
        launcher = self.root / 'Yerd.app/Contents/MacOS/yerd'
        launcher.parent.mkdir(parents=True)
        launcher.write_text('#!/bin/sh\nexit 99\n')
        launcher.chmod(0o755)
        for name in ('yerd', 'php', 'composer'):
            (self.bin / name).symlink_to(launcher)
        return launcher

    def existing_profile(self, content='Handwritten runtime instructions\n'):
        self.target.parent.mkdir(parents=True)
        self.target.write_text(content)

    def test_lerd_preview_and_apply_then_repeat_preserves_profile(self):
        self.executable('lerd')
        preview = installer.install(self.home)
        self.assertFalse(self.home.exists())
        self.assertEqual(preview['runtime']['selected'], 'lerd')
        self.assertEqual(preview['runtime']['status'], 'planned')
        self.assertIn('`lerd php ...`', preview['runtime']['content'])
        applied = installer.install(self.home, apply=True)
        self.assertEqual(applied['runtime']['status'], 'written')
        self.assertIn('`lerd composer ...`', self.target.read_text())
        before = self.target.stat()
        repeated = installer.install(self.home, apply=True)
        self.assertEqual(repeated['runtime']['status'], 'preserved')
        self.assertEqual(repeated['actions'], [])
        self.assertEqual(self.target.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertIsNone(repeated['runtime']['backup'])

    def test_yerd_shims_select_direct_commands_and_record_evidence(self):
        launcher = self.yerd_shims()
        result = installer.install(self.home, apply=True)
        runtime = result['runtime']
        self.assertEqual(runtime['selected'], 'direct')
        self.assertEqual(runtime['executables']['php']['resolved'], str(launcher))
        self.assertIn('`php ...`', self.target.read_text())
        self.assertIn('`composer ...`', self.target.read_text())
        self.assertNotIn('lerd php', self.target.read_text())

    def test_yerd_shims_are_recognized_without_yerd_on_path(self):
        self.yerd_shims()
        (self.bin / 'yerd').unlink()
        plan = runtime_profile.plan_runtime(self.home)
        self.assertEqual(plan['selected'], 'direct')

    def test_both_runtimes_are_ambiguous_but_explicit_choice_works(self):
        self.yerd_shims()
        self.executable('lerd')
        result = installer.install(self.home, apply=True)
        self.assertEqual(result['runtime']['status'], 'ambiguous')
        self.assertFalse(self.target.exists())
        self.assertTrue((self.home / '.agents/skills/grilling').is_symlink())
        for choice in ('lerd', 'direct'):
            plan = runtime_profile.plan_runtime(self.home, runtime=choice)
            self.assertEqual(plan['selected'], choice)
            self.assertEqual(plan['status'], 'planned')

    def test_yerd_installed_with_unrelated_or_mixed_tools_is_not_direct(self):
        self.executable('yerd')
        self.executable('php')
        self.executable('composer')
        self.assertEqual(runtime_profile.plan_runtime(self.home)['status'], 'unavailable')
        (self.bin / 'php').unlink()
        (self.bin / 'php').symlink_to(self.bin / 'yerd')
        self.assertEqual(runtime_profile.plan_runtime(self.home)['status'], 'unavailable')

    def test_native_tools_need_explicit_direct_selection(self):
        self.executable('php')
        self.executable('composer')
        self.assertEqual(runtime_profile.plan_runtime(self.home)['status'], 'unavailable')
        explicit = runtime_profile.plan_runtime(self.home, runtime='direct')
        self.assertEqual(explicit['selected'], 'direct')
        self.assertEqual(explicit['status'], 'planned')

    def test_missing_tools_leave_profile_unwritten(self):
        for choice in ('auto', 'lerd', 'direct'):
            plan = runtime_profile.plan_runtime(self.home, runtime=choice)
            self.assertEqual(plan['status'], 'unavailable')
            self.assertIsNone(plan['content'])
        self.executable('php')
        self.assertEqual(runtime_profile.plan_runtime(self.home, runtime='direct')['status'], 'unavailable')
        result = installer.install(self.home, apply=True)
        self.assertEqual(result['runtime']['status'], 'unavailable')
        self.assertFalse(self.target.exists())

    def test_non_executable_and_broken_symlink_are_not_detected(self):
        (self.bin / 'lerd').write_text('not executable')
        (self.bin / 'php').symlink_to(self.root / 'missing')
        self.assertEqual(runtime_profile.plan_runtime(self.home)['status'], 'unavailable')

    def test_existing_profile_is_preserved_without_detection(self):
        self.existing_profile()
        before = self.target.read_bytes()
        with patch.object(runtime_profile, 'detect_runtime', side_effect=AssertionError('must not detect')):
            result = installer.install(self.home, apply=True, runtime='lerd')
        self.assertEqual(result['runtime']['status'], 'preserved')
        self.assertEqual(self.target.read_bytes(), before)

    def test_refresh_preview_backup_replacement_and_no_op(self):
        self.yerd_shims()
        self.existing_profile('Use lerd php and lerd composer.\n')
        self.target.chmod(0o600)
        old = self.target.read_bytes()
        preview = installer.install(self.home, refresh_runtime=True)
        self.assertEqual(preview['runtime']['selected'], 'direct')
        self.assertEqual(self.target.read_bytes(), old)
        self.assertFalse((self.home / '.local').exists())
        result = installer.install(self.home, apply=True, refresh_runtime=True)
        self.assertEqual(Path(result['runtime']['backup']).read_bytes(), old)
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o600)
        before = self.target.stat()
        repeated = installer.install(self.home, apply=True, refresh_runtime=True)
        self.assertEqual(repeated['runtime']['status'], 'unchanged')
        self.assertEqual(repeated['actions'], [])
        self.assertIsNone(repeated['runtime']['backup'])
        self.assertEqual(self.target.stat().st_mtime_ns, before.st_mtime_ns)

    def test_unsuccessful_refresh_preserves_existing_content(self):
        self.existing_profile()
        before = self.target.read_bytes()
        result = installer.install(self.home, apply=True, refresh_runtime=True)
        self.assertEqual(result['runtime']['status'], 'unavailable')
        self.assertEqual(self.target.read_bytes(), before)
        self.assertIsNone(result['runtime']['backup'])

    def test_skip_bypasses_detection_and_refresh_with_skip_is_rejected(self):
        with patch.object(runtime_profile, 'detect_runtime', side_effect=AssertionError('must not detect')):
            result = installer.install(self.home, apply=True, runtime='skip')
        self.assertEqual(result['runtime']['status'], 'skipped')
        self.assertFalse(self.target.exists())
        with self.assertRaises(ValueError):
            runtime_profile.plan_runtime(self.home, runtime='skip', refresh=True)

    def test_symlink_is_preserved_and_refresh_refused_before_skill_changes(self):
        source = self.root / 'custom-runtime.md'
        source.write_text('Custom runtime')
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(source)
        plan = runtime_profile.plan_runtime(self.home)
        self.assertEqual(plan['status'], 'preserved')
        for broken in (False, True):
            if broken:
                source.unlink()
            with self.assertRaisesRegex(RuntimeError, 'symlink'):
                installer.install(self.home, apply=True, refresh_runtime=True)
            self.assertTrue(self.target.is_symlink())
            self.assertFalse((self.home / '.agents').exists())

    def test_skill_collision_prevents_runtime_creation(self):
        self.executable('lerd')
        collision = self.home / '.claude/skills/writing-plans'
        collision.mkdir(parents=True)
        with self.assertRaisesRegex(RuntimeError, 'Unmanaged collision'):
            installer.install(self.home, apply=True)
        self.assertFalse(self.target.exists())

    def test_runtime_directory_collision_fails_before_skill_changes(self):
        self.target.mkdir(parents=True)
        with self.assertRaisesRegex(RuntimeError, 'regular file'):
            installer.install(self.home, apply=True)
        self.assertTrue(self.target.is_dir())
        self.assertFalse((self.home / '.agents').exists())

    def test_failed_refresh_preserves_original_and_backup(self):
        self.executable('lerd')
        self.existing_profile()
        old = self.target.read_bytes()
        plan = runtime_profile.plan_runtime(self.home, refresh=True)
        backup = self.root / 'backups'
        with patch.object(Path, 'replace', side_effect=OSError('disk failure')):
            with self.assertRaisesRegex(OSError, 'disk failure'):
                runtime_profile.apply_runtime(plan, backup)
        self.assertEqual(self.target.read_bytes(), old)
        self.assertEqual((backup / '.config/agent-skills/runtime.md').read_bytes(), old)
        self.assertEqual(list(self.target.parent.iterdir()), [self.target])

    def test_profile_created_during_apply_is_preserved(self):
        self.executable('lerd')
        plan = runtime_profile.plan_runtime(self.home)
        link = os.link

        def competing_creation(source, target):
            target.write_text('Concurrent handwritten instructions')
            return link(source, target)

        with patch.object(runtime_profile.os, 'link', side_effect=competing_creation):
            result = runtime_profile.apply_runtime(plan, self.root / 'backups')
        self.assertEqual(result['status'], 'preserved')
        self.assertEqual(self.target.read_text(), 'Concurrent handwritten instructions')
        self.assertEqual(list(self.target.parent.iterdir()), [self.target])

    def test_cli_flags_and_shell_installer(self):
        self.executable('lerd')
        (self.bin / 'python3').symlink_to(sys.executable)
        preview = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/install.py'), '--home', str(self.home), '--runtime', 'lerd'],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(preview.stdout)['runtime']['status'], 'planned')
        self.assertFalse(self.home.exists())
        # The shell entrypoint needs dirname as well as Python on PATH.
        (self.bin / 'dirname').symlink_to('/usr/bin/dirname')
        applied = subprocess.run(
            ['/bin/bash', str(ROOT / 'install.sh'), '--home', str(self.home), '--runtime', 'lerd'],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(applied.stdout)['runtime']['status'], 'written')
        invalid_home = self.root / 'invalid-home'
        invalid = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/install.py'), '--home', str(invalid_home),
             '--runtime', 'skip', '--refresh-runtime', '--apply'], capture_output=True, text=True,
        )
        self.assertNotEqual(invalid.returncode, 0)
        self.assertFalse(invalid_home.exists())


if __name__ == '__main__':
    unittest.main()
