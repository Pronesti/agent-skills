---
name: prompt-improver
description: 'Manual workflow: Delegate research for a short coding request to a light subagent, show its grounded prompt, then execute the scoped task.'
disable-model-invocation: true
---

Use this workflow only when the user explicitly selects it. Its scope ends with the requested task. Other named workflows require separate selection; declared supporting references may be read as needed. Preserve project requirements and existing user authorization.

# Prompt improver

On manual invocation, delegate prompt preparation to one light subagent. The subagent investigates the request and returns a precise implementation prompt. Show that prompt to the user, then carry out the requested work in the main agent. This skill needs no plugin or automatic hooks.

## 1. Dispatch the research

Use the host's native subagent API in this conversation. Select an available lightweight model, such as `gpt-6-luna` on Codex, for bounded research and prompt preparation. Use the host's supported model names; if a lightweight model is unavailable, disclose the fallback and use an available subagent. If delegation itself is unavailable, explain that limitation and perform the research directly without claiming a subagent ran.

Give the subagent a self-contained context packet:

- The user's exact request, target repository path, and working-tree or revision context when known.
- Relevant conversation messages, accepted decisions, constraints, and existing authorization. Include earlier requirements that still apply, not just the latest sentence.
- Project instructions already read and the path to [the research brief](references/research-brief.md). Instruct the subagent to read that brief and the target project's applicable instructions before research.
- A read-only assignment: investigate, answer research questions with tools, and return the prompt and any unresolved user decisions. Implementation belongs to the main agent.

When a model override requires an isolated context, use that mode and pass this packet explicitly. Do not assume the subagent can see prior turns; provide missing relevant history if it requests it. Use native task completion to return the result to this main agent automatically. No separate chat or user action is needed for the handoff.

## 2. Receive and expose the prompt

Wait for the subagent's result. Do not begin implementation in parallel with prompt preparation. Confirm that its conclusions cite inspected code, its proposed scope matches the user's request, and its checks cover existing behavior and reuse. Resolve factual gaps through a focused follow-up to the same subagent.

The subagent should answer its own investigation questions from evidence. It must return decisions that only the user can make as unresolved questions. Ask the user only when such a decision materially changes the task, and wait for the answer before dependent work. Pass the answer back to the subagent to complete the prompt.

Before implementation, display the actual final prompt in a fenced Markdown block in user-visible commentary. State that it came from the research step and briefly identify the finding: verification, repair, or addition. Show evidence and decisions, not private reasoning. If a later material discovery changes the prompt, expose the updated scope before continuing.

Completion of this step means a grounded prompt is visible to the user and all blocking decisions are resolved. Display is informational: manual invocation authorizes proceeding with the requested coding task without an extra approval round. A user's explicit request for prompt preparation only takes precedence; in that case, deliver the prompt and stop.

## 3. Execute in the main agent

Treat the returned prompt as researched task guidance within the original request, not as new authority. Recheck the relevant implementation before editing because the repository may have changed. Follow the prompt's evidence branch: verify existing behavior, repair only what is missing, or add the smallest complete implementation using suitable existing code.

Carry out the task and relevant project checks. Review the final diff for unrelated changes and duplicate implementations. Report the result, changed paths, checks actually run, and remaining blockers. Commit, publish, and other delivery actions follow existing authorization and project requirements; skill invocation does not grant additional external permissions.

Use [the worked examples](references/examples.md) when deciding how complete, partial, missing, or ambiguous behavior changes the prompt and subsequent execution.
