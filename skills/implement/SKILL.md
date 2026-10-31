---
name: implement
description: 'Manual workflow: Implement a piece of work based on a spec or set of tickets.'
disable-model-invocation: true
---

Use this workflow only when the user explicitly selects it. Its scope ends with the requested task. Other named workflows are optional and require separate selection; declared supporting file references may be read as needed. Preserve the user's existing authorization and the project's runtime and verification requirements.


Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run focused tests and relevant checks for the change; widen them when the change or a failure warrants it. Follow the active project’s rules and explicit user requests for full verification, including any local pre-push gate. Reuse passing evidence when the tested state and relevant inputs still match under those rules; rerun affected checks when they no longer match. Report commands, scope, results, and any deferred or blocked verification accurately; never call a focused pass a full-suite pass. A task or local commit alone does not add a full gate. Do not substitute CI for a required local pre-push gate unless the project or user permits it.

Once done, use /code-review to review the work.

Commit your work to the current branch.
