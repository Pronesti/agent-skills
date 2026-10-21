---
name: show-me-your-work
description: 'Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for /show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away.'
disable-model-invocation: true
---

# show-me-your-work

Use only when explicitly selected. Apply this workflow to the authorized task.
Resolve this entrypoint's symlink to its canonical directory before following relative paths.

1. In Codex, read [the Codex harness adapter](../../pstack/docs/harness/codex.md).
   In Claude Code, read [the Claude harness adapter](../../pstack/docs/harness/claude-code.md).
   In Cursor, use the upstream tool names. Apply the repository's invocation policy in every host.
2. Read [the complete upstream workflow](../../pstack/skills/show-me-your-work/SKILL.md),
   then follow it using that adapter. Resolve its references relative to the upstream file.

The adapter applies to the workflow and all resources it reaches. A selected workflow
may read its declared supporting resources within scope; naming another workflow
does not independently authorize additional work, external actions, or a session-wide mode.
