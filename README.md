# Agent Skills

A personal collection of agent skills, shared Codex instructions, and machine-specific PHP/Composer runtime guidance. Use the same repository on your computers and VMs to keep the shared instructions consistent.

## Prerequisites

- macOS or Linux, including Linux VMs, with support for symbolic links.
- Git, Bash, and Python 3 available as `git`, `bash`, and `python3` on your `PATH`.
- Access to this GitHub repository for cloning and pulling updates.
- An installed agent host, such as Codex or Claude Code, to use the skills.

The installer uses Python's standard library; it does not need additional Python packages. PHP, Composer, Lerd, and Yerd are optional for installation. Set up the runtime you use before asking the installer to generate its PHP/Composer profile.

## Install on a computer or VM

Run these commands as your normal user in a directory where you keep projects:

```sh
git clone https://github.com/Pronesti/agent-skills.git
cd agent-skills
```

Keep this checkout in a permanent location: installed skill links point to its files.

**The installer replaces the complete global Codex AGENTS.md, including local additions.** It backs up changed existing content under `~/.local/share/agent-skills/backups` and reports the backup path. Review the preview before the first installation:

```sh
python3 scripts/install.py
```

Apply with one command:

```sh
./install.sh
```

The installer handles all three parts:

| Part | Installed location | Behavior |
| --- | --- | --- |
| Standalone skills | `~/.agents/skills` and `~/.claude/skills` | Links to the canonical files in this checkout. |
| Shared Codex instructions | `~/.codex/AGENTS.md` | Renders the shared template and skill policy; backs up changed existing content. |
| Local runtime profile | `~/.config/agent-skills/runtime.md` | Creates a missing file when runtime detection is unambiguous. |

If `CODEX_HOME` is set, its `AGENTS.md` is the target instead. Use `./install.sh --codex-home /path/to/profile` to choose a specific Codex directory. Other installation paths still use your home directory.

The Caveman plugin and Claude instruction-block setup have separate host configuration steps. Follow the [detailed installation guide](MANIFEST.md#installation) for those steps. The main installer does not register plugins or update Claude instructions.

Start a fresh agent chat after installation so the host can load updated instructions and skill discovery.

## Update an existing installation

From this repository's checkout, select `main` and pull the published updates before installing:

```sh
git switch main && git pull --ff-only && ./install.sh
```

Run this on each computer or VM. The installer does not fetch Git changes itself.

Repeated installation is idempotent: correct skill links and identical AGENTS.md content stay unchanged, and an existing runtime profile is preserved. Changed shared instructions are backed up before replacement.

To change your shared personal instructions, edit [config/codex/AGENTS.md](config/codex/AGENTS.md). Preserve its policy placeholder. After those changes are committed, pushed, and merged into `main`, run the update command on each machine. Edits made directly to the installed global file are not imported into the repository.

## Set up the local runtime

Run the installer on the machine where PHP and Composer will execute. It inspects executable paths and symlinks on the current `PATH`; it does not install runtimes, launch them, check their health, or select a PHP version.

| Detected setup | Generated command forms |
| --- | --- |
| Lerd available without competing Yerd | `lerd php ...` and `lerd composer ...` |
| Both PHP and Composer resolve to Yerd's launcher, without Lerd | `php ...` and `composer ...` |
| Both managers, missing tools, or an unclear setup | No profile generated; output reports `ambiguous` or `unavailable`. |

Skills and AGENTS.md can still install when runtime detection is unresolved. Check the JSON output's `runtime.status`, `runtime.reason`, and `runtime.executables` fields.

If automatic detection cannot select your setup, verify the commands on that machine and choose the appropriate option:

```sh
./install.sh --runtime lerd
```

Or, for verified direct PHP and Composer access:

```sh
./install.sh --runtime direct
```

An explicit selection still preserves an existing runtime profile. After changing runtimes or `PATH`, preview and apply a refresh:

```sh
python3 scripts/install.py --refresh-runtime
./install.sh --refresh-runtime
```

Refresh backs up changed regular files. You can combine it with `--runtime lerd` or `--runtime direct`. To leave runtime detection out entirely, use `./install.sh --runtime skip`; skills and AGENTS.md still install.

Keep runtime.md local to each machine. Follow each project's PHP version requirements separately. See the [runtime guide](MANIFEST.md#machine-specific-php-and-composer-runtimes) for examples and detection details.

## Use the skills

Select a skill by name in your agent request, or through the host's skill picker. For example:

```text
Use brainstorming to help design this feature before implementation.
```

Most personal workflows require explicit selection. Only the focused skills listed in [POLICY.md](POLICY.md) may activate automatically for an applicable task. See the [workflow guide](WORKFLOW-GUIDE.md) for choosing skills, combining them, and example requests.

## Troubleshooting

- **AGENTS.override.md, a symlink, or a directory blocks syncing:** inspect and preserve that item, then resolve the conflict before retrying. The installer checks these conditions before changing skills or runtime profiles.
- **Unmanaged skill collision:** inspect the named installation and decide which copy to keep. The installer leaves unmanaged collisions untouched.
- **Runtime remains unchanged:** existing profiles are intentionally preserved. Use `--refresh-runtime` for a regular file; a runtime-profile symlink must be resolved separately.
- **Git cannot fast-forward:** resolve local changes or branch divergence before retrying the update. Installation does not resolve Git conflicts.

To restore previous global instructions, copy the backup reported in `codex_agents.backup` to the path reported in `codex_agents.target`. For a refreshed runtime profile, use `runtime.backup` and `runtime.target`.

## Detailed guides

- [MANIFEST.md](MANIFEST.md): skill catalog, provenance, installation details, custom paths, and [upstream maintenance and validation](MANIFEST.md#updating-without-losing-the-policy).
- [WORKFLOW-GUIDE.md](WORKFLOW-GUIDE.md): workflow selection, sequences, scenarios, and example prompts.
- [POLICY.md](POLICY.md): automatic invocation boundaries and host configuration policy.
- [Shared AGENTS.md template](config/codex/AGENTS.md): the source for global personal instructions.
- [Third-party licenses](licenses/): licenses retained for the collected skills.
