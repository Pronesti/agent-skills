# pstack in Codex

Read this adapter before the upstream workflow, and apply it to every reference,
playbook, script instruction, and delegate reached by that workflow. The upstream
tree is preserved verbatim; Cursor names there describe intent, not Codex APIs.
Use the tools and fields actually offered by the current session. Never send a
Cursor field to a Codex tool that does not accept it.

`<pstack>` is the canonical directory containing this file, `skills/`, `agents/`,
and `README.md`. Resolve installation symlinks first. The personal entrypoints
are outside this tree, under the containing repository's `skills/` directory.

## Scope and invocation

All personal entrypoints require explicit selection. A selected pstack workflow
can read the bundled procedures and principles it declares as supporting
resources for the current task. Optional independent workflows still need user
selection. Selecting a workflow does not authorize unrelated work, messages to
other people, commits, publication, merges, deployments, or persistent automation.
Existing user authorization and project instructions govern those actions.

Apply the user's current instructions before upstream autonomy, writing, Git,
or memory rules. Keep the repository's shared AGENTS.md and runtime requirements.
In particular, upstream's blanket permission to use MCP or perform reversible
external actions is not user authorization. A mode ends with the requested task
unless the user explicitly selected a session-wide mode.

## Tools and resources

| Cursor instruction | Codex execution |
| --- | --- |
| `Task` | Use the session's native subagent tool when delegation is authorized and available. In Codex desktop this can be `collaboration.spawn_agent`; other sessions expose different names. Inspect the tool schema. |
| `AskQuestion` | Use a native user-input tool when offered, otherwise ask in the conversation. Continue work independent of a pending answer. |
| Todo list | Use a native plan tool if available, otherwise maintain a short task checklist in the conversation. |
| `Read`, `Grep`, `Glob`, `Bash` | Native file/shell tools; prefer `rg` and `rg --files` for search. |
| `/name`, **name** skill | Resolve `<pstack>/skills/<name>/SKILL.md` as a supporting resource within the selected workflow's scope. For user invocation, write `$name`; there is no `pstack:` prefix in this personal catalog. |
| `create-skill` | Use the host's available skill-authoring capability, following project instructions. |
| `control-ui`, `control-cli` | Use available native browser/computer-use tools or project UI/CLI harnesses. Inspect their docs first. An unavailable tool is not proof of UI behavior. |
| `deslop` | Review the scoped diff with available review tools and project checks. This catalog does not bundle cursor-team-kit or claim its exact behavior. |
| MCP search/discovery | Discover the session's connected tools. A named server is not necessarily installed or authorized. |
| Built-in PR tool | Use an available forge connector or CLI with the existing delivery authorization. |

Read local bundled files rather than fetching current upstream during a run.
For `git show origin/main:pstack/...`, read `<pstack>/...` from this pinned
installation; `origin/main` in the user's product repository is not pstack's
upstream. Historical upstream comparisons must use the recorded upstream URL
and revision, separately from the product checkout. Keep product Git operations
inside the project under work.

## Delegation and models

| Cursor field or behavior | Codex mapping |
| --- | --- |
| `generalPurpose` | A native general-purpose subagent. Do not pass `subagent_type` when the tool has no such field. |
| `poteto-agent` | Use native `pstack-poteto-agent`, with the scoped brief and resource paths. See [native agents](../../../docs/codex/agents-and-models.md) for schema-specific dispatch and the fallback when the host lacks a custom-agent selector. |
| `comment-sicko` | Use native `pstack-comment-sicko` for the read-only review. Its native configuration reads the original agent body through this adapter. |
| `readonly: true` | State the read-only boundary in the assignment; use a read-only agent type if provided. Check the resulting workspace state. A prompt alone does not enforce permissions. |
| `run_in_background` | Use native asynchronous execution and completion notifications. |
| `resume` | Use native follow-up/resume if offered, otherwise start a new delegate with the earlier result and relevant context. |
| `file_attachments` | Include absolute file paths and the required excerpts/context in the brief. |
| `environment: local/cloud`, `cloud_base_branch` | Use the supported local workspace/worktree mechanism when appropriate; give the exact base revision. A local worktree does not provide Cursor cloud-agent services. |

The installer generates native TOML agents for both named agents and every
workflow role. Defaults inherit the parent model and effort. Follow
[native agents and models](../../../docs/codex/agents-and-models.md) for dispatch,
validated role choices, panel fan-out, native reasoning settings, ownership and
backups. `scripts/pstack_codex.py models` queries the runtime instead of guessing
model slugs. Saved choices live in `~/.config/agent-skills/pstack-models.json`;
installed TOML files apply them natively. The shared AGENTS.md and global model
configuration stay untouched.

## setup-pstack in Codex

Replace the upstream `.mdc` procedure with the concrete JSON/native-agent setup
in [the model guide](../../../docs/codex/agents-and-models.md). Discover models,
resolve budget and role choices, preview `configure`, get the selected workflow's
confirmation, then apply. Keep its optional verification-skill offers within the
user's setup request. Different GPT variants can supply separate runs; they do
not reproduce the upstream Claude/Grok cross-provider diversity. If delegation
is unavailable, do the bounded work directly and state that no independent or
parallel agent ran.

## Paths, history, and generated skills

Map `.cursor/skills/` and generated verification skills to the product project's
`.agents/skills/`. User skills are under `~/.agents/skills/`. Follow the current
repository's instruction locations instead of creating Cursor rule files.
For model roles use the native-agent setup above. Keep user preferences in their
owning source; persist memory only when the user asks.

For recall, correct, automate-me, reflect, and other history consumers, follow
[the history integration](../../../docs/codex/history.md). Use supplied context
or native chat tools first. When summaries omit needed tool evidence, the helper
uses project-filtered `thread/list`, metadata-first `thread/read`, and paginated
`thread/turns/list` with full persisted items. Preserve project checks and cursor
coverage; report omitted/compacted evidence. Do not guess storage paths or read
another project's transcripts.

## Monitoring and unavailable services

Follow [native monitoring](../../../docs/codex/monitoring.md) for one-shot checks,
active drive, native chat heartbeats, deduplicated observations and terminal
cleanup. The helper reuses the upstream watcher and validates its target/output;
readiness is not inferred from a green check list. Native Goal mode requires an
explicit goal request. A future watch uses the native scheduling tool rather
than assuming a shell loop persists across turns.

Benny's 12 source files and three internal skills are preserved, outside the
installed catalog. Its Cursor Automations scheduler, webhook/state API, Slack
integration and secret handoff have no bundled Codex implementation. Preserve
the requested goal, but report that prerequisite before dependent setup or work.
Never register a fake automation, send a message, or request secrets to simulate it.
The same limit applies to make-bot-ui: `update_state` routine creation,
`api2.cursor.sh/automations` webhooks, and `SendToUser` secret-request cards are
Cursor services. A native Codex reminder does not implement that webhook API.

Cursor cloud-agent dashboards and Cursor model-entitlement APIs are unavailable
through this adapter. Bugbot review comments already present on a forge can be
reviewed using authorized forge tools; starting or configuring Bugbot needs the
actual integration. For unsupported optional steps, report the skipped step and
reason, then continue independent work. When a missing capability prevents the
requested outcome, report it as incomplete with the concrete prerequisite;
do not claim success or silently replace it with a weaker proof.
