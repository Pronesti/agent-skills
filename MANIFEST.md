# Curated Agent Skills

This repository owns **54 standalone skills and a 20-skill Caveman edition**. Seven focused skills allow automatic invocation; the other 67 personal workflows require explicit user selection. See [POLICY.md](POLICY.md) for invocation boundaries.

Read the [workflow guide](WORKFLOW-GUIDE.md) for 56 scenarios in ASD-STE100 English. The guide covers all 74 workflows, their sequences, and combinations with different instructions.

## Author revisions

All 73 managed skills were checked against their authors on 7 November 2026: 41 had upstream file changes, 30 had unchanged upstream content, and two removed upstream skills were retained locally. See the [update report](reports/2026-11-07-skill-updates/REPORT.md) for reconciliation decisions and verification limits. [upstreams.json](upstreams.json) records applied bases and separate checked revisions for retained skills. A newer repository revision does not necessarily change every selected skill. Impeccable, added later the same day, was not part of that check, which is why it counted 73 of the current 74 skills.

| Source | Original repository | Pinned revision | Skills |
|---|---|---|---:|
| superpowers | [obra/superpowers](https://github.com/obra/superpowers) | `22f0b463e7a5e579904dd6211a520321035526f7` | 8 |
| mattpocock | [mattpocock/skills](https://github.com/mattpocock/skills) | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | 23 |
| pstack | [cursor/plugins](https://github.com/cursor/plugins) | `6b0300214a09fd6029cfb7077043125758cd1fd2` | 7 |
| ponytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` | 1 |
| humanlayer | [humanlayer/skills](https://github.com/humanlayer/skills) | `4d69d20f6e9b57b4fcf0d501ccfb1be961f0f329` | 1 |
| vercel | [vercel-labs/skills](https://github.com/vercel-labs/skills) | `d3701c11b1101251af14c9d148f026e1a47ebe17` | 1 |
| caveman | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `c310c9d300df13a1dd9f5c086120ffd857a164a1` | 20 |
| wshobson | [wshobson/agents](https://github.com/wshobson/agents) | `4bde3168b43c0655c4d00ea2726e631719908a6d` | 1 |
| addyosmani | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | `301b02b12bff98e4688e6984af6556802322bbde` | 2 |
| severity1 | [severity1/claude-code-prompt-improver](https://github.com/severity1/claude-code-prompt-improver) | `50aae187bb4f08b852f318234b654df3332726a4` | 1 |
| vercel-agent-browser | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | `d44f6989bf5e9a9a1c6dd6d97175f8c33b138eca` | 1 |
| taste | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | `b482f7a970abb98c4108d4a9f761e458c64cefc8` | 1 |
| onewave | [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | `b2267d9171af4f56848d82992381b20b89b44056` | 1 |
| mattpocock-pr | [mattpocock/skills](https://github.com/mattpocock/skills) | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | 1 |
| warpdotdev | [warpdotdev/common-skills](https://github.com/warpdotdev/common-skills) | `8792394ff1b655e0af451b8fabb68ef0cfcbd208` | 1 |
| anthropics-frontend | [anthropics/skills](https://github.com/anthropics/skills) | `2c5958ecac7cee2b583967a2c4981d0f4a75c579` | 1 |
| nextlevelbuilder | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `b7d5353e0130feb8c5574ef1251f8a1db1873ccb` | 1 |
| mattpocock-conflicts | [mattpocock/skills](https://github.com/mattpocock/skills) | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | 1 |
| impeccable | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `414603bf14c7a344edb466bb1f85690c77ce8b7d` (`skill-v4.8.0`) | 1 |

Architecture Patterns includes its upstream `references/details.md` and `references/advanced-patterns.md`. Incremental Implementation bundles the upstream shared `references/definition-of-done.md` inside its own reference directory; `upstreams.json` records that additional source-to-local mapping. Commit and delivery instructions in the Addy forks honor existing authorization and project requirements. Other workflow names remain optional, separately selected choices.

Prompt Improver adapts severity1's research-first workflow into a manually invoked research and execution handoff. One light subagent answers investigation questions from code and supplied conversation history, checks existing behavior and reuse targets, and returns a scoped prompt. The main agent displays that prompt and executes it without an extra approval round; unresolved user decisions are clarified first. Local supporting references cover the subagent assignment and complete, partial, missing, and inaccessible implementations. No upstream plugin or automatic hooks are included; the local adaptations are recorded in `upstreams.json`.

Manual QA preserves Vercel's exploratory QA guidance, issue checklist, and adapted report template. It uses native Codex Computer Use, resolves URL/sign-in/scope from user context, plans and tracks every case, continues independent cases after failures, and reports incomplete coverage. The source revision, original file paths, renamed destinations, and local changes are recorded in `upstreams.json`. It has no separate browser CLI or plugin dependency.

Taste and OneWave were added on 8 October 2026. Taste `image-to-code` preserves text → generated images → analysis → frontend implementation. OneWave `screenshot-to-code` preserves screenshot → visual spec → implementation → render comparison, including its stack and visual-check references. Both use manual invocation and retain upstream workflow bodies. Their license notices are preserved in `licenses/`.

Matt's `pr` and Warp's `write-pr-description` were added on 14 October 2026 with narrow automatic invocation. Warp owns the drafting procedure; Matt supplies summary, evidence, and impact guidance in the same body. Both require a specific authorized PR authoring deliverable, honor repository templates, and keep publication within existing authorization. Their shared scope reference excludes review-only, coding-only, research, and template/skill editing. Matt's new skill has a separate provenance pin so the other Matt skills retain their recorded revision. Warp's references and upstream evaluation cases are bundled; both authors' license notices are preserved.

Anthropic `frontend-design` and Next Level Builder `ui-ux-pro-max` were added on 17 October 2026. The first guides visual direction and frontend implementation. The second provides a local searchable UI/UX catalog and stack-specific guidance. Both are manual workflows with pinned upstream revisions, bundled data and scripts where needed, and upstream license notices.

Impeccable 4.8.0 was added on 7 November 2026 from the compiled Codex skill in the pinned `skill-v4.8.0` release. It bundles references, helper-agent prompts, data, and portable launchers; platform binaries and hook registration are excluded. The launcher downloads a checksum-verified engine into the user cache when needed. Invoke `$impeccable` explicitly. The same repository directory is linked at user level for Codex, Cursor, and Claude. Existing project-local copies can take precedence and remain separately managed.

## Functional groups

Skill picker labels use 20 functional prefixes, each grouping 2–5 skills by their main purpose. All 74 skills are assigned exactly once. Invocation names and installation paths are preserved. See the [complete grouping](reports/skill-groups.md).

## Catalog

**superpowers:** `brainstorming`, `executing-plans`, `finishing-a-development-branch`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `writing-plans`.

**mattpocock:** `grill-me`, `grill-with-docs`, `grilling`, `research`, `wait-what`, `wizard`, `writing-for-agents`, `code-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `handoff`, `implement`, `improve-codebase-architecture`, `prototype`, `setup-matt-pocock-skills`, `tdd`, `teach`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`, `wayfinder`.

**mattpocock-pr:** `pr`.

**mattpocock-conflicts:** `resolving-merge-conflicts`.

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

**anthropics-frontend:** `frontend-design`.

**nextlevelbuilder:** `ui-ux-pro-max`.

**impeccable:** `impeccable`.

**caveman:** `caveman:cavecrew`, `caveman:caveman`, `caveman:caveman-commit`, `caveman:caveman-compress`, `caveman:caveman-discover`, `caveman:caveman-evidence-review`, `caveman:caveman-explore`, `caveman:caveman-help`, `caveman:caveman-learn`, `caveman:caveman-manage`, `caveman:caveman-optimize`, `caveman:caveman-review`, `caveman:caveman-setup`, `caveman:caveman-stats`, `caveman:investigate-first`, `caveman:lean-build`, `caveman:migration`, `caveman:safe-refactor`, `caveman:surgical-patch`, `caveman:verify-and-stop`.

## Installation

Run `python3 scripts/install.py` to preview, then `./install.sh` to apply. This command installs skill links and generates a missing [runtime profile](#machine-specific-php-and-composer-runtimes) when local executable paths identify an unambiguous runtime. Existing global instructions are preserved byte for byte, including local additions and managed policy blocks. When neither `AGENTS.md` nor `AGENTS.override.md` exists in the selected Codex directory, the installer creates the [shared global instructions](#share-global-instructions-across-hosts-computers-and-vms) there, and it creates a missing `~/.claude/CLAUDE.md` that imports them. Existing symlinks, overrides, and Claude files are left in place. Full instruction replacement requires the explicit `--sync-agents` flag.

The installer keeps one canonical directory per standalone skill under this repository, links it through `~/.agents/skills` and `~/.claude/skills`, and retires repository-owned aliases under `~/.codex/skills` and `~/.cursor/skills-cursor`. It refuses unmanaged skill name collisions and backs up replaced copies outside discovery roots. Re-running it preserves existing runtime profiles, global instructions, and current skill links. If Impeccable was already installed globally by `npx`, back up that unmanaged skill directory outside discovery roots before running the installer; unmanaged collisions remain protected. Update the managed copy through Git and this installer, rather than `npx impeccable update`.

For the local Caveman edition and the personal instruction block:

```sh
python3 scripts/configure_hosts.py
codex plugin add caveman@personal
claude plugin marketplace add ./plugins
claude plugin install caveman@personal-manual
claude plugin disable caveman@caveman
```

Disable the original `caveman@caveman` entry in Codex plugin settings as well; leave `caveman@personal` enabled. Do not delete upstream caches. Start a fresh task after changing discovery, and restart Claude Code to unload previously registered hooks. Application-managed built-in and specialist plugins remain owned by their host.

### Share global instructions across hosts, computers, and VMs

[config/AGENTS.md](config/AGENTS.md) is the shared template for the complete global instructions of both Codex and Claude Code. Codex reads the installed copy at `~/.codex/AGENTS.md`. Claude Code reads `~/.claude/CLAUDE.md`, which the installer creates, when it is missing, as a single import of that same file (`@~/.codex/AGENTS.md`). One installed file therefore serves both hosts, and tools that write into `~/.codex/AGENTS.md`, such as `lerd mcp:enable-global`, reach both. An existing `CLAUDE.md` is never rewritten; the JSON result's `claude.imports_shared` reports whether it already imports the shared file. Edit personal rules there. Keep its `{{PERSONAL_SKILL_POLICY}}` placeholder inside the policy markers; the sync command fills that section from [invocation-policy.json](invocation-policy.json) and the existing policy generator. The generated file contains your personal rules and the current skill policy on every machine running the same repository revision.

Ordinary skill updates preserve existing global instructions. To explicitly replace the global instructions with the shared template while installing skills, preview the replacement first:

```sh
python3 scripts/install.py --sync-agents
./install.sh --sync-agents
```

The preview prints a JSON result with an `instructions` section containing the target path, whether it would change, and a unified diff. It creates no files. Default installation reports `preserved: true` and an empty diff when instructions already exist. With `--sync-agents`, apply installs a regular UTF-8 file and reports the backup file path in `instructions.backup` when replacing existing content. Backups live under `~/.local/share/agent-skills/backups`. A repeated explicit sync with identical content does not rewrite the file or create another backup. Existing file permissions are preserved; replacement is atomic. Creating a missing file also preserves instructions that appear concurrently during installation.

Explicit sync replaces the entire global file, including local additions such as the block that `lerd mcp:enable-global` writes; rerun that command after a sync on machines that use lerd. Review the preview before using it. Edit the repository template for changes you want to share; edits to the installed file are not imported. After committing and pushing shared instruction changes, opt into syncing on each machine with:

```sh
git pull --ff-only && ./install.sh --sync-agents
```

Skill links read this checkout's canonical files. Global instruction copies change only when initialized or explicitly synced. Start a fresh Codex or Claude Code session to load updated instructions.

The target is `$CODEX_HOME/AGENTS.md` when that variable is set, otherwise `~/.codex/AGENTS.md`. Both the installer and standalone sync accept `--codex-home /path/to/profile` to select a specific Codex directory. For isolated testing, `--home /path/to/scratch-home` puts both the target and backups under that home and ignores `CODEX_HOME`; an explicit `--codex-home` can still select a separate target. Backups always use the selected home.

Explicit instruction sync stops if `AGENTS.override.md` exists in the selected Codex directory, because it can take precedence over the shared file. Resolve that override before syncing. Explicit sync also refuses an existing symlink or non-file at the target; preserve or move that item before retrying. These checks run before changing skill links or runtime profiles. Default skill installation leaves those instruction paths untouched and continues. To restore an explicitly replaced file, copy the backup file reported in the JSON result to the reported target.

To sync only the global instructions, the standalone commands remain available:

```sh
python3 scripts/configure_hosts.py --sync-agents
python3 scripts/configure_hosts.py --sync-agents --apply
```

This standalone mode leaves skills, runtime profiles, and marketplace registration untouched, and cannot be combined with `--policy-only`. Like the installer, it creates a missing Claude import and leaves an existing `CLAUDE.md` alone. The `--policy-only` command updates just the managed blocks while preserving other instructions; it skips a `CLAUDE.md` that imports the shared file, because Claude already receives the block through the import. Where no global instructions exist, it installs the complete shared template first rather than a policy-only fragment. The combined installer leaves marketplace registration untouched. See [OpenAI's instruction discovery documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) for global overrides and session loading.

#### Machine-specific PHP and Composer runtimes

The shared instructions explicitly tell the agent to read `~/.config/agent-skills/runtime.md` before running PHP or Composer commands. Run the installer on each computer or VM to generate this machine-specific file. It stays outside the repository, so the global `AGENTS.md` can remain identical across machines. The separate `--sync-agents` command only installs the shared instructions and leaves runtime profiles alone.

The installer inspects executables on its current `PATH` and resolves symlinks. It does not invoke the discovered tools, start containers, install runtimes, or test their health. Shell aliases and functions are not included. An explicit `--home` changes the installation destination; detection still describes the machine and environment running the installer.

Automatic detection follows these rules:

- Lerd alone is available: select `lerd php` and `lerd composer`.
- Both `php` and `composer` resolve to Yerd's launcher, with no competing Lerd: select direct `php` and `composer` commands.
- Both runtime managers are found: report `ambiguous` and leave the profile untouched.
- The paths do not establish either setup, or tools are missing: report `unavailable` and leave the profile untouched. The presence of Yerd alone does not prove the direct commands use it.

Skill installation and optional instruction syncing can complete when runtime detection is ambiguous or unavailable. Inspect the JSON `runtime` result: it includes the status, reason, discovered executable paths, selected command forms, proposed file content, and any backup file. A preview creates no profile; apply reports `written` after generation.

Use an explicit choice when necessary. `lerd` requires an executable `lerd` on PATH; `direct` requires both `php` and `composer`. Explicit `direct` can also be used for a non-Yerd setup you have verified. `skip` disables runtime detection and generation; instruction preservation and skill installation follow their usual rules.

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

- [invocation-policy.json](invocation-policy.json) owns the seven automatic skills and their triggers. Their entrypoints set `disable-model-invocation: false` and `policy.allow_implicit_invocation: true`. The other 67 entrypoints keep the opposite settings. Both fields must agree with the allowlist.
- Selection applies to one task. Session-wide modes need an explicit request. Always-on style mandates, forced workflow transitions, and automatic activation from generated plans or handoffs are removed or made optional.
- Supporting files are still readable. `grill-me` declares the grilling procedure; `grill-with-docs` declares grilling and domain documentation.
- Project runtime, verification, delivery requirements, and existing user authorization take precedence. Superpowers namespace references are adapted for standalone installation; optional isolation uses host facilities.
- Caveman preserves its 20 workflow names, reviewer presets, and manual stats helper, with four focused automatic workflows and no startup/prompt hook registration. The original plugin is disabled rather than deleted. The stats helper cannot reconstruct mode attribution that was never recorded.
- Duplicate installations are consolidated by name. Distinct alternative workflows such as `tdd` and `test-driven-development` remain separate, manually selected choices.

## Updating without losing the policy

Run `python3 scripts/check_updates.py` to compare the pinned revisions with the authors’ default branches. It reports only; it never replaces skills. Merge changed skill files against the recorded base, preserve the selective invocation overlay, update `upstreams.json`, and review executable helpers. The invocation overlay applies to every entry, so an entry's `local_changes` lists only deviations beyond it. For Caveman, bump the local plugin version and reinstall through each host after editing the source. Do not edit versioned plugin caches.

Validate metadata and references with `python3 scripts/validate.py` (requires `pip install -r scripts/requirements.txt` in your chosen environment). Run `python3 -m unittest discover -s tests -v` for installer behavior. Verify that all personal skills remain available for explicit selection, only the allowlisted skills appear in automatic discovery, and each automatic trigger stays within the authorized task. Start a fresh task after changing discovery.

Third-party licenses are preserved in [licenses/](licenses/). Excluded upstream bundles, bootstrap skills, and hooks are not installed by this repository.
