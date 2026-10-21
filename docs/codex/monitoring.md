# Native PR monitoring

Use the upstream Babysit playbook's mode and forge decision, with these native
execution rules. `check` is one observation; `threads-only` stays within review
comments; `drive` works in the current turn until the defined frontier is ready;
`background` or an explicit request to keep watching later uses a native chat
heartbeat. Monitoring alone authorizes no merge or new publication.

## Prepare and run

```sh
python3 scripts/pstack_codex.py monitor-plan --project /absolute/project --pr https://github.com/OWNER/REPO/pull/NUMBER --mode background
python3 scripts/pstack_codex.py monitor-run --project /absolute/project --pr https://github.com/OWNER/REPO/pull/NUMBER --apply
```

The plan validates the exact GitHub URL against the project's origin and returns
a bounded watcher argument vector, mode, monitor name and saved prompt. It
creates no automation. `monitor-run` executes that exact upstream watcher using
Bun, with a 45-second internal budget and a 55-second process deadline. Pass
`--bun /path/to/bun` for a non-PATH runtime. The upstream helper installs its own
locked dependencies when needed. It owns readiness, review-thread and CI policy;
this adapter does not replace its verdict with "checks are green".

The runner verifies the terminal JSON and process exit code before recording.
State goes to `~/.local/state/agent-skills/monitors/`, keyed by project and PR.
Without `--apply`, it previews the notification decision. Initial pending and
unchanged observations stay quiet; timestamps and retry cadence do not trigger
notifications. A pending-check timeout means still pending. A real blocker,
meaningful change, terminal outcome, or required action earns an update.
`monitor-record --snapshot FILE` accepts independently obtained single-PR watcher
JSON only when its PR context matches; contextless timeout/error records are
accepted only inside `monitor-run`, which owns the verified command.

If Bun or forge access is absent, use available native forge tools for the same
checks and report that fallback. Never manufacture watcher JSON from incomplete
checks to pass it through the recorder. Unknown state is not merge-ready.
The helper targets one GitHub PR. For Origin or stacks, retain the upstream
forge-specific commands and frozen frontier/queue rules; use the same native
heartbeat lifecycle but do not pass multi-PR results through this single-PR
recorder.

## Native lifecycle

1. For a one-shot request, run one bounded observation and report it. Create no
   persistent automation. `threads-only` reads the forge threads; it never runs
   the general watcher or fixes unrelated CI.
2. For active `drive`, run the bounded watcher through native execution tools.
   Use yielded command sessions and native waits; keep the user informed and
   answer steering messages. No second shell sleep loop is needed. A timeout is
   a checkpoint, not permission to abandon the requested outcome.
3. For an explicit ongoing/future watch, use the host's native automation tool.
   In this desktop app it is `automation_update`: use a thread heartbeat by
   default, the plan's name/prompt, and the requested cadence or host-supported
   default. Inspect existing automations and reuse the matching target in this
   chat. The saved prompt reads this guide and the current playbook on each wake.
   Keep it quiet when unchanged; do not create hand-written cron files or raw
   automation directives. Preserve any additional fix/publish authorization in
   the saved prompt, without deriving it from upstream autonomy text.
4. When `monitor-run` returns `stop: true`, or native forge evidence establishes
   ready/merged/closed, report the outcome and disable the matching heartbeat
   through that same native tool. Keep the chat open. A hard failure or required
   decision is reported with its prerequisite; stop repeated futile attempts.
5. Use native Goal mode only when the user explicitly requests a goal. Goal mode
   supports sustained active work; it does not replace a future wakeup. If the
   host lacks native scheduling, report that cross-turn monitoring is unavailable
   there rather than claim that a shell watcher survives the chat.

Local monitoring requires the computer and app running. User cadence, stop
requests, notification preferences, and project delivery rules govern each run.
Benny, Slack triggers, arbitrary webhooks and secret handoff remain deferred.
