# Skill groups

All 66 repository-owned skills are divided into 18 functional groups, each containing 3–5 skills. Prefixes appear in `interface.display_name` in each skill’s `agents/openai.yaml`. Existing skill IDs, directories, invocation policy, and supporting references stay compatible. Host-owned skills outside this repository are outside this catalog.

Standalone installations linked to this repository pick up the metadata after discovery refresh. The Caveman source version is `2.7.0+selective.20261006`; installed plugin copies need updating through their host to load these labels.

| Prefix | Skills | Purpose |
|---|---:|---|
| Interview: | 4 | Clarify decisions through questions. |
| Planning: | 5 | Explore requirements and plan work. |
| Architecture: | 4 | Model domains and improve code structure. |
| Implementation: | 5 | Build features and prototypes with appropriate scope. |
| Execution: | 3 | Carry out plans inline or with selected delegation. |
| Maintenance: | 4 | Refactor, migrate, and patch existing behavior. |
| Testing: | 3 | Develop test-first and verify acceptance conditions. |
| Debugging: | 3 | Investigate failures and regressions. |
| Review: | 4 | Review code and assess change impact. |
| Delivery: | 4 | Organize tickets and complete branch integration. |
| Exploration: | 4 | Research questions and understand repositories. |
| Teaching: | 3 | Explain concepts clearly and visually. |
| Writing: | 3 | Create and improve technical and agent documentation. |
| Compression: | 3 | Use concise communication and compress text. |
| Context: | 3 | Recover, record, and transfer working context. |
| Setup: | 5 | Discover skills and configure workflow tools. |
| Optimization: | 3 | Apply cost improvements and manage experiments. |
| Measurement: | 3 | Discover workflows and inspect usage evidence. |

## Interview (4)

Clarify decisions through questions.

| Invocation name | Display name |
|---|---|
| `grill-me` | [Interview: Grill Me](../skills/grill-me/SKILL.md) |
| `grill-with-docs` | [Interview: Grill with Docs](../skills/grill-with-docs/SKILL.md) |
| `grilling` | [Interview: Grilling](../skills/grilling/SKILL.md) |
| `to-questionnaire` | [Interview: To Questionnaire](../skills/to-questionnaire/SKILL.md) |

## Planning (5)

Explore requirements and plan work.

| Invocation name | Display name |
|---|---|
| `brainstorming` | [Planning: Brainstorming](../skills/brainstorming/SKILL.md) |
| `prompt-improver` | [Planning: Prompt Improver](../skills/prompt-improver/SKILL.md) |
| `to-spec` | [Planning: To Spec](../skills/to-spec/SKILL.md) |
| `wayfinder` | [Planning: Wayfinder](../skills/wayfinder/SKILL.md) |
| `writing-plans` | [Planning: Writing Plans](../skills/writing-plans/SKILL.md) |

## Architecture (4)

Model domains and improve code structure.

| Invocation name | Display name |
|---|---|
| `architecture-patterns` | [Architecture: Architecture Patterns](../skills/architecture-patterns/SKILL.md) |
| `codebase-design` | [Architecture: Codebase Design](../skills/codebase-design/SKILL.md) |
| `domain-modeling` | [Architecture: Domain Modeling](../skills/domain-modeling/SKILL.md) |
| `improve-codebase-architecture` | [Architecture: Improve Codebase Architecture](../skills/improve-codebase-architecture/SKILL.md) |

## Implementation (5)

Build features and prototypes with appropriate scope.

| Invocation name | Display name |
|---|---|
| `caveman:lean-build` | [Implementation: Lean Build](../plugins/caveman/skills/lean-build/SKILL.md) |
| `implement` | [Implementation: Implement](../skills/implement/SKILL.md) |
| `incremental-implementation` | [Implementation: Incremental Implementation](../skills/incremental-implementation/SKILL.md) |
| `ponytail` | [Implementation: Ponytail](../skills/ponytail/SKILL.md) |
| `prototype` | [Implementation: Prototype](../skills/prototype/SKILL.md) |

## Execution (3)

Carry out plans inline or with selected delegation.

| Invocation name | Display name |
|---|---|
| `caveman:cavecrew` | [Execution: Cavecrew](../plugins/caveman/skills/cavecrew/SKILL.md) |
| `executing-plans` | [Execution: Executing Plans](../skills/executing-plans/SKILL.md) |
| `subagent-driven-development` | [Execution: Subagent Driven Development](../skills/subagent-driven-development/SKILL.md) |

## Maintenance (4)

Refactor, migrate, and patch existing behavior.

| Invocation name | Display name |
|---|---|
| `caveman:migration` | [Maintenance: Migration](../plugins/caveman/skills/migration/SKILL.md) |
| `caveman:safe-refactor` | [Maintenance: Safe Refactor](../plugins/caveman/skills/safe-refactor/SKILL.md) |
| `caveman:surgical-patch` | [Maintenance: Surgical Patch](../plugins/caveman/skills/surgical-patch/SKILL.md) |
| `code-simplification` | [Maintenance: Code Simplification](../skills/code-simplification/SKILL.md) |

## Testing (3)

Develop test-first and verify acceptance conditions.

| Invocation name | Display name |
|---|---|
| `caveman:verify-and-stop` | [Testing: Verify and Stop](../plugins/caveman/skills/verify-and-stop/SKILL.md) |
| `tdd` | [Testing: TDD](../skills/tdd/SKILL.md) |
| `test-driven-development` | [Testing: Test Driven Development](../skills/test-driven-development/SKILL.md) |

## Debugging (3)

Investigate failures and regressions.

| Invocation name | Display name |
|---|---|
| `caveman:investigate-first` | [Debugging: Investigate First](../plugins/caveman/skills/investigate-first/SKILL.md) |
| `diagnosing-bugs` | [Debugging: Diagnosing Bugs](../skills/diagnosing-bugs/SKILL.md) |
| `systematic-debugging` | [Debugging: Systematic Debugging](../skills/systematic-debugging/SKILL.md) |

## Review (4)

Review code and assess change impact.

| Invocation name | Display name |
|---|---|
| `blast-radius` | [Review: Blast Radius](../skills/blast-radius/SKILL.md) |
| `caveman:caveman-review` | [Review: Caveman Review](../plugins/caveman/skills/caveman-review/SKILL.md) |
| `code-review` | [Review: Code Review](../skills/code-review/SKILL.md) |
| `requesting-code-review` | [Review: Requesting Code Review](../skills/requesting-code-review/SKILL.md) |

## Delivery (4)

Organize tickets and complete branch integration.

| Invocation name | Display name |
|---|---|
| `finishing-a-development-branch` | [Delivery: Finishing A Development Branch](../skills/finishing-a-development-branch/SKILL.md) |
| `resolving-merge-conflicts` | [Delivery: Resolving Merge Conflicts](../skills/resolving-merge-conflicts/SKILL.md) |
| `to-tickets` | [Delivery: To Tickets](../skills/to-tickets/SKILL.md) |
| `triage` | [Delivery: Triage](../skills/triage/SKILL.md) |

## Exploration (4)

Research questions and understand repositories.

| Invocation name | Display name |
|---|---|
| `caveman:caveman-explore` | [Exploration: Caveman Explore](../plugins/caveman/skills/caveman-explore/SKILL.md) |
| `how` | [Exploration: How](../skills/how/SKILL.md) |
| `research` | [Exploration: Research](../skills/research/SKILL.md) |
| `why` | [Exploration: Why](../skills/why/SKILL.md) |

## Teaching (3)

Explain concepts clearly and visually.

| Invocation name | Display name |
|---|---|
| `show-me` | [Teaching: Show Me](../skills/show-me/SKILL.md) |
| `teach` | [Teaching: Teach](../skills/teach/SKILL.md) |
| `wait-what` | [Teaching: Wait What](../skills/wait-what/SKILL.md) |

## Writing (3)

Create and improve technical and agent documentation.

| Invocation name | Display name |
|---|---|
| `technical-writing` | [Writing: Technical Writing](../skills/technical-writing/SKILL.md) |
| `unslop` | [Writing: Unslop](../skills/unslop/SKILL.md) |
| `writing-for-agents` | [Writing: Writing for Agents](../skills/writing-for-agents/SKILL.md) |

## Compression (3)

Use concise communication and compress text.

| Invocation name | Display name |
|---|---|
| `caveman:caveman` | [Compression: Caveman](../plugins/caveman/skills/caveman/SKILL.md) |
| `caveman:caveman-commit` | [Compression: Caveman Commit](../plugins/caveman/skills/caveman-commit/SKILL.md) |
| `caveman:caveman-compress` | [Compression: Caveman Compress](../plugins/caveman/skills/caveman-compress/SKILL.md) |

## Context (3)

Recover, record, and transfer working context.

| Invocation name | Display name |
|---|---|
| `handoff` | [Context: Handoff](../skills/handoff/SKILL.md) |
| `recall` | [Context: Recall](../skills/recall/SKILL.md) |
| `show-me-your-work` | [Context: Show Me Your Work](../skills/show-me-your-work/SKILL.md) |

## Setup (5)

Discover skills and configure workflow tools.

| Invocation name | Display name |
|---|---|
| `caveman:caveman-help` | [Setup: Caveman Help](../plugins/caveman/skills/caveman-help/SKILL.md) |
| `caveman:caveman-setup` | [Setup: Caveman Setup](../plugins/caveman/skills/caveman-setup/SKILL.md) |
| `find-skills` | [Setup: Find Skills](../skills/find-skills/SKILL.md) |
| `setup-matt-pocock-skills` | [Setup: Setup Matt Pocock Skills](../skills/setup-matt-pocock-skills/SKILL.md) |
| `wizard` | [Setup: Wizard](../skills/wizard/SKILL.md) |

## Optimization (3)

Apply cost improvements and manage experiments.

| Invocation name | Display name |
|---|---|
| `caveman:caveman-learn` | [Optimization: Caveman Learn](../plugins/caveman/skills/caveman-learn/SKILL.md) |
| `caveman:caveman-manage` | [Optimization: Caveman Manage](../plugins/caveman/skills/caveman-manage/SKILL.md) |
| `caveman:caveman-optimize` | [Optimization: Caveman Optimize](../plugins/caveman/skills/caveman-optimize/SKILL.md) |

## Measurement (3)

Discover workflows and inspect usage evidence.

| Invocation name | Display name |
|---|---|
| `caveman:caveman-discover` | [Measurement: Caveman Discover](../plugins/caveman/skills/caveman-discover/SKILL.md) |
| `caveman:caveman-evidence-review` | [Measurement: Caveman Evidence Review](../plugins/caveman/skills/caveman-evidence-review/SKILL.md) |
| `caveman:caveman-stats` | [Measurement: Caveman Stats](../plugins/caveman/skills/caveman-stats/SKILL.md) |
