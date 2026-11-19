---
name: wait-what-list
description: 'Manual workflow: Explain the topic as a detailed ordered list in ASD-STE100.'
disable-model-invocation: true
---

Use this workflow only when the user explicitly selects it. Its scope ends with the requested task. Other named workflows are optional and require separate selection; declared supporting file references may be read as needed. Preserve the user's existing authorization and the project's runtime and verification requirements.

Explain the topic I name as a detailed ordered list. If I name no topic, use your last message. Write in English ASD-STE100 Simplified Technical English. Use the ubiquitous language from `GLOSSARY.md` (follow `GLOSSARY-MAP.md` to the right one if the repo has more than one).

Start with one or two sentences of context. Then write the numbered list:

- Put the items in the order that things happen, or in the order that I must do them.
- Give each item one action or one fact.
- Write instructions in the imperative. Put the condition before the command: "If the build fails, read the log."
- Keep each item to 20 words or fewer.
- Use letters for sub-steps (a, b, c) when one item has its own sequence.
- Put a warning or a caution immediately before the item it applies to.
- Use one term for each thing in the whole list.

Write code identifiers, commands, and paths exactly as they are. Use only the facts that you already have. If a fact is missing, say so in the list and do not guess.
