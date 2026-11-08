---
name: manual-qa
description: 'Manual workflow: Test realistic user journeys and edge cases with native Codex Computer Use, track every case, and report observed bugs with evidence.'
disable-model-invocation: true
---

Use only when explicitly selected, for the requested QA task. Preserve project requirements and authorization. Deliver findings and coverage; product changes need authorization and other workflows need separate selection.

# Manual QA

Execute finite cases through the real interface. Plans, simulations and source/API checks are not UI execution. Attribute imported results separately from your observations.

Local fork provenance: `upstreams.json`; licenses: `licenses/`.

## 1. Resolve

Read [context and access](references/context-and-access.md). Apply its target decision table before runnable cases; resolve environment/build, surface/session, role, scope, expectations, authority, destination and budget independently. Reuse settled fields. Verify destination before credentials/mutations and role after sign-in. Ask only unresolved material fields, with the affected cases and a supported recommendation/tradeoff; continue independent work.

A plan may reference an explicitly supplied oracle without copying its text. Retrieve that source for execution; ask only if retrieval actually fails. Use requirements, accepted decisions and product/domain documentation, not current behavior or product source, as correctness criteria. Unstated contracts stay unknown: retry availability establishes no draft-retention rule. Clarify required assertions or record observations without a verdict.

## 2. Plan or reconstruct

Use one ledger from the [report template](templates/manual-qa-report-template.md), in the requested destination or a fresh `qa-output/` run in the target project (task workspace if none). Preserve earlier runs; keep report/evidence together and update incrementally.

**New testing:** show a finite plan before execution, without another approval gate. Each case needs an ID, priority, starting state, actions/nonsecret data and observable expectation. Map scoped requirements and unavailable coverage; prioritize core/high-impact journeys within budget without reducing requested breadth to smoke coverage. Use [the issue checklist](references/issue-taxonomy.md). Include returning-user/persistence checks, alternate/bulk entry points, refresh/navigation/recovery and relevant input, role, keyboard and layout boundaries. For forms, cover required fields' empty/invalid states and correction before optional formats. Distinguish invalid input from valid-but-unfulfillable requests; queued/stateful flows need successive edits and the specified final ordering/state. Add discovered cases before executing them; group shared variants while retaining each outcome.

**Reporting supplied results:** retain original IDs, boundaries, outcomes and retries before proposing anything new. Reconstruct only supplied coverage; label reconstructed IDs and original planned total (unknown unless supplied). An extra chart comparison, replay or excluded action is not another historical case. Keep proposed checks and exclusions outside run counts. Required new-testing recovery belongs in that plan, not an optional follow-up. New plans need no historical-total boilerplate.

## 3. Execute and classify

Read [computer interaction](references/computer-interaction.md) before the first UI action. Use available native tools; unavailable control blocks dependent cases rather than justifying scripts/HTTP substitutes.

For each case, verify preconditions through UI; isolate roles/fresh-user state while preserving returning-user data and user-owned sessions. Reset only authorized owned test state. Observe, act through visible controls, wait, then inspect all required feedback and downstream state. A click/toast or absent error does not establish persistence. Record actual actions, outcomes and evidence immediately.

| Status | Decision |
|---|---|
| `PASS` | All case actions executed and established expected product behavior observed. |
| `FAIL` | Observed discrepancy against an established expectation; later passing retries retain FAIL. |
| `BLOCKED` | A known prerequisite prevents completion, or a known interruption leaves required steps/outcomes incomplete. Preserve partial observations and block confirmed dependents. |
| `NOT RUN` | Unattempted or explicitly unchecked coverage, including budget/deferral; give the reason. Missing observations alone establish no blocker. |

For imported reports, preserve explicit outcomes. Executing an observation sequence with an unresolved required oracle is BLOCKED, not PASS. A stated missing verification oracle (such as an absent authoritative totals source) BLOCKS that assertion; lack of an observation alone does not. “Focus not observed” or “keyboard unattempted” stays NOT RUN unless the record identifies a preventing prerequisite. Do not invent missing access or an oracle to reclassify historical coverage. By contrast, a save interrupted before required reload is one BLOCKED case: the toast is partial evidence, not a new PASS. Separately supplied component PASS and static-review FAIL survive blocked downstream journeys.

Preserve evidence before reset. Inspect committed state before replaying writes; retry safely from verified preconditions, keeping attempts within their case and marking replay-confirmed, intermittent or observed once. Stop unsafe replay; continue independent cases. Unknown causes stay unknown: unavailable upload does not establish a missing fixture. Preserve ledger, evidence, changed state and resume point on interruption.

## 4. Reconcile and report

Finish scoped cases or state the real blocker/budget limit. Derive all summary counts once from the final ledger: `PASS + FAIL + BLOCKED + NOT RUN = known ledger total`; completed cases = PASS + FAIL. Count partial attempts separately. Original planned total may remain unknown. Separate case counts from issue counts; link each FAIL to an issue, allowing shared findings.

For each issue record impact-based severity/category, affected IDs, sanitized target/preconditions, expected versus actual, numbered actual reproduction steps, evidence and confirmation limits. Missing steps/inputs remain unknown; do not invent bugs, causes or artifacts. Optional cause hypotheses must be explicitly unverified. Capture relevant states and the broken result; a screenshot may suffice for static findings. Video is optional; unsupported/unsafe capture is a stated gap. Sanitize before saving/sharing; if safe capture is impossible, retain sanitized observations without inventing evidence.

Record last observed state and actual cleanup; an opened tab does not prove it remains open. Unobserved final state stays unknown. Restore only authorized owned test state; retain evidence and user sessions. Blocked/unrun cases and deferrals keep coverage incomplete; passing scoped cases never proves the app bug-free. Product fixes, commits, publication, sends and other external actions require their own authorization.

Keep output compact through shared setup and one ledger, not fewer cases. State provenance once, reference it thereafter; give issue/reproduction detail once. Omit repeated case summaries and unchanged/null setup fields. Return report path, counts, findings, gaps and resume point; put detailed cases in the report rather than duplicating them in chat.
