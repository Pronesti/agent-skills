import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


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
            preview = installer.install(home)
            self.assertFalse(existing.is_symlink())
            self.assertTrue(preview["actions"])
            result = installer.install(home, True)
            self.assertEqual(existing.resolve(), installer.REPO / "skills/grilling")
            self.assertFalse(old.is_symlink())
            self.assertEqual((Path(result["backup"]) / ".agents/skills/grilling/SKILL.md").read_text(), "local customization")
            self.assertIn("unrelated", json.loads(lock.read_text())["skills"])
            self.assertNotIn("grilling", json.loads(lock.read_text())["skills"])
            self.assertEqual(installer.install(home, True)["actions"], [])

    def test_unmanaged_collision_changes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            collision = home / ".claude/skills/writing-plans"
            collision.mkdir(parents=True)
            (collision / "SKILL.md").write_text("unrelated installation")
            with self.assertRaisesRegex(RuntimeError, "Unmanaged collision"):
                installer.install(home, True)
            self.assertFalse((home / ".agents/skills").exists())
            self.assertEqual((collision / "SKILL.md").read_text(), "unrelated installation")


if __name__ == "__main__":
    unittest.main()
