# caveman

Talk like smart caveman. Same brain, fewer tokens.

## What it does

Makes the model answer first and cut the ceremony: no greeting, hedging,
filler, recap, or closer. Articles drop when the sentence still reads in one
pass. Code, commands, paths, numbers, and exact error strings never change.
Result depends on model and workload. Measured once on the 3.1.0 skill text (`evals/snapshots/results.json`: claude-opus-5-5, ten prompts, single run, output length only, tiktoken o200k approximation): caveman 3% fewer output tokens at the median than a plain `Answer concisely.` control, inside the noise; ultracave 35%; megacave 9%. No quality-equivalence claim is published. The measurements describe upstream fixtures, not a quality or savings guarantee for this local edition.

This local edition retains `lite`, `full`, `ultra`, and the `wenyan-*`
intensity controls inside the Caveman skill. Upstream's separate `ultracave`
and `megacave` skills are not bundled. Styles apply to the selected task;
session-wide behavior requires an explicit request.

Auto-clarity: every skill drops to normal prose for security warnings,
irreversible-action confirmations, step sequences a fragment could scramble,
and a user who repeats a question. Resumes after the clear part.

## How to invoke

```
/caveman              # the voice (default)
/caveman status       # show current mode without changing it
/caveman ultra       # shorter fragments
/caveman wenyan      # explicitly selected classical Chinese
stop caveman          # back to normal prose
```

This hook-free edition answers status from the conversation and marks it
`(not tracked by this host)`. It has no automatic startup activation.

## Example output

Question: "Why does my React component re-render?"

Normal prose:
> Your component re-renders because you create a new object reference each render. Wrapping it in `useMemo` will fix the issue.

caveman:
> New object ref each render, so React re-renders. Wrap the prop in `useMemo`.

Upstream ultracave example (not a bundled skill):
> Inline object prop, new ref, re-render. `useMemo`.

Upstream megacave example (not a bundled skill):
> 每繪新生對象參照，故重繪；以 `useMemo` 包之則免。

## See also

- [`SKILL.md`](./SKILL.md): full LLM-facing instructions
- [Caveman README](../../README.md): repo overview, install, benchmarks
