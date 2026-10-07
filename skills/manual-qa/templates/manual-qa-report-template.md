# Manual QA Report: {APP_NAME}

| Field | Value |
|---|---|
| Date / build | {DATE_AND_BUILD} |
| Target | {SANITIZED_URL_OR_APP} |
| Environment / browser | {ENVIRONMENT_AND_BROWSER} |
| Account role | {ROLE_OR_NON_SENSITIVE_ALIAS} |
| Scope / exclusions | {SCOPE_AND_EXCLUSIONS} |
| Setup sources | {CALLING_PROMPT_PRIOR_DECISIONS_AND_CONTEXT_REFERENCES_WITHOUT_SECRETS} |
| Execution budget | {USER_LIMIT_OR_SCOPED_CASE_COMPLETION} |
| Coverage | {COMPLETE_OR_INCOMPLETE_AND_REASON} |

## Case ledger

Fill planned cases before execution; then update actual results immediately. A `PASS` requires observed execution and the expected result. `FAIL` records an observed discrepancy. `BLOCKED` identifies an unmet prerequisite; `NOT RUN` identifies an unexecuted case. Expected results remain visible after execution.

| ID / priority | Scenario / starting state | User actions / test data | Expected result | Status | Observed result | Evidence / blocker |
|---|---|---|---|---|---|---|
| {CASE_ID_AND_PRIORITY} | {SCENARIO_AND_PRECONDITIONS} | {ACTIONS_AND_NON_SECRET_DATA} | {EXPECTED} | {STATUS} | {OBSERVED} | {LINK_OR_REASON} |

## Summary

| Cases | Count |
|---|---:|
| Planned total | {TOTAL} |
| Executed: PASS + FAIL | {EXECUTED} |
| PASS | {PASS} |
| FAIL | {FAIL} |
| BLOCKED | {BLOCKED} |
| NOT RUN | {NOT_RUN} |

All four status counts must sum to the planned total. Blocked/unrun coverage and approved deferrals stay explicit.

| Issue severity | Count |
|---|---:|
| Critical | {CRITICAL} |
| High | {HIGH} |
| Medium | {MEDIUM} |
| Low | {LOW} |
| Total | {ISSUE_TOTAL} |

## Issues

Copy this block per finding. Capture key interaction steps and the broken result; a static issue may need only one screenshot. Video is optional when supported. Record observed-once and intermittent findings with their limits.

### ISSUE-001: {SHORT_TITLE}

| Field | Value |
|---|---|
| Cases | {AFFECTED_CASE_IDS} |
| Severity / category | {SEVERITY_AND_CATEGORY} |
| Target | {SANITIZED_PAGE_OR_APP_STATE} |
| Confirmation | {REPLAY_CONFIRMED_OBSERVED_ONCE_OR_INTERMITTENT} |
| Reproduction video | {LINK_OR_NOT_CAPTURED_AND_REASON} |

**Expected:** {EXPECTED_BEHAVIOR}

**Actual:** {OBSERVED_BEHAVIOR_AND_USER_IMPACT}

**Starting state:** {ROLE_DATA_AND_UI_PRECONDITIONS_WITHOUT_SECRETS}

**Reproduction steps:**

1. {USER_ACTION_AND_EVIDENCE_LINK}
2. {USER_ACTION_AND_EVIDENCE_LINK}
3. Observe {BROKEN_RESULT_AND_EVIDENCE_LINK}.

**Possible cause:** {OPTIONAL_UNVERIFIED_HYPOTHESIS_SEPARATE_FROM_OBSERVATIONS}

## Coverage gaps and resume point

{BLOCKED_OR_UNRUN_CASE_IDS_REASONS_TOOL_OR_ENVIRONMENT_LIMITS_AND_NEXT_ACTION}

## Test state and cleanup

{OWNED_TEST_DATA_OR_UI_STATE_CHANGED_CLEANUP_ACTUALLY_COMPLETED_AND_RETAINED_EVIDENCE}
