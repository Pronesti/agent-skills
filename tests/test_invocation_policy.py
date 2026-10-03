import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('invocation_policy', ROOT / 'scripts/invocation_policy.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


class InvocationPolicyTests(unittest.TestCase):
    def test_allowlist_rejects_missing_skill_and_duplicate_entries(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            entry = {'name': 'example', 'local_path': 'skills/example', 'trigger': 'Edit an example'}
            config = root / 'invocation-policy.json'
            config.write_text(json.dumps({'automatic_skills': [entry]}))
            with self.assertRaisesRegex(ValueError, 'Invalid automatic skill path'):
                policy.automatic_skills(root)
            skill = root / 'skills/example'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('example')
            self.assertEqual(policy.automatic_skills(root), [entry])
            config.write_text(json.dumps({'automatic_skills': [entry, entry]}))
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                policy.automatic_skills(root)

    def test_host_update_preserves_unmanaged_instructions_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            paths = [home / '.codex/AGENTS.md', home / '.claude/CLAUDE.md']
            old = 'Before\n<!-- personal-skill-policy:start -->\nOld policy\n<!-- personal-skill-policy:end -->\nAfter\n'
            for path in paths:
                path.parent.mkdir(parents=True)
                path.write_text(old)
            command = ['python3', str(ROOT / 'scripts/configure_hosts.py'), '--home', str(home), '--policy-only']
            first = json.loads(subprocess.check_output(command, text=True))
            self.assertIsNotNone(first['backup'])
            for path in paths:
                new = path.read_text()
                self.assertTrue(new.startswith('Before\n'))
                self.assertTrue(new.endswith('\nAfter\n'))
                self.assertIn(policy.host_policy_body(), new)
                self.assertEqual((Path(first['backup']) / path.relative_to(home)).read_text(), old)
            second = json.loads(subprocess.check_output(command, text=True))
            self.assertIsNone(second['backup'])
            self.assertFalse((home / '.agents/plugins/marketplace.json').exists())
            self.assertFalse((home / 'plugins').exists())


if __name__ == '__main__':
    unittest.main()
