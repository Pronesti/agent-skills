---
name: manual-qa
description: 'Manual workflow: Test realistic user journeys and edge cases with native Codex Computer Use, track every case, and report observed bugs with evidence.'
disable-model-invocation: true
---

Use this workflow only when the user explicitly selects it. Apply it to the requested QA task. Other named workflows need separate selection; declared supporting references may be read as needed. Preserve project requirements and existing authorization.

# Manual QA

Systematically use the application as a customer would. Prepare a case list, execute the cases through the real interface, and report observed results with reproduction evidence. The output is QA findings and coverage; product changes require separate authorization.

Local fork: adapted for native Computer Use, context-derived setup, and case-based completion. Source revision and original file mappings are preserved in the repository's `upstreams.json`; its upstream license is preserved in `licenses/`.

## 1. Resolve setup from context

Read [context and access](references/context-and-access.md) before opening the target. Resolve the target URL or app, environment, browser, sign-in, scope, exclusions, and any execution budget from the calling prompt, relevant earlier messages, and supplied project context. The latest explicit user instruction takes precedence for each field; keep earlier instructions that still apply. Ask only when a necessary value is missing or materially conflicting.

Briefly state the resolved target, scope, and account role without exposing credentials. Use the existing authorized session or supplied test credentials under the host's rules. A source link or ambient browser tab is not automatically the application under test.

## 2. Initialize and orient

Use native Codex browser or computer tools already available in the session. Read [computer interaction](references/computer-interaction.md) before the first UI action. Work sequentially in the chosen app or browser session; competing agents must not drive that same surface. If native control is unavailable, report the affected coverage as blocked rather than silently replacing UI QA with scripts or HTTP requests.

Use the user's output destination when supplied. Otherwise create a fresh run directory under `qa-output/` in the target project, or in the task workspace when no project is available. Keep screenshots and the report together. Start from [the report template](templates/manual-qa-report-template.md); preserve previous runs and update this run incrementally.

Open the resolved target, complete authorized sign-in if necessary, and verify the actual account role and environment. Capture the starting screen and inspect visible navigation and controls. Read [the issue checklist](references/issue-taxonomy.md) to calibrate categories, severity, and exploration coverage.

## 3. Plan the cases before testing

Build a finite case list for the resolved scope and show it to the user before execution. This is informational, not an additional approval gate. Use explicit requirements, accepted conversation decisions, existing manual QA plans, and observed UI to define expected results. Product or domain documentation may establish intended behavior; keep product source inspection out of the user-facing QA pass. If a meaningful expectation is unresolved, ask or record that case as blocked rather than treating current behavior as the specification.

Give each case an ID, starting state or preconditions, user actions and test data, expected observable result, and priority. Match the number of cases to the feature and its risks; do not reduce a multi-case request to a single smoke check.

Select applicable cases from these families:

- Normal end-to-end journeys and returning-user journeys.
- Empty, valid, invalid, boundary, long, and unusual inputs where relevant.
- Empty results, loading, visible error feedback, and recovery.
- Interactions between controls, state changes, refresh, Back/Forward, and repeated or rapid actions.
- Signed-out behavior, roles, and permissions when authorized accounts are available.
- Keyboard navigation, focus, layout, and supported viewport sizes.

Use realistic values and user goals. List relevant cases that cannot be reached with the supplied accounts, data, environment, or tool capabilities; unavailable coverage does not vanish from the plan. Keep unrelated pages and speculative features outside the agreed scope. Add newly discovered in-scope cases to the ledger before running them.

## 4. Execute as a user

Work through the planned cases. For each case:

1. Establish and verify its starting state. Use visible UI to reset state or owned test data within authorization. Reuse a known session when the case requires it; isolate roles or fresh-user scenarios when needed. Never clean up someone else's data to obtain a fresh state.
2. Observe the current screen, act through visible controls, wait for the relevant state, and verify the expected outcome. Use fresh UI state after navigation or rendering changes. Inspect feedback, loading, errors, and whether a user can understand and recover from the result.
3. Capture evidence and update the ledger immediately. Record `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`, with observed result and evidence or a reason. Only actual execution of the stated actions and observation of the expected outcome can produce `PASS`.
4. On failure, document it before continuing. Retry from the relevant starting state when safe to distinguish repeatable and intermittent behavior. Preserve observed-once findings with their limits; inability to reproduce again does not erase the original observation.
5. Continue independent cases after failures. Mark dependent cases blocked when their prerequisite fails, then move to cases that can still run. A safety, environment, or budget stop must identify all remaining cases and why they were not run.

Use the browser's console or network evidence as supplementary diagnostics only when the native tools expose them within existing permissions. UI evidence remains necessary for user-facing outcomes. Do not bypass the interface with API calls, database writes, script-driven product state, or product-source inspection to claim a user journey passed.

## 5. Document issues with reproduction evidence

Give each issue an ID and link its affected case IDs. Record severity, category, sanitized target, starting state, expected result, actual result, numbered user actions, evidence, and whether it was replay-confirmed, observed once, or intermittent. Separate visible symptoms from an unverified cause.

For interaction problems, capture the starting state, important actions, and broken result with screenshots and clear steps. Record a video only when the native tool supports it and it helps explain timing or interaction; otherwise disclose that limitation and retain screenshots and steps. For static problems, one clear screenshot can be sufficient. Pace reproduction for a human reader; use character-by-character input when that behavior matters, and condition-based waits instead of arbitrary delays.

Write findings as they occur. Preserve screenshots, videos, case results, and earlier observations if interrupted. Mask secrets before saving evidence; a screenshot with hidden input values can still expose a token in a URL or another part of the screen.

## 6. Reconcile coverage and finish

Account for every planned case. Counts must match the ledger and issue entries. A complete pass has executed all required cases; blocked and unrun cases make coverage incomplete, even if every executed case passed. Explicit user-approved deferrals remain visible. State environment and tooling limits, remaining cases, and a resume point when appropriate.

Finish when the agreed cases are executed or a real blocker or supplied budget prevents further work. Never use a target number of bugs as the stopping rule, invent defects to reach a quota, or conclude that the application is bug-free from a partial pass.

Restore temporary UI state and clean up only owned test artifacts or data where the task authorizes it; preserve report evidence. Close only tabs or sessions opened for this run when appropriate, leaving user-provided sessions intact. Return the report path, executed/total case counts, result counts, key findings, and coverage gaps. Further fixes, commits, tracker publication, and external actions follow the user's actual authorization.
