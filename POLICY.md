# Invocation policy

Personal workflow skills run only when explicitly selected by the user. Selection applies to the requested task; a session-wide mode requires an explicit request. Ordinary coding, debugging, planning, review, and writing continue using native capabilities.

A selected skill may read its declared supporting references. Other workflow names in a skill, plan, or handoff are suggestions for the user, not instructions to activate them. `grill-me` declares the grilling procedure; `grill-with-docs` declares grilling and domain documentation. Neither alias starts planning or implementation.

Project runtime, integration contracts, verification, and delivery requirements remain mandatory. Keep these requirements in project instructions and executable repository checks. Application-required built-in skills follow the host's instructions.

All managed skill entrypoints set both `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Preserve both settings during upstream updates. The Caveman edition in this repository registers no startup or prompt hooks.

Install canonical skills through `./install.sh`. Preview migration with `python3 scripts/install.py`. Replaced copies and retired links are retained under `~/.local/share/agent-skills/backups`, outside directories scanned for skills. Codex and Cursor use `~/.agents/skills`; Claude uses links to the same canonical files in `~/.claude/skills`.
