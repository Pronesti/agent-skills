# Curated Agent Skills

This repository owns **47 standalone skills and a 20-skill Caveman edition**. Five focused skills allow automatic invocation; the other 62 personal workflows require explicit user selection. See [POLICY.md](POLICY.md) for invocation boundaries.

Read the [workflow guide](WORKFLOW-GUIDE.md) for 56 scenarios in ASD-STE100 English. The guide covers all 67 workflows, their sequences, and combinations with different instructions.

## Author revisions

Pinned author revisions were recorded on 19 September 2026. All 63 skill directories were checked again on 3 October 2026: 40 unchanged, 22 with upstream changes available, and one absent from its recorded upstream path. The check is recorded in `reports/2026-10-03-skill-updates/upstream-check.json`; it does not replace the pinned content. Full revisions, upstream paths, and local destinations are pinned in [upstreams.json](upstreams.json). A newer repository revision does not necessarily change every selected skill.

The wshobson, addyosmani, severity1, and vercel-agent-browser sources were added on 7 October 2026 at the revisions below. These are local forks with the same selective invocation overlay; their upstream repositories remain the reference for future updates.

| Source | Original repository | Pinned revision | Skills |
|---|---|---|---:|
| superpowers | [obra/superpowers](https://github.com/obra/superpowers) | `5bf4e78011075bcfc0dc295f0724994cd123ee71` | 8 |
| mattpocock | [mattpocock/skills](https://github.com/mattpocock/skills) | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | 24 |
| pstack | [cursor/plugins](https://github.com/cursor/plugins) | `032be146865d973682535de75f2287da438550bf` | 7 |
| ponytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` | 1 |
| humanlayer | [humanlayer/skills](https://github.com/humanlayer/skills) | `ca7c8088db69e315a8b2deea43820270457f8f3c` | 1 |
| vercel | [vercel-labs/skills](https://github.com/vercel-labs/skills) | `7407f3893ad4dceab546ac002c3ef806e4000c73` | 1 |
| caveman | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `542442bab314973709f95b85b1ac0b3f6f5b5dc6` | 20 |
| wshobson | [wshobson/agents](https://github.com/wshobson/agents) | `46891e7e60da0e52baf1050b7b6391b64e84c6d9` | 1 |
| addyosmani | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | `1401c8b8030e023baeebb31781a6653fe8e93026` | 2 |
| severity1 | [severity1/claude-code-prompt-improver](https://github.com/severity1/claude-code-prompt-improver) | `50aae187bb4f08b852f318234b654df3332726a4` | 1 |
| vercel-agent-browser | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | `f7c8b071343dda29477a56cb336ea76144c05496` | 1 |

Architecture Patterns includes its upstream `references/details.md` and `references/advanced-patterns.md`. Incremental Implementation bundles the upstream shared `references/definition-of-done.md` inside its own reference directory; `upstreams.json` records that additional source-to-local mapping. Commit and delivery instructions in the Addy forks honor existing authorization and project requirements. Other workflow names remain optional, separately selected choices.

Prompt Improver adapts severity1's research-first workflow into a manually invoked research and execution handoff. One light subagent answers investigation questions from code and supplied conversation history, checks existing behavior and reuse targets, and returns a scoped prompt. The main agent displays that prompt and executes it without an extra approval round; unresolved user decisions are clarified first. Local supporting references cover the subagent assignment and complete, partial, missing, and inaccessible implementations. No upstream plugin or automatic hooks are included; the local adaptations are recorded in `upstreams.json`.

Manual QA preserves Vercel's exploratory QA guidance, issue checklist, and adapted report template. It uses native Codex Computer Use, resolves URL/sign-in/scope from user context, plans and tracks every case, continues independent cases after failures, and reports incomplete coverage. The source revision, original file paths, renamed destinations, and local changes are recorded in `upstreams.json`. It has no separate browser CLI or plugin dependency.

## Functional groups

Skill picker labels use 18 functional prefixes, each grouping 3–5 skills by their main purpose. All 67 skills are assigned exactly once. Invocation names and installation paths are preserved. See the [complete grouping](reports/skill-groups.md).

## Catalog

**superpowers:** `brainstorming`, `executing-plans`, `finishing-a-development-branch`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `writing-plans`.

**mattpocock:** `grill-me`, `grill-with-docs`, `grilling`, `research`, `resolving-merge-conflicts`, `wait-what`, `wizard`, `writing-for-agents`, `code-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `handoff`, `implement`, `improve-codebase-architecture`, `prototype`, `setup-matt-pocock-skills`, `tdd`, `teach`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`, `wayfinder`.

**pstack:** `blast-radius`, `how`, `recall`, `show-me-your-work`, `technical-writing`, `unslop`, `why`.

**ponytail:** `ponytail`.

**humanlayer:** `show-me`.

**vercel:** `find-skills`.

**wshobson:** `architecture-patterns`.

**addyosmani:** `code-simplification`, `incremental-implementation`.

**severity1:** `prompt-improver`.

**vercel-agent-browser:** `manual-qa`.

**caveman:** `caveman:cavecrew`, `caveman:caveman`, `caveman:caveman-commit`, `caveman:caveman-compress`, `caveman:caveman-discover`, `caveman:caveman-evidence-review`, `caveman:caveman-explore`, `caveman:caveman-help`, `caveman:caveman-learn`, `caveman:caveman-manage`, `caveman:caveman-optimize`, `caveman:caveman-review`, `caveman:caveman-setup`, `caveman:caveman-stats`, `caveman:investigate-first`, `caveman:lean-build`, `caveman:migration`, `caveman:safe-refactor`, `caveman:surgical-patch`, `caveman:verify-and-stop`.

## Installation

Run `python3 scripts/install.py` to preview, then `./install.sh` to apply. The installer keeps one canonical directory per standalone skill under this repository, links it through `~/.agents/skills` and `~/.claude/skills`, and retires repository-owned aliases under `~/.codex/skills` and `~/.cursor/skills-cursor`. It refuses unmanaged name collisions and backs up replaced copies outside discovery roots. Re-running it is a no-op.

For the local Caveman edition and the personal instruction block:

```sh
python3 scripts/configure_hosts.py
codex plugin add caveman@personal
claude plugin marketplace add ./plugins
claude plugin install caveman@personal-manual
claude plugin disable caveman@caveman
```

Disable the original `caveman@caveman` entry in Codex plugin settings as well; leave `caveman@personal` enabled. Do not delete upstream caches. Start a fresh task after changing discovery, and restart Claude Code to unload previously registered hooks. Application-managed built-in and specialist plugins remain owned by their host.

## Local policy overlay

- [invocation-policy.json](invocation-policy.json) owns the five automatic skills and their triggers. Their entrypoints set `disable-model-invocation: false` and `policy.allow_implicit_invocation: true`. The other 62 entrypoints keep the opposite settings. Both fields must agree with the allowlist.
- Selection applies to one task. Session-wide modes need an explicit request. Always-on style mandates, forced workflow transitions, and automatic activation from generated plans or handoffs are removed or made optional.
- Supporting files are still readable. `grill-me` declares the grilling procedure; `grill-with-docs` declares grilling and domain documentation.
- Project runtime, verification, delivery requirements, and existing user authorization take precedence. Superpowers namespace references are adapted for standalone installation; optional isolation uses host facilities.
- Caveman preserves its 20 workflow names, reviewer presets, and manual stats helper, with four focused automatic workflows and no startup/prompt hook registration. The original plugin is disabled rather than deleted. The stats helper cannot reconstruct mode attribution that was never recorded.
- Duplicate installations are consolidated by name. Distinct alternative workflows such as `tdd` and `test-driven-development` remain separate, manually selected choices.

## Updating without losing the policy

Run `python3 scripts/check_updates.py` to compare the pinned revisions with the authors’ default branches. It reports only; it never replaces skills. Merge changed skill files against the recorded base, preserve the selective invocation overlay, update `upstreams.json`, and review executable helpers. For Caveman, bump the local plugin version and reinstall through each host after editing the source. Do not edit versioned plugin caches.

Validate metadata and references with `python3 scripts/validate.py` (requires `pip install -r scripts/requirements.txt` in your chosen environment). Run `python3 -m unittest discover -s tests -v` for installer behavior. Verify that all personal skills remain available for explicit selection, only the allowlisted skills appear in automatic discovery, and each automatic trigger stays within the authorized task. Start a fresh task after changing discovery.

Third-party licenses are preserved in [licenses/](licenses/). Excluded upstream bundles, bootstrap skills, and hooks are not installed by this repository.
