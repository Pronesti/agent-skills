# Native agents and model roles

The installer generates native TOML agents under the selected Codex profile's
`agents/` directory. Two named agents preserve the upstream agent bodies:
`pstack-poteto-agent` and `pstack-comment-sicko`. The remaining agents cover every
role in [the role registry](../../config/codex/pstack-roles.json), including panel
slots. The default installation has 23 agents. All inherit model and effort.

When a selected workflow delegates work:

1. Resolve its role using the registry and the installed `pstack-*.toml` files.
   Use the host's native custom-agent selector when its spawn schema offers one
   (commonly `agent_type`). Send the scoped brief and absolute resource paths.
2. A session such as Codex desktop may expose a spawn tool without an agent-type
   field. Read the installed TOML instead; put its `developer_instructions` in
   the delegate brief and apply its model and effort using supported spawn
   fields. Use isolated context when that schema requires it for overrides.
   State that this is instruction-based dispatch rather than registered-role
   dispatch. Never pass an unsupported `agent_type` or Cursor `subagent_type`.
3. The parent runs the coordinator workflow. A role delegate uses that workflow
   as reference for its assigned slice and does not restart its fan-out. For
   Comment Sicko, preserve the upstream opening line, read-only review, exception
   list, and report contract. A read-only brief does not change the parent's
   sandbox. MCP access continues to come from the parent.
4. Respect the host concurrency limit. A native subagent needs a persisted
   parent thread in the tested runtime; `codex exec --ephemeral` cannot supply
   its saved context. Use a normal session (a disposable profile for tests).

## Configure models

Run from the installed repository. Commands use its `scripts/pstack_codex.py`:

```sh
python3 scripts/pstack_codex.py models
python3 scripts/pstack_codex.py defaults > /tmp/pstack-choices.json
```

Edit the JSON's role entries after resolving the user's budget and choices.
Each role is a list of `{ "model": "inherit-parent" }` entries. Panel lists
set fan-out. A real model entry can add `"effort": "high"` only if that effort
appears in the native catalog. Keep role names from the registry. Use `auto` or
`inherit-parent` for full inheritance, without an effort override.

```sh
python3 scripts/pstack_codex.py configure --choices /tmp/pstack-choices.json
python3 scripts/pstack_codex.py configure --choices /tmp/pstack-choices.json --apply
```

`configure` queries native `model/list` with pagination, validates every real
model and effort, fills an explicit model's omitted effort from its native
default, then previews the exact file operations. Apply saves the resolved
choices at `~/.config/agent-skills/pstack-models.json` and updates native agents
with backups. It does not change `config.toml`, AGENTS.md, providers, permissions,
or MCP settings. `--home` and `--codex-home` precede the subcommand when selecting
an isolated target. Discovery uses the current CLI account; installation
revalidates real model choices on the machine where it runs.

For `$setup-pstack`, replace the upstream `.mdc` procedure with this JSON/native
agent procedure. Show the complete proposed role mapping, including panel slots,
and get the confirmation required by the selected setup workflow before apply.
The `agents` subcommand previews/resyncs native files from saved choices; the
normal installer does the same. No network query is needed for default inherited
settings. Existing legacy `pstack-models.md` choices cause an explicit migration
error rather than being discarded; preserve that file until its choices have
been transferred and confirmed.

The native-agent ownership manifest tracks generated files. Installation refuses
unmanaged same-name files and edited managed files before touching skills or
shared instructions. Untouched managed files can be replaced or retired with a
backup. User agents with other names remain intact. Backups stay under the chosen
home even when the Codex profile is elsewhere.

Different supported GPT models can supply independent panel runs. The helper
reports whether a panel actually configures at least two distinct real models;
`auto` and inheritance do not prove diversity. Different efforts or personas on
one model do not recreate the upstream Claude/Grok cross-provider signal.
