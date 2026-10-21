# Native Codex integration verification — 21 October 2026

Implemented locally on `feat/pstack-only`. No commits, pushes, PRs, merges,
live-home installation, real PR changes or persistent automations were made.
Benny and the webhook service remain deferred; all upstream files stay intact.

## Implemented behavior

- Installation generates 23 native TOML agents by default: the two named agents
  and the role/panel entries. Default models and effort inherit. Ownership,
  backups, collision checks and repeat-install behavior cover the native files.
- Model setup uses native `model/list`, validates supported models/efforts, and
  saves resolved role choices plus native agent settings. It leaves the user's
  parent model, provider, permissions, MCP configuration and shared AGENTS
  template unchanged. Legacy Markdown choices are detected and preserved.
- History uses project-filtered native list/read APIs and full persisted item
  pages, with project checks before turn hydration. It supports cursors,
  archives, exclusions and explicitly selected sibling Git worktrees.
- Monitoring executes the unchanged upstream watcher with bounded arguments,
  verifies the target and result, records state atomically, suppresses pending
  churn and duplicates, and signals readiness/closed termination. The workflow
  guide integrates native chat heartbeats and explicit Goal mode without making
  a shell watcher into a pretend persistent service.

## Verification

| Check | Result |
| --- | --- |
| Repository suite | 61 tests passed |
| Catalog/provenance validation | 56 entrypoints, native TOML/roles and supporting references passed |
| Upstream snapshot | All 172 original files still match their recorded checksums |
| Native model discovery | Available models/efforts returned through the installed runtime |
| Authenticated native-agent test | Two real configured roles completed in an isolated App Server profile |
| Actual model setting | Runtime metadata confirmed `pstack-how-explorer` used fixture-selected `gpt-6-luna`, `medium` effort |
| Workflow outputs | Explorer explained the fixture's sum calculation; Comment Sicko identified its redundant comment; both cited the fixture |
| Read-only behavior | Fixture remained unchanged; disposable profile removed |
| Native history | Full persisted items verified in the test; a separate project-scoped read of this chat also returned full items and an older-page cursor |
| Monitoring execution | Real upstream Bun watcher against a local forge fixture returned `READY`; first notification decision true, duplicate false, stop true |
| Live monitoring side effects | Zero live forge calls or persistent scheduled tasks in the smoke test |
| Shared infrastructure | AGENTS template, runtime detection, instruction-sync implementation, install.sh and update checker remain byte-identical to main |
| Working tree checks | Whitespace validation passed; original main checkout and its unrelated untracked report preserved |

Runtime tested: `codex-cli 0.163.0-alpha.11`. Native agents were verified through
the live App Server's child metadata and persisted output, rather than relying
on the parent agent's summary. An ephemeral CLI parent cannot provide the saved
context needed by subagents in this runtime. Completed child metadata also need
not appear in a separate App Server's history-list process; the test observes
the same live server connection.

The new tests run with:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 tests/native_codex_smoke.py
python3 tests/native_monitor_smoke.py --bun /path/to/bun
```

The authenticated smoke test uses a temporary copy of CLI authentication inside
a disposable profile, never prints credentials, and removes the profile after
the run. It starts bounded model turns; ordinary unit tests do not. The monitor
test uses the original locked watcher dependencies in a temporary package and
a local fake forge command, with no network requests to a real pull request.

Native scheduling is integrated through workflow instructions and a generated
targeted prompt; no live watch was scheduled because this implementation task
specified no PR or cadence. Native Goal mode still requires an explicit goal
request. Local background watches require the machine and app running. Source
preservation and these representative workflows are verified; all 56 workflows
were not exercised end to end. Cross-provider Claude/Grok diversity, Benny,
arbitrary webhooks and Cursor-only services remain outside this implementation.

Native formats and APIs follow the official [custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[App Server protocol](https://learn.chatgpt.com/docs/app-server), and
[scheduled-task behavior](https://learn.chatgpt.com/docs/automations).
