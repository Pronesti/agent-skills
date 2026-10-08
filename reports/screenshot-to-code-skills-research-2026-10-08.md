# Screenshot-to-prompt, plan, and implementation skills

Research date: 8 October 2026. Requested workflow: `research`. Sources were inspected upstream skill instructions, companion references, official repository APIs, and the first-party skills.sh directory. This is a source survey and recommendation, not an installation or a benchmark on an attached image. No screenshot was attached to this research request.

## Recommendation

For your problem, choose a **reference reproduction workflow** with mandatory image inspection, a persistent visual spec, and a rendered comparison gate. A general UI design skill can improve aesthetics while still changing the reference's layout. Popularity and suitability point to different winners here; no inspected skill combines overwhelming screenshot-specific adoption with universally enforced visual verification.

- **Best lightweight, adoption-backed starting point:** OneWave-AI's `screenshot-to-code`, with an explicit requirement to open the image and block completion until comparison succeeds.
- **Strongest inspected official integrated workflow:** OpenAI Product Design's `image-to-code` with its internal `design-qa`. Evaluate the full plugin and its dependencies; this is not a standalone drop-in procedure.
- **Best specialist to evaluate for image-reading discipline:** simota's `pixel` and its shared Image Input Protocol. Strong extraction and comparison requirements, but substantial coupling to the author's agent system.
- **Best experimental measurement supplement:** bdsanxz's `pixel-perfect`. Useful deterministic inspection, regional comparisons, and final verification, but very little adoption evidence and it explicitly permits a text-only model workflow.

These are source-based judgments. They are not measured rankings of output fidelity. Primary sources: [OneWave skill](https://github.com/OneWave-AI/claude-skills/blob/main/screenshot-to-code/SKILL.md), [OpenAI skill](https://github.com/openai/plugins/blob/main/plugins/product-design/skills/image-to-code/SKILL.md), [Pixel skill](https://github.com/simota/agent-skills/blob/main/pixel/SKILL.md), [pixel-perfect skill](https://github.com/bdsanxz/pixel-perfect/blob/main/SKILL.md).

## Popularity: separate broad design from actual screenshot reproduction

### Follow-up: direct skills.sh listings

A direct directory search found a material omission from the initial survey: Leonxlnx Taste Skill's `image-to-code` has roughly **350K displayed installs** (348.4K on the owner page, 349.9K on the leaderboard; these directory snapshots differ). Its source mandates generating new section reference images first, analyzing them, and then coding. That is a popular image-first design workflow, but its generated-reference and regeneration defaults are a poor default for preserving an already supplied screenshot. This candidate should have appeared in the initial popularity comparison. [Owner listing](https://www.skills.sh/leonxlnx/taste-skill), [leaderboard](https://www.skills.sh/), [upstream instructions](https://github.com/Leonxlnx/taste-skill/blob/main/skills/image-to-code-skill/SKILL.md).

Other direct listings verified in the follow-up are [OneWave screenshot-to-code](https://www.skills.sh/onewave-ai/claude-skills/screenshot-to-code) at **1.2K installs**, [OpenAI image-to-code](https://www.skills.sh/openai/plugins/image-to-code) at **6 installs**, [nexu-io image-to-code](https://www.skills.sh/nexu-io/open-design/image-to-code) at **1.5K installs** (explicitly credited to Taste Skill), and [plugin87 image-to-code](https://www.skills.sh/plugin87/ux-ui-agent-skills/image-to-code) at **570 installs**. The plugin87 listing warns that installing only skill folders via `npx skills add` omits its required kit. These are directory figures, not benchmark results. The OpenAI count replaces the initial table's unverified status.

Repository star counts are exact GitHub API snapshots retrieved on 8 October 2026. They describe the whole repository, including unrelated skills. Installs are rounded values displayed by skills.sh at inspection; its documentation describes deduplicated install telemetry. Neither stars nor installs establish active use, quality, or successful screenshot reproduction. Directory summaries can lag upstream instructions, so the actual `SKILL.md` controls the assessment. [skills.sh API](https://skills.sh/docs/api), [FAQ](https://skills.sh/docs/faq).

| Candidate | Repository stars | Individual skill installs | Fit for this request |
|---|---:|---:|---|
| Anthropic `frontend-design` | 180,127 | 962.6K | Very popular aesthetic direction; not a dedicated screenshot extraction workflow |
| UI UX Pro Max | 133,989 | 386.4K | Very popular UI knowledge and stack guidance; not a dedicated screenshot reproduction workflow |
| OpenAI Product Design `image-to-code` | 7,350 | Not verified | Exact image-to-implementation task; integrated plugin |
| OneWave `screenshot-to-code` | 324 | 1.2K | Direct screenshot-to-spec-to-code workflow |
| simota `pixel` | 90 | Not verified | Detailed image extraction and visual verification |
| afterxleep `pixel-perfect-design` | 67 | Not verified | Image-to-native-UI comparison; SwiftUI/FlowDeck oriented |
| xiaopu-ai `web-clone-prompt` | 20 | Not verified | Screenshot/URL-to-portable-prompt specialist |
| santowilem `clone-ui` | 13 | Not verified | Existing-stack replication with evidence and adversarial verification |
| Surya17155 `replica` | 9 | Not verified | Landing-page screenshot-to-developer-prompt specialist |
| WCF900905 `screenshot-to-design-system` | 5 | Not verified | Controls/tokens only; explicitly excludes page layout |
| zwq-top `ui-image-to-code` | 2 | Not verified | Heavy source/spec/browser/Studio workflow |
| bdsanxz `pixel-perfect` | 1 | Not verified | Tool-backed screenshot verification specialist |

Install sources: [frontend-design](https://skills.sh/anthropics/skills/frontend-design), [UI UX Pro Max](https://skills.sh/nextlevelbuilder/ui-ux-pro-max-skill/ui-ux-pro-max), [screenshot-to-code](https://skills.sh/onewave-ai/claude-skills/screenshot-to-code). “Not verified” does not mean zero installs.

Star snapshot sources: [Anthropic API](https://api.github.com/repos/anthropics/skills), [UI UX API](https://api.github.com/repos/nextlevelbuilder/ui-ux-pro-max-skill), [OpenAI API](https://api.github.com/repos/openai/plugins), [OneWave API](https://api.github.com/repos/OneWave-AI/claude-skills), [simota API](https://api.github.com/repos/simota/agent-skills), [afterxleep API](https://api.github.com/repos/afterxleep/agents), [xiaopu API](https://api.github.com/repos/xiaopu-ai/web-clone-prompt), [santowilem API](https://api.github.com/repos/santowilem/skills), [Replica API](https://api.github.com/repos/Surya17155/Replica), [design-system API](https://api.github.com/repos/WCF900905/screenshot-to-design-system), [Studio API](https://api.github.com/repos/zwq-top/ui-image-to-code-studio), [pixel-perfect API](https://api.github.com/repos/bdsanxz/pixel-perfect).

## What the shortlist actually enforces

### OneWave: practical baseline with a verification loophole

The current skill writes a short spec from the image before coding: regions, tokens, repeated components, and unknown states. It matches the repository's stack, builds the reference viewport first, and compares layout, spacing, type, and color. It explicitly disallows claiming a match without looking. However, the render-and-compare step is conditional on browser availability; missing imagery can become sized placeholders. This is a useful baseline, not a hard guarantee that every run opens and verifies the pixels. [Current skill](https://github.com/OneWave-AI/claude-skills/blob/main/screenshot-to-code/SKILL.md).

Its companion visual-check reference shows browser capture, source/render review, responsive checks, and a discrepancy-first correction order. Use it as a procedure rather than blindly copying its example capture geometry. Record actual CSS viewport and image density; a 2880-pixel screenshot does not by itself prove a 1440 CSS-pixel Retina capture. [Visual check](https://github.com/OneWave-AI/claude-skills/blob/main/screenshot-to-code/references/visual-check.md).

### OpenAI: strongest official build-and-QA contract inspected

The skill requires an exact selected visual target, section measurements, matching fonts/icons, and a blocking `design-qa` result before handoff. It runs an interactive frontend prototype, rather than automatically implementing authentication, persistence, or backend integrations. It depends on plugin routing, user context, preflight, and shared overrides. Its asset-generation instructions and mobile template rules may need reconciliation with an existing production application; supplied assets and repository requirements should govern the actual task. One source statement about Image Gen lacking transparency is inconsistent with the currently exposed tool schema, illustrating why host capabilities must be checked. [Image to Code](https://github.com/openai/plugins/blob/main/plugins/product-design/skills/image-to-code/SKILL.md).

The QA helper directly addresses your complaint: open both the source and latest render, put them into one comparison input, normalize viewport/state/density, examine full composition and readable detail crops, and re-capture after fixes. It rejects QA derived solely from memory, code, or paths. Missing comparison evidence yields a blocked result. Its rubric includes typography, spacing, color, imagery, and copy. This is stronger evidence discipline than merely asking for a beautiful frontend. [Design QA](https://github.com/openai/plugins/blob/main/plugins/product-design/skills/design-qa/SKILL.md).

### simota Pixel: explicit extraction, but not a small independent skill

Pixel requires reading the mockup before composition, confidence annotations on extracted values, and a visual verification report. It offers extraction, reproduction, verification, and gap-audit recipes. Tradeoffs include many shared `_common` contracts, project journals, named companion agents, framework questions, and a rule against directly modifying production code. Its stated fidelity percentages are upstream targets/claims, not independently verified benchmark results. Do not adopt its 4/8-pixel snapping if that would change a measured reference. [Pixel](https://github.com/simota/agent-skills/blob/main/pixel/SKILL.md).

The shared Image Input Protocol is especially relevant: read the global frame, create actual regional/detail crops, transcribe visible content, reconcile readings, and separate observations from inference. It explicitly warns against silently losing detail through image downscaling. It is the most detailed inspected source for the “agent never really read the screenshot” failure. [Image Input Protocol](https://github.com/simota/agent-skills/blob/main/_common/IMAGE_INPUT.md).

### bdsanxz: reproducible measurement rather than mandatory vision

This skill provides an inspection/decomposition/render/compare/verify CLI, section acceptance contracts, a hypothesis ledger, focused regression checks, and a final full-page gate. It distinguishes threshold passes from exact identity and preserves evidence under one artifact directory. However, it allows models without vision to use text metrics and probes, so it does not satisfy your insistence on actual visual reading by itself. Its workflow also contains a commit instruction; installing it must not be treated as authorization to commit. With one repository star, consider it an experimental tool-assisted option. [Skill source](https://github.com/bdsanxz/pixel-perfect/blob/main/SKILL.md).

## Prompt-only and other specialist options

| Candidate | Useful behavior | Why it is not the main recommendation |
|---|---|---|
| `web-clone-prompt` | Portable prompt as first artifact; reference frames; font/asset slots and regression plan | Small adoption; Chinese instructions; explicitly assigns precise-looking inferred values and adds motion from a static screenshot. Requires implementation confirmation even after some implementation requests. Useful template ideas, weaker evidence discipline. |
| `replica` | Detailed hero/full-page prompt, asset inventory, classes and component structure | Small adoption; waits for hosted asset URLs; silently runs analysis; encourages detailed motion specs a single still cannot establish. |
| `clone-ui` | Source tiers, screenshot-only support, existing-stack fit, per-section evidence and multiple verification passes | Small adoption and a long operational/security procedure; review dependencies and scope before use. |
| `pixel-perfect-design` | Structured visual analysis and tight build/read/compare cycle | SwiftUI/iOS and FlowDeck examples dominate; rules such as avoiding pure black can conflict with exact reference reproduction. |
| `screenshot-to-design-system` | Region-by-region control styling and sampled token output | Explicitly ignores page layout, backgrounds, icons, and decoration. It would preserve some styling while discarding exactly the layout you want retained. |
| `ui-image-to-code` | Atomic evidence, compiled specs, browser parity, editable Studio layers | Tiny adoption; compulsory Studio, roundtrip, menu-scan and multiple companion signoffs are disproportionate for an ordinary screenshot task. |

Sources, one per candidate: [web-clone-prompt](https://github.com/xiaopu-ai/web-clone-prompt/blob/main/SKILL.md), [Replica](https://github.com/Surya17155/Replica/blob/main/SKILL.md), [clone-ui](https://github.com/santowilem/skills/blob/main/skills/clone-ui/SKILL.md), [pixel-perfect-design](https://github.com/afterxleep/agents/blob/main/skills/pixel-perfect-design/SKILL.md), [screenshot-to-design-system](https://github.com/WCF900905/screenshot-to-design-system/blob/main/SKILL.md), [ui-image-to-code](https://github.com/zwq-top/ui-image-to-code-studio/blob/main/skill/SKILL.md).

## Why the most popular design skills are insufficient alone

Anthropic's current `frontend-design` emphasizes deliberate aesthetic direction, a token/layout plan, and self-critique. It explicitly says pinned visual direction wins, so faithful reproduction is compatible with it. But it does not prescribe a dedicated screenshot intake/extraction gate, and screenshots are conditional on environment support. Choose it for creative decisions left open by the brief; do not let its anti-template preferences override an existing screenshot. [Upstream skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md).

UI UX Pro Max searches design knowledge by product, style, outcome, and stack. It is useful for accessibility or implementation questions, but choosing a recommended palette or pattern is not extracting the supplied reference. Use its recommendations on unshown states or quality concerns without silently replacing observed colors, typography, density, and layout. [Upstream skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/.claude/skills/ui-ux-pro-max/SKILL.md).

Also distinguish **skills** from applications. `abi/screenshot-to-code` is a dedicated image-to-code application with 80,081 repository stars, not a `SKILL.md` workflow for your existing agent. It supports screenshot-based frontend generation and is worth considering if a separate tool fits the process, but its popularity must not be attributed to OneWave's similarly named skill. [Repository](https://github.com/abi/screenshot-to-code), [API snapshot](https://api.github.com/repos/abi/screenshot-to-code).

## Proposed task contract

This is a synthesis from the inspected intake and QA patterns, not an assertion that one upstream implements every requirement.

1. **Open and identify the image.** Record the exact reference, dimensions, visible state, and viewport/density when known. For dense or long screens, inspect the full frame plus actual readable crops. A filename, OCR output, or claimed mental crop is insufficient evidence of visual inspection.
2. **Write the visual spec before implementation.** Preserve region order, anchors, sizes/proportions, spacing, line breaks, typography, palette, borders/shadows, icons, imagery, and visible copy. Give estimated values confidence and source-region references. List unseen behavior and responsive states separately.
3. **Choose the requested deliverable.** Prompt: portable instructions plus reference/spec. Plan: component mapping, existing-stack constraints, assets, steps, acceptance. Implementation: code from that same spec. A text prompt alone loses image evidence; pass the image or crops to the implementing agent when possible.
4. **Render at the reference state.** Match route, data, theme, viewport, crop and density. Inspect a combined source/render comparison and close-up regions. Fix structure first, then geometry, type, color and assets. Re-capture after changes.
5. **Finish with evidence.** Deliver reference/spec/render paths, concrete remaining differences, and verified/unverified status. Passing build/tests is separate from matching the image. Do not announce visual completion if the image cannot be opened or the implementation cannot be compared.

The source disciplines informing this contract are [Image Input Protocol](https://github.com/simota/agent-skills/blob/main/_common/IMAGE_INPUT.md), [Visual check](https://github.com/OneWave-AI/claude-skills/blob/main/screenshot-to-code/references/visual-check.md), and [Design QA](https://github.com/openai/plugins/blob/main/plugins/product-design/skills/design-qa/SKILL.md).

### Reusable invocation

```text
Use the attached screenshot as the visual source of truth.
Deliverable: [prompt only / implementation plan only / implement in this repo].

Before writing the prompt, plan, or code, actually open the image with vision.
Inspect the complete frame and readable crops of dense regions. State the
reference dimensions, visible state, and the concrete regions you observed.
If you cannot access the pixels, report that limitation; do not substitute a
generic UI or pretend you inspected the screenshot.

Write a persistent visual spec covering region order, alignment, proportions,
spacing, typography and line breaks, colors, borders, shadows, icons, imagery,
and visible copy. Separate observed details from estimates and unseen states.
Keep the styling and layout faithful. Do not redesign, simplify away distinctive
details, add decorative motion, or replace assets without identifying the deviation.
Match this repository's actual framework and component/runtime conventions.

For prompt/plan only, include a reference-to-component mapping, asset gaps,
assumptions, and a same-viewport visual acceptance procedure; stop at that deliverable.
For implementation, render the same viewport and state, open a combined
reference/render comparison plus focused crops, fix material differences, and
capture again. Deliver the visual evidence and remaining differences. A successful
build is not visual acceptance. If comparison is blocked, mark fidelity unverified.
```

No skill was installed or invoked beyond the requested research workflow. The next useful evaluation would run the short-listed procedures on the same screenshot and repository, comparing preserved details and actual evidence rather than their marketing claims.
