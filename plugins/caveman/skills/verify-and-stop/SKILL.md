---
name: verify-and-stop
description: 'Prove existing work meets acceptance conditions without expanding scope. Use for
  validation-only tasks, completion checks, focused gate runs, and last-mile proof.'
disable-model-invocation: false
---

This skill may be selected automatically when its trigger fits the authorized task. Apply only to that task. Other named workflows follow their own invocation policy; automatic selection grants no additional authorization.


# Verify and stop

Translate acceptance conditions into smallest sufficient proof set.

- Reuse still-current results with matching repository state.
- Run focused checks before wider gates.
- Distinguish pass, fail, unavailable, and blocked exactly.
- Do not edit product code unless verification request includes fixes.
- Do not add polish, cleanup, or unrelated tests after criteria pass.

Each claim needs its own proof:

| Claim | Proof |
|---|---|
| Tests pass | Test output, zero failures, exit 0 |
| Build or lint clean | That command's own output, exit 0 |
| Bug fixed | Original symptom reproduced, now passing |
| Regression test works | Seen red before fix, green after |
| Subagent or tool finished | Diff or artifact inspected, not its report |
| Requirements met | Each acceptance condition checked one by one |

Hedged status words ("should", "probably", "seems", "Done!") mean proof missing. Run the check, or report status unverified.

Stop immediately when acceptance proof is complete. Report commands, results, and unresolved risk only.
