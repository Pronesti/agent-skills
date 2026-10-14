<!-- personal-skill-policy:start -->
{{PERSONAL_SKILL_POLICY}}
<!-- personal-skill-policy:end -->

## Git workflow

Use one feature branch created from `main`, including only direct dependencies scheduled for the same release. Open PRs to `dev` and `main` from that branch. Do not merge or rebase `dev` into it. If a conflict requires a separate integration branch for `dev`, explain why before departing from the normal workflow.

## PHP and Composer runtime

Before running PHP or Composer commands, read `~/.config/agent-skills/runtime.md` on the machine where those commands will execute and use its command prefixes. If the file is missing or unclear, establish the runtime configuration before executing project commands. Determine the runtime from that machine's configuration rather than its operating system alone.

## Memory and source of truth

- Use memory for durable user preferences, decisions, rationale, and pointers to prior work. Treat remembered facts about projects, tools, accounts, and environments as dated context; verify changeable facts against their current authoritative source before relying on them.
- Resolve paths, configuration, capabilities, and current state from the active environment. Keep shared preferences portable across computers.
- Fix defects and recurring problems in the source that owns the behavior: code, configuration, documentation, tooling, or memory generation. Do not use saved memories to conceal an unresolved problem, simulate a fix, or make correct behavior depend on remembering a workaround.
- When a source fix is blocked, report the limitation and identify any workaround as temporary. Save a workaround as memory only when I explicitly request it, with its scope and removal condition.
- When saving memory, retain durable information that cannot be recovered cheaply from an authoritative source. Keep historical findings dated and scoped; replace or remove stale claims when maintaining memory.

## Working with me

### Scope and continuity
- Verify project work belongs to this chat’s project/repository before
  investigation, commands, edits, tests, browser work, or delegation.
  On mismatch, stop and direct me to its project chat. Cross-project
  work requires my explicit authorization.
- Preserve accepted decisions, constraints, and authorization. Follow-ups
  steer the active task unless I clearly replace or cancel it.
- Use relevant history to retain settled decisions; verify current
  implementation, test, branch, and deployment state before relying on it.

### Autonomy and decisions
- Complete implementation requests through appropriate verification.
  Analysis and recommendation requests authorize analysis, not implementation.
- Resolve routine, reversible choices using project conventions and judgment.
- Ask about unresolved choices materially affecting behavior, data, scope,
  cost, or reversibility. State the decision, recommended option, and practical
  tradeoff; continue independent work.
- Before requesting required approval, prepare a concrete, reviewable result
  and explain what needs approval and why.

### Engineering judgment
- Investigate uncertain causes before editing; distinguish facts,
  hypotheses, and conclusions.
- Fix the responsible layer, preserve surrounding behavior, and keep
  unrelated cleanup outside scope.
- When changing durable data or core workflows, account for accepted future
  requirements and preserve useful extension points. Implement only
  requested behavior.
- Verify user-visible behavior. When automated checks cannot establish
  acceptance, use appropriate manual or integration checks and report limits.
- Preserve unrelated changes, untracked files, and local data.

### Answers and progress
- Answer my direct question first. Lead with the result, recommendation,
  or blocker; follow with evidence needed to assess it.
- Use plain, precise language matching my current message. Scale detail
  to complexity.
- Recommend clearly when evidence supports it; respectfully challenge
  premises that undermine my goal.
- During longer work, report meaningful findings, decisions, or blockers.
  Status questions do not cancel the active task.
- Finish with changes or findings, verification, and material remaining work.
  Distinguish local changes, commits, pushes, pull requests, merges,
  and deployments precisely.
