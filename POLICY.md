# Invocation policy

Seven personal skills may activate automatically when their trigger fits the authorized task: `caveman:investigate-first`, `caveman:surgical-patch`, `caveman:safe-refactor`, `caveman:verify-and-stop`, `writing-for-agents`, `pr`, and `write-pr-description`. [invocation-policy.json](invocation-policy.json) owns this allowlist and its triggers. The two PR skills apply only at an authorized title/body drafting stage for a specific PR or change set. General review, coding, research, and template/skill editing do not trigger them. Their shared [activation check](skills/pr/references/authoring-scope.md) defines target resolution, one drafting pass, and format precedence. All other personal workflows require explicit user selection.

Selection applies to the requested task; a session-wide mode requires an explicit request. Automatic invocation does not authorize additional work, external actions, commits, or delegation. Use native capabilities when no allowlisted trigger fits.

A selected skill may read its declared supporting references. Other workflow names in a skill, plan, or handoff are suggestions, not activation instructions; each workflow must independently meet its invocation policy. `grill-me` declares the grilling procedure; `grill-with-docs` declares grilling and domain documentation. Neither alias starts planning or implementation.

Project runtime, integration contracts, verification, delivery requirements, and existing user authorization remain mandatory. Keep repository requirements in project instructions and executable checks. Application-required built-in skills follow the host's instructions.

Allowlisted entrypoints set `disable-model-invocation: false` in `SKILL.md` and `policy.allow_implicit_invocation: true` in `agents/openai.yaml`. All other managed entrypoints set those fields to `true` and `false`, respectively. Preserve this selective policy during upstream updates. The Caveman edition registers no startup or prompt hooks.

## Applying the policy

`./install.sh` links the skills and preserves existing global instructions; only `--sync-agents` replaces them. `python3 scripts/configure_hosts.py --policy-only` regenerates the managed policy blocks from the allowlist, preserving text outside them; it skips a `CLAUDE.md` that imports the shared instructions, and installs the full shared template where no global instructions exist. Start a fresh task after changing discovery. Commands, backups, and runtime profiles are covered in the [installation guide](MANIFEST.md#installation) and the [shared instructions guide](MANIFEST.md#share-global-instructions-across-hosts-computers-and-vms).

## Rationale

The commits below record what changed; the reasons are what the enforced checks protect.

- **Selective invocation.** The catalog holds 74 skills from about 19 authors, several of which overlap on purpose (`tdd` and `test-driven-development`). Upstream skills also chained into one another and set session-wide modes, which `validate.py` now rejects. Every skill became manual-only in `8501543` (2026-09-19); five narrow ones were allowed to start automatically in `54b9646` (2026-10-03), and the two PR-authoring skills joined them in `ebc5833` (2026-10-14), each scoped to a trigger in [invocation-policy.json](invocation-policy.json).
- **Caveman without hooks.** Startup and prompt hooks would apply the Caveman mode to every session. The local edition keeps the workflows and drops hook registration, which `validate.py` enforces for both plugin manifests.
- **Vendored skills at pinned revisions.** A local copy keeps the invocation overlay and local fixes across updates, retains skills that upstream removed, and stops package-manager updates from overwriting them. [upstreams.json](upstreams.json) pins each source, and `check_updates.py` only reports, so every merge is reviewed.
- **One shared instructions file.** [config/AGENTS.md](config/AGENTS.md) installs to `~/.codex/AGENTS.md`, and `~/.claude/CLAUDE.md` imports it (`a9258e0`), so Codex, Claude Code, and tools that write into that file stay in step.
- **Machine runtime profile.** PHP and Composer run differently per machine (lerd on one, direct access on another), so the command forms live in `~/.config/agent-skills/runtime.md` and the shared instructions stay identical everywhere (`af18db6`).
