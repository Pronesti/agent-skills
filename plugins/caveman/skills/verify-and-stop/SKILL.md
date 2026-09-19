---
name: verify-and-stop
description: 'Manual workflow: Prove existing work meets acceptance conditions without expanding scope. Use for
  validation-only tasks, completion checks, focused gate runs, and last-mile proof.'
disable-model-invocation: true
---

Use only when explicitly selected by the user. Other named workflows require separate selection.


# Verify and stop

Translate acceptance conditions into smallest sufficient proof set.

- Reuse still-current results with matching repository state.
- Run focused checks before wider gates.
- Distinguish pass, fail, unavailable, and blocked exactly.
- Do not edit product code unless verification request includes fixes.
- Do not add polish, cleanup, or unrelated tests after criteria pass.

Stop immediately when acceptance proof is complete. Report commands, results, and unresolved risk only.
