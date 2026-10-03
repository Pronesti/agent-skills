---
name: grilling
description: 'Manual workflow: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants
  to stress-test their thinking, or uses any ''grill'' trigger phrases.'
disable-model-invocation: true
---

Use this workflow only when the user explicitly selects it. Its scope ends with the requested task. Other named workflows are optional and require separate selection; declared supporting file references may be read as needed. Preserve the user's existing authorization and the project's runtime and verification requirements.


Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Deliver the complete round as ordinary Markdown in your **final assistant message**, including every question, its full wording, any choices, and its recommendation. In Codex, use chat text for this interview; do not call `request_user_input` or `request_user_input_async`. Include the whole frontier even when it contains more than three questions.

End the round with a short invitation to reply in text by question number, then yield the turn. Yielding waits for the user's next message; it does not complete the interview. Resume from the pending round when the user replies, without polling or keeping the turn running just to wait.

Only actual user answers settle decisions. Recommendations remain proposals until the user accepts them. If the user answers only part of a round, keep the unanswered questions open with their original numbers and defer anything that depends on them. Silence, a timeout, a dismissed question widget, a status request, or an automatic continuation is not an answer or confirmation.

Format a round as rendered Markdown, using this example (the fence is only for showing the template):

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The interview is ready for confirmation when every branch of the design tree has been visited and no unanswered questions or fact-finding prerequisites remain. Summarize the agreed decisions in a final text reply and ask the user to confirm shared understanding. The session is done only after that confirmation; do not act on the plan before it arrives.
