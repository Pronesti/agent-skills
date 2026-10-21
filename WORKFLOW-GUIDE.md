# pstack workflows in Codex

Select a workflow explicitly. These are entrypoints into the complete pinned
[pstack guide](pstack/README.md); the [Codex adapter](pstack/docs/harness/codex.md)
applies to all of them.

| Goal | Entrypoint |
| --- | --- |
| Route a feature, bug fix, investigation, refactor, or shipping request | `$poteto-mode` |
| Find the right workflow or understand the package | `$poteto-help` |
| Explain implementation and ownership | `$how` |
| Explain motivation and decisions | `$why` |
| Explore competing implementations | `$arena` |
| Divide authorized parallel work | `$swarm` |
| Review a design or diff from multiple perspectives | `$interrogate` |
| Check what a small change might break | `$blast-radius` |
| Prove observable application behavior | `$create-verification-skill`, then the generated project skill |
| Capture a reviewable decision trail | `$show-me-your-work` |
| Configure supported model roles | `$setup-pstack` |

The full [catalog](MANIFEST.md#catalog) also includes all upstream principles and
specialized verification, writing, and review skills. The 23 playbooks remain in
[pstack/skills/poteto-mode/playbooks/](pstack/skills/poteto-mode/playbooks/).

Codex uses native subagents when offered and authorized. Model settings default
to inheritance; a same-model review is not a diverse-model panel. History access
uses supplied context or native chat tools, with project scope checked first.
Benny and other Cursor-only services are retained as source and reported as
unsupported prerequisites when needed. See the adapter for exact mappings.

This branch preserves all upstream files. It does not prove that every workflow
produces equivalent results across hosts. Automated checks cover source
preservation, skill packaging, installation, backups, runtime setup, and policy.

Native implementation guides: [agents and models](docs/codex/agents-and-models.md),
[project history](docs/codex/history.md), and [monitoring](docs/codex/monitoring.md).
