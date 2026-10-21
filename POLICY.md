# Invocation policy

The personal catalog contains only pstack. Every public entrypoint requires
explicit selection. [invocation-policy.json](invocation-policy.json) retains the
allowlist mechanism with an empty list; entrypoints set
`disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.

Selection applies to the requested task. A session-wide mode needs an explicit
request. A selected workflow reads its host adapter and unmodified upstream
instructions. It may read declared supporting procedures and principles within
scope. Merely naming another workflow does not authorize independent work.
Existing user and project requirements govern runtime, verification, delegation,
external actions, delivery, and memory. An upstream autonomy statement does not
supply missing authorization.

[config/codex/AGENTS.md](config/codex/AGENTS.md) remains the shared template. Its
managed policy section is rendered from the current allowlist; the rest of the
template is unchanged. Installation syncs the complete instructions with a backup
and preserves existing runtime profiles. `--policy-only` updates managed blocks
in Codex and Claude while preserving other text. `--sync-codex-agents` previews
the complete shared file; add `--apply` to replace it with a backup.

Run `python3 scripts/install.py` to preview and `./install.sh` to apply. The
installer preserves unmanaged skills and backs up retired repository links. It
also installs native Codex agent files with ownership checks, backups, and
validated saved model roles. Native agents inherit permissions and provider;
their availability does not authorize unsolicited delegation.
It leaves plugin caches and marketplace registrations alone; disable an old
Caveman plugin through its host when migrating a live machine. See the
[installation guide](MANIFEST.md#installation) for isolation, runtime choices,
custom Codex directories, and updates. No live installation is part of this task.
