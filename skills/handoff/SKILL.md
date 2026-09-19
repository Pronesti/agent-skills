---
name: handoff
description: 'Manual workflow: Compact the current conversation into a handoff document for another agent to pick
  up.'
argument-hint: What will the next session be used for?
disable-model-invocation: true
---

Use this workflow only when the user explicitly selects it. Its scope ends with the requested task. Other named workflows are optional and require separate selection; declared supporting file references may be read as needed. Preserve the user's existing authorization and the project's runtime and verification requirements.


Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

If useful, include optional workflow suggestions for the user. The handoff must not instruct the next agent to activate additional skills without user selection.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
