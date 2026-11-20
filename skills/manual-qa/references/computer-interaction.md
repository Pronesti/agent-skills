# Native computer interaction

Use the computer and browser tools supplied by the current host. This fork has no separate browser CLI dependency and does not install a driver or plugin.

## Initialize the correct surface

In Codex with `mcp__cua_repl`, use its documented first-call entry point: select the explicitly mentioned tab or app, or create/select a tab for the resolved target and browser. On the first call or after a reset, execute exactly the permitted entry-point call; then read the returned documentation before issuing other actions. Follow the actual tool's initialization rules if its interface changes.

In T3 Code, use the `preview_*` in-app browser tools; load them with tool search when they are deferred. `preview_open` opens a task tab and returns its `tabId`; pass that `tabId` to every later call. `preview_snapshot` observes (`includeImage: true` for visual checks, `save: true` for a screenshot file), `preview_act` clicks, types, presses keys, selects, uploads and scrolls by `aria-ref` locator, and `preview_wait_for` waits for feedback. `preview_resize` covers viewport cases, `preview_dialog` answers native dialogs, and `preview_recording_start`/`preview_recording_stop` capture video. Take a fresh snapshot after each navigation, since refs expire. Close the task tab with `t3_preview_close` at the end unless the user keeps it.

In other hosts, use the browser or computer tools that host supplies and read its own skill or documentation for them first.

Use only APIs described by the tool instructions or returned documentation. Do not hard-code element references, command names from another driver, or a viewport/video capability the tool does not expose. Reuse the current session rather than repeatedly resetting the runtime. The agent's memory is not a substitute for fresh UI state.

## Observe, act, verify, capture

1. Observe the current rendered UI through a screenshot or native snapshot.
2. Identify the visible control a user would choose; use the supported mouse, keyboard, or browser interaction.
3. Wait for relevant visible feedback and re-observe after the state changes.
4. Check the case's expected outcome and capture the result.

Snapshots and accessible names can locate controls, but they do not alone prove visual layout, visibility, or usability. Use screenshots for those checks. Product documentation can establish expectations; do not read product source or set internal state to make the flow succeed. Available console/network diagnostics supplement visible outcomes rather than replacing them.

During normal flows, use realistic interaction order and read the visible feedback. For rapid-action cases, deliberately vary timing and inspect the final result; slowing every action would hide the race being tested. Use keyboard input when testing typing, focus, or keyboard navigation. For dialogs, check initial focus, traversal, exit/Escape, and focus restoration where applicable.

A view resized inside one browser is responsive coverage, not proof of another device or browser engine. If resizing, a role, error injection, file interaction, or recording is unavailable, state that precise gap. Do not invent an action or claim it ran. Use permitted screenshots and reproduction steps when video is unavailable.

## Isolate case state

Establish preconditions through the UI. Clear a filter, close a modal, navigate to the documented entry, or switch an authorized test identity as the case requires. Record reset failures as blockers for dependent cases. Keep one driver per app/session, preserve intentionally returning-user state, and separate fresh-user or role-specific state when supported and authorized.

Operate only the named app and permitted origins. Use a new task tab when appropriate; retain user-owned tabs and sessions. Save evidence only through supported capture/export methods, with secrets masked. Keep artifacts if execution stops so a later pass can resume from its case ledger.
