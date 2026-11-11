# agent-skills

Curated skills and the shared global instructions for Codex and Claude Code, installed by `install.sh`. `CLAUDE.md` imports this file, so these rules apply to both hosts. Installed skills are links to whichever checkout last ran `./install.sh`; an edit here reaches the hosts only when that checkout is this one, or after the installing checkout pulls and reinstalls.

## Sources of truth

- `config/AGENTS.md` is the template for the user's global instructions, not instructions for this repository. Edit global rules there. It installs to `~/.codex/AGENTS.md`; `~/.claude/CLAUDE.md` imports that file, so one copy serves both hosts. An install preserves an existing live file; `--sync-agents` replaces it whole (with a backup) and drops the `<!-- lerd:begin -->` block, which `lerd mcp:enable-global` writes back. Keep that block out of the template.
- `invocation-policy.json` owns the automatic-invocation allowlist. Every skill's `SKILL.md` `disable-model-invocation` and `agents/openai.yaml` `policy.allow_implicit_invocation` must agree with it ([POLICY.md](POLICY.md)). Keep these values when merging upstream skill updates.
- `upstreams.json` records provenance for every skill directory under `skills/` and `plugins/caveman/skills/`. Add or remove its entry together with the directory.
- `MANIFEST.md` and `WORKFLOW-GUIDE.md` state skill and workflow counts. Update them when the catalog changes.

## Checks

Run both after any change; `validate.py` needs PyYAML (`pip install -r scripts/requirements.txt`).

```sh
python3 -m unittest discover tests
python3 scripts/validate.py
```

## Applying to the machine

Preview with `python3 scripts/install.py` (add `--sync-agents` to preview an instruction sync). `./install.sh` and `--apply` write to the user's home directories: run them only when asked. After changing `plugins/caveman`, reinstall the plugin as described in [MANIFEST.md](MANIFEST.md#installation).
