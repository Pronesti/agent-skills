# caveman-help

Quick-reference card. One shot, no mode change.

## What it does

Prints a cheat sheet of the bundled Caveman styles, sibling skills, status, and deactivation triggers. One-shot display — does not flip the active mode, write flag files, or persist anything. Use when you forget the slash commands.

## How to invoke

```
/caveman-help
```

Also triggers on "caveman help", "what caveman commands", "how do I use caveman".

## Example output

```
Modes:
  /caveman              the voice (default)
  /caveman ultra       shorter fragments
  /caveman wenyan      explicitly selected classical Chinese
  /caveman status       report the mode, change nothing

Skills:
  /caveman-commit       terse Conventional Commits
  /caveman-review       one-line PR comments
  /caveman-compress     smaller Markdown memory files
  /caveman-stats        recorded token usage (savings unknown)

Deactivate:
  "stop caveman" or "normal mode"
```

## See also

- [`SKILL.md`](./SKILL.md) — full reference card
- [Caveman README](../../README.md) — repo overview

Modes are task-scoped unless the user requests session-wide behavior. No startup hooks are registered.
