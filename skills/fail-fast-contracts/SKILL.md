---
name: fail-fast-contracts
description: 'Manual workflow: Plan and write code that trusts contracts, asserts on logic errors, stays small, and aborts instead of recovering.'
disable-model-invocation: true
---

Use this workflow only when the user explicitly selects it. Its scope ends with the requested task. Other named workflows are optional and require separate selection; declared supporting file references may be read as needed. Preserve the user's existing authorization and the project's runtime and verification requirements.

# Fail-fast contracts

Select this skill with a planning or coding workflow, such as `writing-plans`, `executing-plans`, `subagent-driven-development`, `tdd`, or `implement`. The other steps of that workflow stay in force.

## Rules

These rules take precedence over other guidance on unexpected input, defensive checks, and failure handling.

1. Assume callers obey function contracts. It is not your job to enforce correct use, and doing so can mask bugs and cause worse problems later.
2. Failing fast via assert is better than trying to "handle" an unexpected condition by exploring a novel part of the program's state space. Fail safe and abort on logic errors.
3. After writing code, ask yourself: "Can I make this simpler?" All things being equal, bug count is proportional to LOC.
4. When the user, the spec, or the project instructions declare crash-only software: This is crash-only software, structured so every prefix of every execution is correct. When in doubt, do not attempt to recover from errors, including resource exhaustion. Just abort and let higher-level logic react.

## Contracts and trust boundaries

A contract binds code inside the program. State each precondition in the signature or type first. Assert it where the code depends on it. An assert message names the invariant and the value: `quantity must be positive, got {q}`.

Data that crosses a trust boundary has no caller to trust: user input, files, network responses, and other services. The spec defines what the boundary accepts. The boundary rejects everything else with the error the spec names, or with a clear error when the spec names none. A rejection that the spec defines is stated behavior, so it gets a test.

## With `writing-plans`

- **Review Focus:** list up to five trust-boundary inputs whose rejection the spec defines and no task's test covers. Add each one's test to the task that owns the boundary. An empty section is a valid result.
- **Self-review item 4:** check the same trust-boundary inputs, and only those.
- **Preconditions:** a step names the contract and its assert. The plan contains no task or test that makes code tolerate a broken precondition.
- **Simplicity:** after the self-review, ask "Can I make this simpler?" Remove each task, branch, option, and parameter that the spec does not require.

## With execution and review workflows

- Copy the Rules section, with its precedence line, into every implementer and reviewer brief.
- A reviewer reports a fallback, retry, or default value that hides a logic error as a defect.
- A reviewer requests a new check only at a trust boundary.

## Before finishing

- Every new assert names the invariant and the value.
- After a logic error, the code aborts. No catch, fallback, or retry continues on the state that the error left.
- Each trust-boundary rejection that the spec defines has a test.
- You asked "Can I make this simpler?" and either made the diff smaller or can state why it is already minimal.
