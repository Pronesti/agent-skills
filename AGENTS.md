# agent-skills

Curated skills and shared global instructions for Codex and Claude Code, installed by `install.sh`. `CLAUDE.md` imports this file, so these rules apply to both hosts. Installed skill links point at whichever checkout last ran `./install.sh`; an edit here reaches a host only after that checkout pulls and reinstalls.

## Git

Work and commit on `main` in this checkout. This overrides the global feature-branch rule.

## After a push

Recommend this install to the user after every push, for each machine that uses these skills:

```sh
git pull --ff-only && ./install.sh
```

Add the step that matches what changed:

| Changed | Also run |
|---|---|
| `config/AGENTS.md` | Preview `python3 scripts/install.py --sync-agents`, then `./install.sh --sync-agents`. The sync replaces the whole live file, so rerun `lerd mcp:enable-global` where lerd is used. |
| `invocation-policy.json` or a skill's invocation flags | `python3 scripts/configure_hosts.py --policy-only` |
| `plugins/caveman` | Reinstall the plugin as in [MANIFEST.md](MANIFEST.md#installation). |

Then start a fresh Codex or Claude Code session, since instructions and skills load at startup. If `./install.sh` reports `Unmanaged collision`, another checkout owns the links: ask the user which checkout should keep them.

## Sources of truth

- `config/AGENTS.md` is the template for the user's global instructions, not instructions for this repository. It installs to `~/.codex/AGENTS.md`, which `~/.claude/CLAUDE.md` imports. Keep the `<!-- lerd:begin -->` block out of it; lerd writes that block into the live file.
- `invocation-policy.json` owns the automatic-skill allowlist; each skill's two invocation flags must agree with it ([POLICY.md](POLICY.md)). Keep those flags when merging upstream updates.
- `upstreams.json` has one entry per skill directory under `skills/` and `plugins/caveman/skills/`; add or remove it with the directory. An entry's `revision` must equal its source's `revision`, so a skill pinned to an older revision needs its own source key. Record deviations beyond the shared invocation overlay in the entry's `local_changes`.
- `MANIFEST.md` and `WORKFLOW-GUIDE.md` state skill and workflow counts. Update them when the catalog changes; `validate.py` checks the `MANIFEST.md` summary counts.

## Upstream updates

- `python3 scripts/check_updates.py` only reports. Merge upstream changes against the recorded `revision`, then update `upstreams.json`.
- Record each review in `reports/YYYY-MM-DD-skill-updates/` (`REPORT.md`, `upstream-check.json`; folders before 2026-11-07 hold only the check) and update the dated summary in `MANIFEST.md`.
- For Caveman changes, bump `version` in both `plugins/caveman/.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`, and log the change in `plugins/caveman/LOCAL-CHANGES.md`.

## Checks

Run both after any change; `validate.py` needs PyYAML (`pip install -r scripts/requirements.txt`).

```sh
python3 -m unittest discover tests
python3 scripts/validate.py
```

Try installer changes with `--home <scratch dir>`, as the tests do, so the real home stays untouched.

## Writing conventions

- `WORKFLOW-GUIDE.md` uses ASD-STE100 Issue 9: short sentences, one action per sentence, active voice.
- `skills/impeccable/scripts/impeccable.cmd` keeps CRLF line endings (`.gitattributes`).
