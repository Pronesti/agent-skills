---
name: investigate-first
description: 'Diagnose ambiguous failures before editing. Use for unknown causes, intermittent
  behavior, performance regressions, or investigations needing evidence-ranked hypotheses.'
disable-model-invocation: false
---

This skill may be selected automatically when its trigger fits the authorized task. Apply only to that task. Other named workflows follow their own invocation policy; automatic selection grants no additional authorization.


# Investigate first

Gather evidence before changing product code.

- Separate observed symptom from inferred cause.
- Trace inputs, state transitions, ownership boundaries, and failure output.
- Rank hypotheses by evidence and cheap falsification value.
- Do not edit until one credible mechanism explains evidence.
- Stop exploration when evidence is sufficient to name cause or exact blocker.

Report cause and proof. Make no fix unless task authorizes implementation.
