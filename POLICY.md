# Invocation policy

Five personal skills may activate automatically when their trigger fits the authorized task: `caveman:investigate-first`, `caveman:surgical-patch`, `caveman:safe-refactor`, `caveman:verify-and-stop`, and `writing-for-agents`. [invocation-policy.json](invocation-policy.json) owns this allowlist and its triggers. All other personal workflows require explicit user selection.

Selection applies to the requested task; a session-wide mode requires an explicit request. Automatic invocation does not authorize additional work, external actions, commits, or delegation. Use native capabilities when no allowlisted trigger fits.

A selected skill may read its declared supporting references. Other workflow names in a skill, plan, or handoff are suggestions, not activation instructions; each workflow must independently meet its invocation policy. `grill-me` declares the grilling procedure; `grill-with-docs` declares grilling and domain documentation. Neither alias starts planning or implementation.

Project runtime, integration contracts, verification, delivery requirements, and existing user authorization remain mandatory. Keep repository requirements in project instructions and executable checks. Application-required built-in skills follow the host's instructions.

Allowlisted entrypoints set `disable-model-invocation: false` in `SKILL.md` and `policy.allow_implicit_invocation: true` in `agents/openai.yaml`. All other managed entrypoints set those fields to `true` and `false`, respectively. Preserve this selective policy during upstream updates. The Caveman edition registers no startup or prompt hooks.

Install canonical skills through `./install.sh`. Preview migration with `python3 scripts/install.py`. Replaced copies and retired links are retained under `~/.local/share/agent-skills/backups`, outside directories scanned for skills. Codex and Cursor use `~/.agents/skills`; Claude uses links to the same canonical files in `~/.claude/skills`.

Run `python3 scripts/configure_hosts.py --policy-only` to update the managed policy blocks in Codex and Claude without modifying marketplace registration. It generates the automatic rules from the allowlist, preserves text outside the managed blocks, and backs up changed files. Reinstall the local Caveman plugin after changing its source; start a fresh task or restart the host to load the new skill catalog.
