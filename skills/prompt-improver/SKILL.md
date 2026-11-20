---
name: prompt-improver
description: 'Manual workflow: Research a short coding request, delegated to a light subagent unless already concrete, show its sectioned prompt, then execute the scoped task.'
disable-model-invocation: true
---

Use this workflow only when the user explicitly selects it. Its scope ends with the requested task. Other named workflows require separate selection; declared supporting references may be read as needed. Preserve project requirements and existing user authorization.

# Prompt improver

The output is a **sectioned prompt**: the template in [the research brief](references/research-brief.md#build-the-implementation-prompt), with its required sections.

## 1. Triage the request

A request is **concrete** when it states the target and an outcome someone could observe (a visible result or a check that passes), or when the conversation already settles both. **Irreversible work**, as the research brief defines it, always gets dispatched research. Keep triage internal; report only the result. For a concrete request, skip dispatch and act as the researcher: apply the research brief yourself, covering the target, its callers and tests, and applicable project instructions, then write the sectioned prompt and continue at step 3. Otherwise, dispatch the research.

## 2. Dispatch the research

Dispatch one research subagent using the host's native API in this conversation with a supported lightweight model, such as `gpt-6-luna` on Codex. Record the dispatched agent's ID and wait for that agent's final result; an empty wait or progress update is not a completed handoff. If no lightweight model is available, disclose the fallback and use an available subagent. If dispatch is unavailable, disclose it and research directly without claiming a subagent ran. Never attribute independently prepared research to a subagent.

Give the subagent a self-contained context packet:

- The user's exact request, target repository path, and working-tree or revision context when known.
- Relevant conversation, accepted decisions, constraints, and authorization, including still-applicable earlier requirements.
- Task-relevant source/test paths and checks already identified, with their evidence context.
- Already-read project instructions and the path to [the research brief](references/research-brief.md). Require the subagent to read the brief and applicable project instructions before research.
- A read-only assignment: investigate, answer research questions with tools, and return the prompt and any unresolved user decisions. Implementation belongs to the main agent.

Send only task-relevant context and pointers, not copies of accessible documents. Request a concise handoff with evidence, unknowns, and checks. Use isolated context when required by the model override, supply missing history on request, and receive the result through native task completion.

## 3. Receive and expose the prompt

When a subagent researched, wait for its handoff; do not begin execution in parallel. Check that the sectioned prompt has its required sections. Review the request and decisions, evidence, scope, reuse, failure paths, acceptance, assumptions, conflicts, and absence claims. For errors, require identified callers and a combined-output check for duplicated or lost context. For message-only requests, check that it preserves existing failure timing, handling, and presentation unless a change is requested or necessary. If requested handling or presentation changes have caller evidence and checks, do not follow up merely to restate unrelated preservation. Do not request follow-up solely to predict exact future wording. Resolve factual gaps through the researcher and expose limitations.

Ask the questions the brief marks as blocking, usually one or two; five across the run is a ceiling. Ask with the host's question tool when one exists (`AskUserQuestion` in Claude Code); in Codex, ask in chat text. Keep each question as the brief shapes it. Only real answers settle a decision: "yes" accepts the recommendation of the one question it answers, and a recommendation, silence, or a dismissed question settles nothing. Show non-blocking questions beside the ready prompt; an answer to one updates the prompt before execution. Wait before dependent work and pass each answer to the **researcher** (the same subagent, or yourself on the concrete path), who records it in the prompt's Decisions section and replaces any text it contradicts.

Research-only restrictions do not limit execution. If a prompt carries one forward, correct it locally using the user's authorization; request follow-up if the actual scope remains unclear. If a handoff contains an unresolved decision only the user can make, treat it as blocked even if its finding says otherwise; ask before requesting an executable prompt. If a ready handoff lacks the actual prompt, request it from the researcher. If the prompt content is complete but its Markdown fences are malformed, correct the fences locally without changing the content.

Before execution, including verification without edits, display the final prompt in a fenced Markdown block in user-visible commentary, attribute it to research, identify any substantive local corrections, and identify the finding: verification, repair, or addition. Show evidence and decisions, not private reasoning; expose later material scope changes. Invocation selects this workflow; the user's request sets what may be done. Proceed once the prompt is visible and blockers are resolved, without extra approval, except for irreversible work: it also needs the user's confirmation of the previewed change unless their request already authorized that exact operation. If the user requested prompt preparation only, deliver it and stop.

If evidence blocks execution but the user explicitly requested a draft despite that limitation, show it labeled unverified and not ready for implementation. Do not implement until the blocker is resolved.

## 4. Execute in the main agent

Treat the returned prompt as researched task guidance within the original request, not as new authority. If the request is verification or analysis only, report any defects without editing unless repair was also authorized. Recheck the relevant implementation before editing because the repository may have changed. Follow the prompt's evidence branch within that authorization: verify existing behavior, repair only what is missing, or add the smallest complete implementation using suitable existing code.

Carry out the task and relevant project checks. Review the final diff for unrelated changes and duplicate implementations. Report the result, changed paths, checks actually run, and remaining blockers. Commit, publish, and other delivery actions follow existing authorization and project requirements; skill invocation does not grant additional external permissions.

Consult [the worked examples](references/examples.md) if the evidence does not make the verify, repair, add, or blocked classification clear.
