#!/usr/bin/env python3
"""Install canonical skill links; back up replaced copies outside discovery roots."""
import argparse
import datetime
import json
from pathlib import Path
import shutil

REPO = Path(__file__).resolve().parents[1]


def install(home, apply=False):
    source = REPO / "skills"
    skills = sorted(p for p in source.iterdir() if (p / "SKILL.md").is_file())
    lock_path = home / ".agents/.skill-lock.json"
    lock = json.loads(lock_path.read_text()) if lock_path.exists() else {}
    owned = {name for name, data in lock.get("skills", {}).items()
             if data.get("source") in ("mattpocock/skills", "vercel-labs/skills")}
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = home / ".local/share/agent-skills/backups" / stamp
    actions = []

    def save(path):
        dest = backup / path.relative_to(home)
        if apply:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(dest))
        actions.append(f"backup {path} -> {dest}")

    for target_root in (home / ".agents/skills", home / ".claude/skills"):
        for skill in skills:
            target = target_root / skill.name
            if target.is_symlink() and target.resolve() == skill.resolve():
                continue
            if target.exists() or target.is_symlink():
                if not (target_root == home / ".agents/skills" and skill.name in owned):
                    raise RuntimeError(f"Unmanaged collision at {target}; left untouched")

    for target_root in (home / ".agents/skills", home / ".claude/skills"):
        for skill in skills:
            target = target_root / skill.name
            if target.is_symlink() and target.resolve() == skill.resolve():
                continue
            if target.exists() or target.is_symlink():
                save(target)
            if apply:
                target_root.mkdir(parents=True, exist_ok=True)
                target.symlink_to(skill, target_is_directory=True)
            actions.append(f"link {target} -> {skill}")

    for target_root in (home / ".codex/skills", home / ".cursor/skills-cursor", home / ".cursor/skills"):
        if not target_root.exists():
            continue
        for target in target_root.iterdir():
            if target.is_symlink() and target.readlink().parent == source:
                save(target)

    migrated = owned.intersection(p.name for p in skills)
    if migrated:
        if apply:
            dest = backup / lock_path.relative_to(home)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(lock_path, dest)
            for name in migrated:
                del lock["skills"][name]
            lock_path.write_text(json.dumps(lock, indent=2) + "\n")
        actions.append(f"retire {len(migrated)} old package-manager ownership records")
    return {"applied": apply, "skills": len(skills), "backup": str(backup) if actions else None,
            "actions": actions}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="Installation root; use a scratch root for tests")
    parser.add_argument("--apply", action="store_true", help="Without this flag, preview only")
    args = parser.parse_args()
    print(json.dumps(install(args.home.resolve(), args.apply), indent=2))
