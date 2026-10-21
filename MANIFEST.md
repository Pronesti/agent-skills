# Personal agent skills — pstack edition

This branch replaces the multi-source personal catalog with the complete pstack
package, adapted for Codex. The shared [AGENTS.md template](config/codex/AGENTS.md),
runtime detection, instruction syncing, installer backups, and read-only update
checker remain in this repository. The template is unchanged from main.

## Source and contents

- Upstream: [cursor/plugins, pstack](https://github.com/cursor/plugins/tree/190d28736eff128ec94f502a22c7fe0c4b56cd37/pstack).
- Revision: `190d28736eff128ec94f502a22c7fe0c4b56cd37`, version `0.15.29`.
- All 172 upstream files are preserved byte-for-byte under [pstack/](pstack/README.md).
  This includes 56 public skills, 23 playbooks, two agent definitions, guides,
  scripts, assets, and the Benny automation pack with three internal skills.
- The [MIT license](pstack/LICENSE) permits forks with the notices retained.
  Earlier license notices remain in `licenses/` for retained history and tooling.

The 56 personal [entrypoints](skills/) load a host adapter and then the unmodified
upstream workflow. Codex uses the [local adapter](pstack/docs/harness/codex.md);
Claude Code uses the bundled upstream adapter. Cursor keeps its native names.
The installer exposes only the public skills, not Benny's internal skills. It also
generates native Codex agent configurations from the local role registry.
[upstreams.json](upstreams.json) records every original file checksum and maps
each entrypoint to its upstream source. No upstream instructions or assets were
removed to make the package appear portable.

## Codex support and limits

Use `$poteto-mode` for the main router, `$poteto-help` for guidance, and
`$setup-pstack` for supported model-role choices. All entrypoints require explicit
selection, matching the prior policy for pstack. Bundled supporting resources
can be read within a selected task. See [POLICY.md](POLICY.md).

The adapter integrates native custom agents, validated per-role model settings,
project-scoped persisted history, and native PR monitoring. See the
[agents/model guide](docs/codex/agents-and-models.md),
[history guide](docs/codex/history.md), and
[monitoring guide](docs/codex/monitoring.md). It keeps model settings
outside the shared AGENTS template. Individual sessions may lack delegation,
history, browser control, or model selection; the adapter requires reporting that
limit instead of inventing an equivalent result. Existing authorization governs
external messages, commits, publication, merging, and deployment.

Cursor Automations/Benny, cloud-agent dashboards, Cursor model APIs, Bugbot setup,
and cursor-team-kit integrations do not carry over unchanged. Benny is retained
as source, not installed as a working Codex automation. Existing forge review
comments and bounded PR checks can use native tools; recurring monitoring needs
an authorized native automation. Full source preservation is verified; full
Cursor feature parity is not claimed.

## Catalog

`architect`, `arena`, `automate-me`, `benchmark-checklist`, `blast-radius`, `bro`, `correct`, `create-formal-verification-skill`, `create-verification-skill`, `figure-it-out`, `how`, `in-your-own-words`, `interrogate`, `ketchup`, `maintain-formal-verification-skill`, `maintain-verification-skill`, `make-bot-ui`, `no-comments`, `poteto-help`, `poteto-mode`, `principle-attack-the-premise`, `principle-boundary-discipline`, `principle-build-the-lever`, `principle-encode-lessons-in-structure`, `principle-exhaust-the-design-space`, `principle-experience-first`, `principle-explain-the-number`, `principle-fix-root-causes`, `principle-foundational-thinking`, `principle-guard-the-context-window`, `principle-laziness-protocol`, `principle-make-operations-idempotent`, `principle-migrate-callers-then-delete-legacy-apis`, `principle-minimize-reader-load`, `principle-model-the-domain`, `principle-never-block-on-the-human`, `principle-outcome-oriented-execution`, `principle-prove-it-works`, `principle-redesign-from-first-principles`, `principle-separate-before-serializing-shared-state`, `principle-sequence-verifiable-units`, `principle-subtract-before-you-add`, `principle-test-behavior-not-implementation`, `principle-type-system-discipline`, `recall`, `reflect`, `setup-pstack`, `sharpen`, `show-me-your-work`, `swarm`, `tdd`, `teach`, `technical-writing`, `typescript-best-practices`, `unslop`, `why`.

See [the workflow guide](WORKFLOW-GUIDE.md) and the complete upstream
[README](pstack/README.md) for routing, principles, and examples.

## Installation

Preview with `python3 scripts/install.py`, then apply with `./install.sh`.
The installer links entrypoints into `~/.agents/skills` and `~/.claude/skills`,
syncs the shared Codex instructions, installs 23 native agent configurations by
default, and detects a missing machine runtime profile. Native agent defaults
inherit model and effort; saved role choices are validated against native model
discovery. Edited or unmanaged same-name agent files stop the install before
skill links or shared instructions change. Preview does not change files. Use `--home /path/to/scratch-home` and
`--runtime skip` for isolated validation. Existing runtime flags are preserved.

When replacing the catalog, links into this repository's old `skills/` or
`plugins/caveman/skills/` roots, including sibling worktrees, can be backed up
and retired. This applies to stale links and same-name links that need to move.
User copies, unrelated links, and unrelated package-manager records are preserved;
a same-name unmanaged collision stops installation before changes.
Backups live under `~/.local/share/agent-skills/backups` outside discovery roots.
A repeat install is idempotent.

Caveman plugin caches and marketplace registrations are not silently modified.
If migrating a machine with Caveman enabled, disable or uninstall its old plugin
through that host to complete the pstack-only live catalog. Application-owned
skills and plugins remain managed by the host. This branch does not install
itself on the live machine or change the main checkout.

`configure_hosts.py --policy-only` keeps its managed-block behavior. Without a
mode flag it also updates only host policy; the obsolete Caveman marketplace
registration step is removed. Use `./install.sh` to install the skills. The standalone shared-instructions mode
and flags below remain available. No plugin marketplace registration is needed
for these personal skill folders.

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

## Updating without losing local behavior

`python3 scripts/check_updates.py` compares the pstack pin with upstream HEAD and
reports only. It never overwrites source. Review upstream changes before importing
an exact new revision. Replace the complete pstack snapshot, refresh its checksum
inventory and public-skill provenance, and create or retire the corresponding
personal entrypoints. Keep the Codex adapter and manual invocation policy.
Changes to upstream source require an explicit new pin/checksum review; do not
silently update the checksums to hide local modifications.

Use Python 3.11 or later for the native TOML integration. Install validation
dependencies in a Python environment:

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The validator checks the complete public catalog, entrypoint links, invocation
metadata, provenance, and every preserved upstream file checksum. Upstream helper
checks, when Bun and dependencies are available, run from
`pstack/skills/poteto-mode/scripts`: `bun run test` and `bun run typecheck`.
Start a fresh chat after installing a changed catalog.

Opt-in native workflow checks (authenticated CLI; all profiles and fixtures are
disposable):

```sh
python3 tests/native_codex_smoke.py
python3 tests/native_monitor_smoke.py --bun /path/to/bun
```

The first verifies actual native agent roles, model/effort application, full
persisted history, and read-only fixture behavior. The second executes the
unchanged upstream watcher against a local forge fixture, testing terminal
notification and deduplication. It makes no live forge calls or scheduled tasks.
See [native integration verification](reports/pstack-native-validation-2026-10-21.md).
