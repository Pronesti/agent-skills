#!/usr/bin/env python3
"""Install skills, shared Codex instructions, and a local runtime profile with backups."""
import argparse
import datetime
import json
from pathlib import Path
import shutil
import subprocess
from functools import lru_cache

from runtime_profile import apply_runtime, plan_runtime
from codex_instructions import resolve_codex_home, sync_instructions
from codex_native import native_agent_plan, apply_agent_plan

REPO = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=None)
def git_common_dir(root):
    """Identify this repository across its managed worktrees, without using remotes."""
    try:
        result = subprocess.run(
            ['git', '-C', str(root), 'rev-parse', '--show-toplevel', '--git-common-dir'],
            capture_output=True, text=True, check=True, timeout=5,
        ).stdout.splitlines()
        top, common = result
        if Path(top).resolve() != root.resolve():
            return None
        return (root / common).resolve()
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def managed_link(target):
    """Recognize only direct skill links into this checkout or a sibling worktree."""
    if not target.is_symlink():
        return False
    destination = (target.parent / target.readlink()).absolute()
    if destination.name != target.name:
        return False
    for relative in ('skills', 'plugins/caveman/skills'):
        parts = Path(relative).parts
        if tuple(destination.parent.parts[-len(parts):]) != parts:
            continue
        root = destination.parents[len(parts)]
        if root.resolve() == REPO.resolve():
            return True
        common = git_common_dir(root)
        if common is not None and common == git_common_dir(REPO):
            return True
    return False


def install(home, apply=False, runtime='auto', refresh_runtime=False, codex_home=None):
    runtime_plan = plan_runtime(home, runtime, refresh_runtime)
    codex_home = resolve_codex_home(home, codex_home)
    codex_result = sync_instructions(home, codex_home, root=REPO)
    native_plan = native_agent_plan(home, codex_home, root=REPO)
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
                if not managed_link(target) and not (target_root == home / ".agents/skills" and skill.name in owned):
                    raise RuntimeError(f"Unmanaged collision at {target}; left untouched")

    if apply:
        codex_result = sync_instructions(home, codex_home, apply=True, root=REPO)
    codex_actions = []
    if codex_result['changed']:
        if codex_result['backup']:
            codex_actions.append(f"backup {codex_result['target']} -> {codex_result['backup']}")
        codex_actions.append(f"write {codex_result['target']} (shared Codex instructions)")

    for target_root in (home / ".agents/skills", home / ".claude/skills"):
        if target_root.exists():
            current_names = {skill.name for skill in skills}
            for target in sorted(target_root.iterdir()):
                if target.name not in current_names and managed_link(target):
                    save(target)
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
            if managed_link(target):
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
    runtime_result = apply_runtime(runtime_plan, backup) if apply else runtime_plan
    native_result = apply_agent_plan(native_plan, home, backup, apply)
    actions.extend(native_result['actions'])
    if runtime_result['status'] in ('planned', 'written'):
        if runtime_result['backup']:
            actions.append(f"backup {runtime_result['target']} -> {runtime_result['backup']}")
        actions.append(f"write {runtime_result['target']} ({runtime_result['selected']})")
    return {"applied": apply, "skills": len(skills), "backup": str(backup) if actions else None,
            "actions": codex_actions + actions, "runtime": runtime_result,
            "codex_agents": codex_result, "native_agents": native_result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, help="Installation root; explicit scratch roots isolate Codex from CODEX_HOME")
    parser.add_argument("--codex-home", type=Path, help="Codex directory; overrides --home and CODEX_HOME")
    parser.add_argument("--apply", action="store_true", help="Without this flag, preview only")
    parser.add_argument("--runtime", choices=('auto', 'lerd', 'direct', 'skip'), default='auto',
                        help="Runtime selection for a missing profile (default: auto); existing profiles are preserved")
    parser.add_argument("--refresh-runtime", action='store_true',
                        help="Regenerate an existing runtime profile, backing it up on apply")
    args = parser.parse_args()
    if args.refresh_runtime and args.runtime == 'skip':
        parser.error('--refresh-runtime cannot be combined with --runtime skip')
    try:
        home = (args.home or Path.home()).expanduser().resolve()
        codex_home = resolve_codex_home(args.home, args.codex_home)
        result = install(home, args.apply, args.runtime, args.refresh_runtime, codex_home)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f'Installation: {exc}\n')
    print(json.dumps(result, indent=2))
