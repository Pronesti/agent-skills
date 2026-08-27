# Curated Agent Skills

Single source of truth for cross-agent skills. `install.sh` symlinks each
`skills/<slug>` into every agent's skill directory (Claude Code, Codex, Cursor).

## Upstreams

| Source | Repo | Commit (taken from) | Path in upstream |
|--------|------|---------------------|------------------|
| superpowers | https://github.com/obra/superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | `skills/<slug>` |
| mattpocock | https://github.com/mattpocock/skills | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/<category>/<slug>` |
| pstack | https://github.com/cursor/plugins | `fdf357fae76feff7e5f2e5aaff57f99f644b55f8` | `pstack/skills/<slug>` |

To update a skill: re-clone the upstream, diff its copy against ours since the
recorded commit, merge what you want, keep the local edits below, bump the SHA.

## Skills

**superpowers (8):** brainstorming, executing-plans, finishing-a-development-branch,
requesting-code-review, subagent-driven-development, systematic-debugging,
test-driven-development, writing-plans

**mattpocock (8):** grill-me, grill-with-docs, grilling, research,
resolving-merge-conflicts, wait-what, wizard, writing-for-agents

**pstack (7):** blast-radius, how, recall, show-me-your-work, technical-writing,
unslop, why

Deliberately excluded: superpowers `using-superpowers` (session-wide
self-triggering bootstrap) and `using-git-worktrees` (forced worktrees);
mattpocock issue-tracker suite (competes with the superpowers plan pipeline);
duplicated tdd/debugging/review skills; pstack `poteto-mode` hub and
`principle-*` set.

## Local edits (diff vs upstream)

- **All superpowers skills:** `superpowers:` plugin prefix stripped from
  cross-skill references (installed as bare user skills, the prefix would not
  resolve).
- **brainstorming:** description softened — was "You MUST use this before any
  creative work"; now triggers on explicit brainstorm/design requests.
- **test-driven-development:** description softened — was "any feature or
  bugfix"; now triggers on explicit TDD requests or plan steps. Also removed a
  reference to the excluded `writing-skills` in `writing-good-tests.md`.
- **requesting-code-review:** description softened — now triggers on plan steps
  or explicit review requests.
- **writing-plans / executing-plans / subagent-driven-development:** references
  to `using-git-worktrees` replaced with "isolation optional — ask first, use
  the agent's native worktree option". executing-plans also dropped a pointer
  into the excluded `using-superpowers` references dir.
- **systematic-debugging:** reference to excluded
  `verification-before-completion` replaced with "run the repository's
  verification gate".
- **blast-radius:** dropped naming of the excluded `arena` skill (inline
  multi-model advice kept).
- **how:** dropped comparison to the excluded `interrogate` skill.
