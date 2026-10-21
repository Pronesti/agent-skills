---
name: maintain-verification-skill
description: 'Periodic pass that keeps a project''s verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at most one PR of proven corrections. Use for /maintain-verification-skill or "audit the verify skill".'
disable-model-invocation: true
---

# maintain-verification-skill

Use only when explicitly selected. Apply this workflow to the authorized task.
Resolve this entrypoint's symlink to its canonical directory before following relative paths.

1. In Codex, read [the Codex harness adapter](../../pstack/docs/harness/codex.md).
   In Claude Code, read [the Claude harness adapter](../../pstack/docs/harness/claude-code.md).
   In Cursor, use the upstream tool names. Apply the repository's invocation policy in every host.
2. Read [the complete upstream workflow](../../pstack/skills/maintain-verification-skill/SKILL.md),
   then follow it using that adapter. Resolve its references relative to the upstream file.

The adapter applies to the workflow and all resources it reaches. A selected workflow
may read its declared supporting resources within scope; naming another workflow
does not independently authorize additional work, external actions, or a session-wide mode.
