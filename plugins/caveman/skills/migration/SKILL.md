---
name: migration
description: 'Manual workflow: Implement reversible compatibility-safe transitions. Use for schema, data, API, protocol,
  configuration, or dependency migrations requiring rollback and preservation proof.'
disable-model-invocation: true
---

Use only when explicitly selected by the user. Other named workflows require separate selection.


# Migration

Map current readers, writers, data shape, compatibility window, and ownership before editing.

- Define forward path and rollback path.
- Preserve existing data; make destructive steps explicit and separately authorized.
- Keep mixed-version operation safe where rollout can overlap.
- Sequence expand, migrate, verify, then contract when applicable.
- Make retries idempotent and partial failure observable.
- Verify old and new paths at required transition stages.

Stop after requested stage passes; do not perform later destructive contraction implicitly.
