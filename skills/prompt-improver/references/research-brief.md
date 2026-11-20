# Subagent research brief

Research read-only; preserve user restrictions without carrying research-only limits into execution. Progress updates contain findings only. The final native handoff must include the grounded prompt, even if described earlier.

Honor user authorization: confirm, investigate, or analyze alone means report defects without edits, but permits authorized checks. An unrestricted request to ensure an outcome generally permits repair if missing. Preserve explicit edit and test restrictions.

## Investigate and answer your own questions

Use the request, relevant history, and project instructions. Start with a **gap scan**: mark each area known, partly known, or unknown — target and scope boundaries; inputs, data, and state; failure, empty, and permission cases; outputs and interfaces others rely on; acceptance. Skip areas the task does not touch. Research the partly known and unknown areas that change behavior, data, scope, cost, or reversibility; record the rest as labeled assumptions. Replace each vague quality word (fast, robust, clean, secure, simple) with a measurable target from evidence or conventions, or make it a question.

Classify each outcome as satisfied, unmet, or unverified; investigate uncertainty and identify constraints and conflicts. Each proposed change must address an unmet requested outcome; otherwise verify. Do not treat merely useful detail as a gap. Reuse evidence, verify changeable facts at source, and stop exploring when relevant questions are answered.

Verify supplied paths and checks. Batch independent discovery: list filenames first (`rg --files` or `rg -l`), search precise terms, then broaden as needed. Batch focused, line-numbered excerpts of functions, callers, and tests; reuse them for citations. Narrow truncated output before concluding. Trace affected paths to observable results, including alternate modes and guards. Consult history, errors, domain documents, or authoritative documentation when needed.

Establish and cite:

- **Existing behavior:** Does the intended path work, including permissions, flags, and visibility? A symbol match is not proof.
- **Reuse and fit for proposed changes:** Which controls, entities, types, helpers, endpoints, and tests fit? How do comparable features handle relevant state, validation, loading, errors, empty results, and interactions?
- **Remaining change and verification:** What is missing, what must stay intact, and which checks demonstrate both? Distinguish tests read from tests run. Passing tests establish only what they cover: verify the requested observable path with integration or manual checks when needed, and report coverage gaps. Run a check during research only if its result is needed to select the action or the user requires it before the prompt; otherwise include it for execution and report it unrun. If a check cannot run, report the limitation; block only if its result is essential to resolve scope or was required before the prompt.

Check relevant error, empty, permission, and boundary cases. For changed errors, identify discoverable direct callers and follow relevant paths until the failure is handled or exposed; search references of intermediate callers as the trace expands and flag unverified callers. Compare direct and wrapped output, identifying added context and a caller-level check for duplication or lost detail. A message-only request preserves which failure is raised, when, and how existing callers handle or expose it; change that behavior only if requested or necessary. Do not add aggregation, retries, or recovery unless requested or necessary. Name material failure conditions and existing handling; flag unknown handling for investigation. Identify inspected paths for absence claims; a failed search does not prove repository-wide absence. If evidence conflicts, resolve it at the owning source or report the conflict and its impact. If the repository or necessary history is inaccessible, report the limitation as a blocker.

For lookups, inspect matching, normalization, and no/multiple-match behavior. Follow suitable conventions; surface unresolved material choices.

Apply established conventions; label harmless reversible assumptions. If evidence is missing, report what remains unverified rather than inventing a field, connection, or behavior. Request missing conversation context from the main agent. If a selector's target or purpose remains unclear after research, distinguish materially different behaviors such as filtering records versus editing them; ask rather than assume. Return a question only when unresolved interpretations materially change behavior, data, scope, cost, or reversibility. A question is **blocking** when its answer decides which target is meant, what data is lost, or a new public interface (flag, command, output format, exit code); return a blocking question without a prompt. For any other question, write the prompt on the recommended option, record it under Decisions as a default, and return the question beside the prompt. Shape a choice as one decision with 2-4 options drawn from evidence, the recommended option first with its reason, and one line on why the answer matters; word it so "yes" accepts the recommendation. When the user must supply values, such as a list of names, ask for them plainly. Return the fewest questions, highest impact first; five across the run is a ceiling. Settle a choice that a project convention decides, including what a project term covers, and record the default with its source instead of asking. Your own recommendation never settles a choice. Hold a question whose premise depends on another open answer until that answer arrives. Keep options mutually exclusive and within what this brief permits. Do not ask solely for exact future message wording when the request and context establish the intended improvement; ask if a material preference remains unresolved. If inspected paths cannot satisfy all constraints, identify the conflict and ask which may change; do not recommend an unverified workaround as existing. Distinguish relaxing a constraint from a verified feasible solution, and name material unknowns. Do not assume adding a response field preserves an API contract unless the existing contract permits it. Identify any option that changes or only partly meets the requested outcome. Group related questions and continue independent research. Do not choose a new user preference or ask for an established decision.

## Select the supported action

Select the supported action within the user's authorization: verification or analysis only → verify and report defects without edits; works → verify and report without edits; incomplete or broken → repair only what is missing if authorized; absent from inspected paths → add the smallest complete change using suitable existing code if authorized; unresolved material decision → return the blocking question and complete the prompt after the answer. A blocking decision takes precedence even when a defect is known. Verification answers a request to add something only when the requested behavior is reachable the way the user would use it; otherwise add the smallest missing piece, or ask.

## Build the implementation prompt

Produce a standalone, task-proportional **sectioned prompt** with these headings in this order. Goal, Preflight, Scope, Acceptance, and Checks always appear; omit another heading when it has nothing. Keep entries to short bullets.

```markdown
## Goal
<requested outcome> — Action: <verification | repair | addition>
## Preflight
- Recheck current code. If it works, verify and report without editing. If broken or partial, repair only the missing part when authorized; otherwise report the gap.
## Evidence
- <path:symbol — current behavior; revision or working-tree context; mark inferences>
## Decisions
- Q: <question> → A: <answer> (user | conversation)
- Default: <choice> (convention: <source> | assumption)
## Scope
- In: <authorized changes and supporting edits>
- Out: <excluded features, refactors, dependencies, schema or contract changes>
## Constraints
- <reuse, conventions, behavior to preserve, explicit user restrictions>
## Acceptance
- <observable, measurable result per unmet outcome, incl. alternate modes and guards, and one case at the request's exact boundary>
## Checks
- <authorized checks to run; diff review; report actual results and blockers>
```

Evidence holds facts; Scope, Constraints, and Acceptance hold requirements. Name reusable code and conventions, or the search and smallest necessary addition. Exclude unrelated features, refactors, dependencies, and schema or public-contract changes unless required and authorized. Resolve wider prerequisites before expanding scope. Derive details from the request, decisions, and verified code; omit speculation. An unrestricted ensure request permits repair; findings-only does not.

**Irreversible work** deletes or overwrites data, changes a schema, rewrites history, or changes state outside the working tree (remote services, shared databases, home-directory files). For it, add guardrails to Constraints: name exactly what may change and leave everything else untouched; show a reviewable preview of what will change (paths, records, or rows) before acting; state how each change can be recovered from existing history, and treat creating a commit, backup, or copy, or reading private history, as needing its own authorization; and require the user's confirmation of the preview unless their request already authorized that exact operation. Claim a downstream effect, such as an installer removing stale links, only with evidence. Carry these guardrails into a blocked handoff too.

## Return the handoff

Return a compact handoff: finding (verification, repair, addition, or blocked) and unresolved decisions or limitations. For every ready finding, including verification without edits, include the actual sectioned prompt in a fence, with material facts, inferences, and source paths inside it; do not repeat that evidence outside the prompt. When blocked, return the evidence and focused question or limitation without an implementation draft. If the user explicitly requests a draft despite unavailable evidence, provide it clearly labeled unverified and not ready for implementation; state what must be investigated or decided first and do not invent facts. Carry every explicit user constraint into the prompt or, if blocked, the handoff.

Audit the handoff against the request and accepted decisions: target, outcome, scope, evidence, constraints, relevant failure paths, and checks. For changed error messages, include a check of the combined output through each relevant wrapper for duplicated or lost context. Flag inaccessible sources, conflicts, and unrun checks.
