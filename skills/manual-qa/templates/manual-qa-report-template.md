# Manual QA: {APP_NAME}

Use applicable fields only. Shared setup/provenance belongs here once; the skill defines status and safety rules.

| Setup | Value |
|---|---|
| Date/build; target/environment | {VERIFIED_SETUP} |
| Surface/session/role | {NONSECRET_IDENTITY} |
| Scope/exclusions; budget | {EFFECTIVE_REQUEST} |
| Sources/report provenance | {CONTEXT_AND_IMPORTED_OBSERVATIONS} |

For imported/reconstructed results only: ledger origin {ORIGIN}; original planned total {SOURCE_TOTAL_OR_UNKNOWN}; reconstructed IDs {IDS_IF_ANY}.

## Case ledger

| ID / priority | Starting state | Actions / nonsecret data | Expected | Status | Actual | Evidence / blocker |
|---|---|---|---|---|---|---|
| {ID} | {PRECONDITIONS} | {ACTIONS} | {ORACLE} | {STATUS} | {OBSERVATIONS} | {REFERENCE_OR_REASON} |

## Reconciled coverage

Known ledger total {TOTAL}; completed {PASS_PLUS_FAIL}; PASS {PASS}, FAIL {FAIL}, BLOCKED {BLOCKED}, NOT RUN {NOT_RUN}; partial attempts {PARTIAL}.

Counts come only from the ledger. List issue counts separately by supplied/default severity; one issue may cover multiple failed cases.

## Issues

Repeat only for findings, not passing cases.

### {ISSUE_ID}: {TITLE}

- Severity/category; affected cases: {IMPACT_BASED_SEVERITY_CATEGORY_IDS}
- Target/preconditions: {SANITIZED_LOCATION_AND_START}
- Expected versus actual; impact: {SPECIFIED_EXPECTATION_OBSERVED_DISCREPANCY_AND_REACH}
- Actual reproduction steps: {NUMBERED_OBSERVED_ACTIONS_OR_UNKNOWN_DETAILS}
- Evidence: {LINKS_AND_PROVENANCE}
- Confirmation/limits: {ATTEMPTS_INTERMITTENCE_UNKNOWNS_OPTIONAL_UNVERIFIED_HYPOTHESIS}

## Gaps and resume point

{BLOCKED_NOT_RUN_AND_DEFERRALS_WITH_REASONS_AND_NEXT_ACTION}

## Proposed checks — outside run counts

{ONLY_NEW_FOLLOWUPS_AND_REQUIRED_ACCESS_OR_ORACLES}

## State and cleanup

{LAST_OBSERVED_STATE_ACTUAL_CLEANUP_RETAINED_EVIDENCE_AND_UNOBSERVED_STATE_MARKED_UNKNOWN}
