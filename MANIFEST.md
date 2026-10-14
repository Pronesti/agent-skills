# Curated Agent Skills

This repository owns **51 standalone skills and a 20-skill Caveman edition**. Seven focused skills allow automatic invocation; the other 64 personal workflows require explicit user selection. See [POLICY.md](POLICY.md) for invocation boundaries.

Read the [workflow guide](WORKFLOW-GUIDE.md) for 56 scenarios in ASD-STE100 English. The guide covers all 71 workflows, their sequences, and combinations with different instructions.

## Author revisions

Pinned author revisions were recorded on 19 September 2026. All 63 skill directories were checked again on 3 October 2026: 40 unchanged, 22 with upstream changes available, and one absent from its recorded upstream path. The check is recorded in `reports/2026-10-03-skill-updates/upstream-check.json`; it does not replace the pinned content. Full revisions, upstream paths, and local destinations are pinned in [upstreams.json](upstreams.json). A newer repository revision does not necessarily change every selected skill.

The wshobson, addyosmani, severity1, and vercel-agent-browser sources were added on 7 October 2026 at the revisions below. These are local forks with the same selective invocation overlay; their upstream repositories remain the reference for future updates.

| Source | Original repository | Pinned revision | Skills |
|---|---|---|---:|
| superpowers | [obra/superpowers](https://github.com/obra/superpowers) | `5bf4e78011075bcfc0dc295f0724994cd123ee71` | 8 |
| mattpocock | [mattpocock/skills](https://github.com/mattpocock/skills) | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | 24 |
| mattpocock-pr | [mattpocock/skills](https://github.com/mattpocock/skills) | `49dd158d1076134a641b33efb035946536778336` | 1 |
| warpdotdev | [warpdotdev/common-skills](https://github.com/warpdotdev/common-skills) | `7c4eb852de8d7c3e68c81802e1c59db9a611f914` | 1 |
| pstack | [cursor/plugins](https://github.com/cursor/plugins) | `032be146865d973682535de75f2287da438550bf` | 7 |
| ponytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` | 1 |
| humanlayer | [humanlayer/skills](https://github.com/humanlayer/skills) | `ca7c8088db69e315a8b2deea43820270457f8f3c` | 1 |
| vercel | [vercel-labs/skills](https://github.com/vercel-labs/skills) | `7407f3893ad4dceab546ac002c3ef806e4000c73` | 1 |
| caveman | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `542442bab314973709f95b85b1ac0b3f6f5b5dc6` | 20 |
| wshobson | [wshobson/agents](https://github.com/wshobson/agents) | `46891e7e60da0e52baf1050b7b6391b64e84c6d9` | 1 |
| addyosmani | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | `1401c8b8030e023baeebb31781a6653fe8e93026` | 2 |
| severity1 | [severity1/claude-code-prompt-improver](https://github.com/severity1/claude-code-prompt-improver) | `50aae187bb4f08b852f318234b654df3332726a4` | 1 |
| taste | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | `b482f7a970abb98c4108d4a9f761e458c64cefc8` | 1 |
| onewave | [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | `fc5b7851a6c7ba367e05797df46ad3679df355dd` | 1 |
| vercel-agent-browser | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | `f7c8b071343dda29477a56cb336ea76144c05496` | 1 |

Architecture Patterns includes its upstream `references/details.md` and `references/advanced-patterns.md`. Incremental Implementation bundles the upstream shared `references/definition-of-done.md` inside its own reference directory; `upstreams.json` records that additional source-to-local mapping. Commit and delivery instructions in the Addy forks honor existing authorization and project requirements. Other workflow names remain optional, separately selected choices.

Prompt Improver adapts severity1's research-first workflow into a manually invoked research and execution handoff. One light subagent answers investigation questions from code and supplied conversation history, checks existing behavior and reuse targets, and returns a scoped prompt. The main agent displays that prompt and executes it without an extra approval round; unresolved user decisions are clarified first. Local supporting references cover the subagent assignment and complete, partial, missing, and inaccessible implementations. No upstream plugin or automatic hooks are included; the local adaptations are recorded in `upstreams.json`.

Manual QA preserves Vercel's exploratory QA guidance, issue checklist, and adapted report template. It uses native Codex Computer Use, resolves URL/sign-in/scope from user context, plans and tracks every case, continues independent cases after failures, and reports incomplete coverage. The source revision, original file paths, renamed destinations, and local changes are recorded in `upstreams.json`. It has no separate browser CLI or plugin dependency.

Taste and OneWave were added on 8 October 2026. Taste `image-to-code` preserves text → generated images → analysis → frontend implementation. OneWave `screenshot-to-code` preserves screenshot → visual spec → implementation → render comparison, including its stack and visual-check references. Both use manual invocation and retain upstream workflow bodies. Their license notices are preserved in `licenses/`.

Matt's `pr` and Warp's `write-pr-description` were added on 14 October 2026 with narrow automatic invocation. Warp owns the drafting procedure; Matt supplies summary, evidence, and impact guidance in the same body. Both require a specific authorized PR authoring deliverable, honor repository templates, and keep publication within existing authorization. Their shared scope reference excludes review-only, coding-only, research, and template/skill editing. Matt's new skill has a separate provenance pin so the other Matt skills retain their recorded revision. Warp's references and upstream evaluation cases are bundled; both authors' license notices are preserved.

## Functional groups

Skill picker labels use 20 functional prefixes, each grouping 2–5 skills by their main purpose. All 71 skills are assigned exactly once. Invocation names and installation paths are preserved. See the [complete grouping](reports/skill-groups.md).

## Catalog

**superpowers:** `brainstorming`, `executing-plans`, `finishing-a-development-branch`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `writing-plans`.

**mattpocock:** `grill-me`, `grill-with-docs`, `grilling`, `research`, `resolving-merge-conflicts`, `wait-what`, `wizard`, `writing-for-agents`, `code-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `handoff`, `implement`, `improve-codebase-architecture`, `prototype`, `setup-matt-pocock-skills`, `tdd`, `teach`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`, `wayfinder`.

**mattpocock-pr:** `pr`.

**warpdotdev:** `write-pr-description`.

**pstack:** `blast-radius`, `how`, `recall`, `show-me-your-work`, `technical-writing`, `unslop`, `why`.

**ponytail:** `ponytail`.

**humanlayer:** `show-me`.

**vercel:** `find-skills`.

**wshobson:** `architecture-patterns`.

**addyosmani:** `code-simplification`, `incremental-implementation`.

**severity1:** `prompt-improver`.

**vercel-agent-browser:** `manual-qa`.

**taste:** `image-to-code`.

**onewave:** `screenshot-to-code`.

**caveman:** `caveman:cavecrew`, `caveman:caveman`, `caveman:caveman-commit`, `caveman:caveman-compress`, `caveman:caveman-discover`, `caveman:caveman-evidence-review`, `caveman:caveman-explore`, `caveman:caveman-help`, `caveman:caveman-learn`, `caveman:caveman-manage`, `caveman:caveman-optimize`, `caveman:caveman-review`, `caveman:caveman-setup`, `caveman:caveman-stats`, `caveman:investigate-first`, `caveman:lean-build`, `caveman:migration`, `caveman:safe-refactor`, `caveman:surgical-patch`, `caveman:verify-and-stop`.

## Installation

Run `python3 scripts/install.py` to preview, then `./install.sh` to apply. This one command installs skill links, syncs the complete [shared Codex AGENTS.md](#share-global-codex-instructions-across-computers-and-vms), and generates a missing [runtime profile](#machine-specific-php-and-composer-runtimes) when local executable paths identify an unambiguous runtime. The installer keeps one canonical directory per standalone skill under this repository, links it through `~/.agents/skills` and `~/.claude/skills`, and retires repository-owned aliases under `~/.codex/skills` and `~/.cursor/skills-cursor`. It refuses unmanaged skill name collisions and backs up replaced copies outside discovery roots. Re-running it preserves an existing runtime profile and makes no changes to current skill links or identical global instructions.

For the local Caveman edition and the personal instruction block:

```sh
python3 scripts/configure_hosts.py
codex plugin add caveman@personal
claude plugin marketplace add ./plugins
claude plugin install caveman@personal-manual
claude plugin disable caveman@caveman
```

Disable the original `caveman@caveman` entry in Codex plugin settings as well; leave `caveman@personal` enabled. Do not delete upstream caches. Start a fresh task after changing discovery, and restart Claude Code to unload previously registered hooks. Application-managed built-in and specialist plugins remain owned by their host.

### Share global Codex instructions across computers and VMs

[config/codex/AGENTS.md](config/codex/AGENTS.md) is the shared template for the complete global Codex instructions. Edit personal rules there. Keep its `{{PERSONAL_SKILL_POLICY}}` placeholder inside the policy markers; the sync command fills that section from [invocation-policy.json](invocation-policy.json) and the existing policy generator. The generated file contains your personal rules and the current skill policy on every machine running the same repository revision.

After cloning this repository, run `./install.sh` from its directory. To preview all changes first:

```sh
python3 scripts/install.py
./install.sh
```

The preview prints a JSON result with a `codex_agents` section containing the target path, whether it would change, and a unified diff. It creates no files. Apply installs a regular UTF-8 file and reports the backup file path in `codex_agents.backup` when replacing existing content. Backups live under `~/.local/share/agent-skills/backups`. A repeated apply with identical content does not rewrite the file or create another backup. Existing file permissions are preserved; installation uses an atomic replacement.

Sync replaces the entire global file, including any local additions. Edit the repository template for changes you want to share; edits to the installed file are not imported. After committing and pushing shared changes, update each other machine with:

```sh
git pull --ff-only && ./install.sh
```

Git transport and installation are explicit. Switching branches or pulling changes does not change the installed copy until you run the installer or apply the standalone sync. Start a fresh Codex session to load updated instructions.

The target is `$CODEX_HOME/AGENTS.md` when that variable is set, otherwise `~/.codex/AGENTS.md`. Both the installer and standalone sync accept `--codex-home /path/to/profile` to select a specific Codex directory. For isolated testing, `--home /path/to/scratch-home` puts both the target and backups under that home and ignores `CODEX_HOME`; an explicit `--codex-home` can still select a separate target. Backups always use the selected home.

Installation stops if `AGENTS.override.md` exists in the selected Codex directory, because it can take precedence over the shared file. Resolve that override before syncing. It also refuses an existing symlink or non-file at the target; preserve or move that item before retrying. The installer checks these conditions before changing skill links or runtime profiles. To restore a replaced file, copy the backup file reported in the JSON result to the reported target.

To sync only Codex instructions, the standalone commands remain available:

```sh
python3 scripts/configure_hosts.py --sync-codex-agents
python3 scripts/configure_hosts.py --sync-codex-agents --apply
```

This standalone mode leaves skills, runtime profiles, Claude instructions, and marketplace registration untouched, and cannot be combined with `--policy-only`. The existing `--policy-only` command continues to update just the managed blocks while preserving other instructions. The combined installer also leaves Claude instructions and marketplace registration untouched. See [OpenAI's instruction discovery documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) for global overrides and session loading.

#### Machine-specific PHP and Composer runtimes

The shared instructions explicitly tell the agent to read `~/.config/agent-skills/runtime.md` before running PHP or Composer commands. Run the installer on each computer or VM to generate this machine-specific file. It stays outside the repository, so the global `AGENTS.md` can remain identical across machines. The separate `--sync-codex-agents` command only installs the shared instructions and leaves runtime profiles alone.

The installer inspects executables on its current `PATH` and resolves symlinks. It does not invoke the discovered tools, start containers, install runtimes, or test their health. Shell aliases and functions are not included. An explicit `--home` changes the installation destination; detection still describes the machine and environment running the installer.

Automatic detection follows these rules:

- Lerd alone is available: select `lerd php` and `lerd composer`.
- Both `php` and `composer` resolve to Yerd's launcher, with no competing Lerd: select direct `php` and `composer` commands.
- Both runtime managers are found: report `ambiguous` and leave the profile untouched.
- The paths do not establish either setup, or tools are missing: report `unavailable` and leave the profile untouched. The presence of Yerd alone does not prove the direct commands use it.

Skill installation and shared AGENTS.md syncing can complete when runtime detection is ambiguous or unavailable. Inspect the JSON `runtime` result: it includes the status, reason, discovered executable paths, selected command forms, proposed file content, and any backup file. A preview creates no profile; apply reports `written` after generation.

Use an explicit choice when necessary. `lerd` requires an executable `lerd` on PATH; `direct` requires both `php` and `composer`. Explicit `direct` can also be used for a non-Yerd setup you have verified. `skip` disables runtime detection and generation; the installer still installs skills and syncs AGENTS.md.

```sh
python3 scripts/install.py --runtime lerd
./install.sh --runtime lerd
./install.sh --runtime direct
./install.sh --runtime skip
```

Existing profiles, including handwritten files and symlinks, are preserved before detection. An explicit runtime choice does not replace an existing profile by itself. After changing runtimes or PATH, preview a refresh, then apply it:

```sh
python3 scripts/install.py --refresh-runtime
./install.sh --refresh-runtime
```

Combine refresh with `--runtime lerd` or `--runtime direct` if needed. Refresh backs up changed regular files under `~/.local/share/agent-skills/backups` before atomic replacement, preserves permissions, and does nothing when the content already matches. It refuses symlinks and cannot be combined with `--runtime skip`. Unsuccessful detection leaves the previous file intact.

You can also maintain a profile manually: create the directory with `mkdir -p ~/.config/agent-skills`, then save the applicable example below as `runtime.md` inside it. Adapt the command forms if your setup differs. These command forms follow the [Lerd PHP documentation](https://lerd.sh/usage/php) and [Yerd PHP documentation](https://yerd.app/guide/php-versions).

For your Mac using Lerd:

```markdown
# PHP and Composer runtime

Run PHP and Composer commands through Lerd from the project directory:

- PHP: `lerd php ...` (for example, `lerd php artisan test`).
- Composer: `lerd composer ...` (for example, `lerd composer check`).
```

For your VM with direct access to Yerd's PHP and Composer through PATH:

```markdown
# PHP and Composer runtime

Yerd's PHP and Composer are available directly through PATH. Run commands
from the project directory:

- PHP: `php ...` (for example, `php artisan test`).
- Composer: `composer ...` (for example, `composer check`).
```

The example test commands assume the project provides those commands or scripts. When commands execute in a VM or remote host, read that execution host's runtime file. The file is consulted through the shared instruction; it is not an automatically discovered Codex instruction filename. If it is missing or unclear, establish the runtime configuration before executing project commands. An operating system name alone does not select a runtime.

## Local policy overlay

- [invocation-policy.json](invocation-policy.json) owns the seven automatic skills and their triggers. Their entrypoints set `disable-model-invocation: false` and `policy.allow_implicit_invocation: true`. The other 64 entrypoints keep the opposite settings. Both fields must agree with the allowlist.
- Selection applies to one task. Session-wide modes need an explicit request. Always-on style mandates, forced workflow transitions, and automatic activation from generated plans or handoffs are removed or made optional.
- Supporting files are still readable. `grill-me` declares the grilling procedure; `grill-with-docs` declares grilling and domain documentation.
- Project runtime, verification, delivery requirements, and existing user authorization take precedence. Superpowers namespace references are adapted for standalone installation; optional isolation uses host facilities.
- Caveman preserves its 20 workflow names, reviewer presets, and manual stats helper, with four focused automatic workflows and no startup/prompt hook registration. The original plugin is disabled rather than deleted. The stats helper cannot reconstruct mode attribution that was never recorded.
- Duplicate installations are consolidated by name. Distinct alternative workflows such as `tdd` and `test-driven-development` remain separate, manually selected choices.

## Updating without losing the policy

Run `python3 scripts/check_updates.py` to compare the pinned revisions with the authors’ default branches. It reports only; it never replaces skills. Merge changed skill files against the recorded base, preserve the selective invocation overlay, update `upstreams.json`, and review executable helpers. For Caveman, bump the local plugin version and reinstall through each host after editing the source. Do not edit versioned plugin caches.

Validate metadata and references with `python3 scripts/validate.py` (requires `pip install -r scripts/requirements.txt` in your chosen environment). Run `python3 -m unittest discover -s tests -v` for installer behavior. Verify that all personal skills remain available for explicit selection, only the allowlisted skills appear in automatic discovery, and each automatic trigger stays within the authorized task. Start a fresh task after changing discovery.

Third-party licenses are preserved in [licenses/](licenses/). Excluded upstream bundles, bootstrap skills, and hooks are not installed by this repository.
