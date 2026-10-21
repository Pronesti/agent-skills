# pstack branch verification — 21 October 2026

This records the initial catalog replacement. See the later
[native integration verification](pstack-native-validation-2026-10-21.md) for
the current native agents, model settings, history, monitoring and test results.

Branch: `feat/pstack-only`, based on main `7d17c86` in a separate worktree.
Changes are local and uncommitted. No live-home installation, push, PR, merge,
or GitHub repository fork was performed.

| Check | Result |
| --- | --- |
| Repository unittest suite | 42 passed |
| Project catalog validator | 56 public entrypoints, source mappings, manual invocation metadata, and supporting links passed |
| Complete upstream preservation | All 172 files match the SHA-256 inventory for cursor/plugins `190d28736eff128ec94f502a22c7fe0c4b56cd37` |
| Existing main installer → new installer in scratch home | 53 standalone skills migrated to 56 pstack skills; preview made no changes; custom skill retained; prior instructions backed up; repeat had zero actions |
| Upstream helper tests | 68 passed, 0 failed; Bun 1.4.3 executed the unmodified test command in a temporary copy with local dependencies |
| Upstream helper typecheck | Passed, strict TypeScript watch-pr project |
| Bundled Markdown targets | Resolved; the synthesizer prompt's literal `(url)` example is an output placeholder |
| Read-only upstream update checker | Pin matched upstream HEAD when checked |
| Whitespace check | `git diff --check` passed |
| Shared infrastructure | AGENTS template, install.sh, runtime detection, full instruction-sync implementation, and update checker are byte-identical to main |
| Original checkout | Remains on main with its pre-existing untracked report preserved |

The optional system skill-creator `quick_validate.py` rejects the
`disable-model-invocation` field in the personal entrypoints. This is the existing
Claude/Cursor invocation field used throughout the original repository, paired
with Codex's `agents/openai.yaml` policy. The project validator checks both host
fields. The strict generic validator was not counted as a pass; no system tool
was modified to hide the difference.

Packaging, references, source preservation, installer behavior, and helper code
were checked. A live model run of every workflow was not performed. The Codex
adapter supplies native mappings for tools, delegation, supported models, history,
and file paths, and reports unsupported prerequisites. Benny, Cursor webhooks,
cloud-agent dashboards, Cursor model APIs, and exact cursor-team-kit integrations
do not have full Codex parity. Their source is retained intact.
