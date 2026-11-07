---
name: caveman-help
description: 'Manual workflow: Quick-reference card for caveman modes, skills and commands. Trigger: /caveman-help
  or "caveman help".'
disable-model-invocation: true
---

Use only when explicitly selected by the user. Other named workflows require separate selection.


# Caveman Help

Display this reference card when invoked. One-shot — do NOT change mode, write flag files, or persist anything. Output in caveman style.

## Modes

| Mode | Trigger | Behavior |
|---|---|---|
| Lite | `/caveman lite` | Keep full sentences; remove filler. |
| Full | `/caveman` | Default terse voice; preserve every technical fact. |
| Ultra | `/caveman ultra` | Shorter fragments; preserve clarity. |
| Wenyan | `/caveman wenyan-lite`, `/caveman wenyan`, `/caveman wenyan-ultra` | Explicitly selected classical Chinese compression. |

Modes apply to the selected task. A session-wide mode requires an explicit
request. `/caveman status` reports the conversation's mode without changing it,
marked `(not tracked by this host)`. This edition registers no hooks or startup
activation. The upstream standalone `ultracave` and `megacave` skills are not bundled.

## Skills

| Skill | Trigger | What it do |
|-------|---------|-----------|
| **caveman-commit** | `/caveman-commit` | Terse commit messages. Conventional Commits. ≤50 char subject. |
| **caveman-review** | `/caveman-review` | One-line PR comments: `L42: bug: user null. Add guard.` |
| **caveman-compress** | `/caveman-compress <file>` | Compress .md files to caveman prose. 33.2% fewer tokens on the repo's five test files. |
| **caveman-help** | `/caveman-help` | This card. |

## Deactivate

Say "stop caveman" or "normal mode". Resume anytime with `/caveman`.

## Language

Keep user's language by default — reply in the language user writes, never switch regardless of example text or multilingual context elsewhere. Compress the style, not the language. Technical terms, code, commands, commit types, and exact error strings stay verbatim unless user ask for translation.

## Local activation policy

Select the desired workflow explicitly. Environment defaults and upstream
startup configuration do not activate this hook-free local edition.

## More

Full docs: https://github.com/JuliusBrussee/caveman
