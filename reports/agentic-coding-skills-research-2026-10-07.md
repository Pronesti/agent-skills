# Popular agentic coding skills for design, readability, and evolution

Research date: 7 October 2026. Requested workflow: `research`. Research used the requested Search Service, upstream GitHub source files, GitHub's repository API, and the first-party skills.sh directory. This report records findings and recommendations; it does not install skills, edit the existing skill collection, or authorize their invocation.

## Recommendation

Your current collection already includes the strongest popularity-backed foundation for grilling and domain vocabulary: Matt Pocock's `grill-me`, `grill-with-docs`, `domain-modeling`, `codebase-design`, and `improve-codebase-architecture`. They have both a highly starred upstream repository and substantial individual install counts. Keep them as the foundation. For additions, prioritize Addy Osmani's `code-simplification`, `api-and-interface-design`, and `deprecation-and-migration`; add wshobson's `architecture-patterns` for tactical entity and aggregate design and `dependency-upgrade` for actual dependency changes. Popularity evidence is in the tables below. These are a recommended selection, not an executed installation.

The principal gap is **entity design**. A glossary can settle what “Order” means without settling which states are legal, who owns its invariants, which changes must be atomic, or how concurrent updates behave. Your installed `domain-modeling` is strongest at vocabulary and decision records. A tactical modeling procedure should supplement it. The distinction between strategic domain analysis and tactical entities/aggregates is explicit in Microsoft's architecture guidance. [Domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis), [tactical DDD](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design).

For **readability**, your `unslop` improves prose. It does not replace a code simplification skill. For **upgradability**, distinguish code that is easy to evolve from a dependency, schema, or API migration that must preserve running consumers. That distinction informs the recommendations below.

## Scope and method

The search covered popular standalone skill packs, official and community plugin collections, specification workflows, project delivery frameworks, and specialist DDD repositories. Search themes included requirements interrogation, brainstorming, entity/value-object modeling, aggregates, bounded contexts, architecture, simplification, refactoring, API compatibility, deprecation, dependency upgrades, and schema migration. Secondary articles and directories were useful for discovery; technical conclusions were checked against the upstream sources that own the instructions.

Popularity is used as the **first selection criterion among candidates relevant to the requested job**. A highly popular frontend UI skill does not win a domain modeling comparison merely because it has more installs. Within the shortlist, individual skill installs are stronger evidence of specific adoption than stars on a large collection. Stars establish ecosystem interest; they do not establish how much any one skill is used.

Two independently reported popularity measures are retained:

- **GitHub stars/forks:** exact repository API values retrieved on 7 October, except the explicitly rounded awesome-copilot figures. Stars belong to the whole repository and are not transferable to individual skills or successor repositories.
- **skills.sh installs:** displayed, usually rounded cumulative install counts. Its API documentation calls these deduplicated install counts; its FAQ describes aggregate CLI telemetry. They do not measure active users, successful tasks, or improvements to software quality. Some search-service pages were cached earlier than the access date; those dates are called out where known. [API documentation](https://skills.sh/docs/api), [FAQ](https://skills.sh/docs/faq).

This is an extensive source survey, not an exhaustive census of every skill. No controlled comparison of these skills on your production code was performed. Ratings of fit are researcher judgments from the instructions, not benchmark scores.

## Repository popularity

Exact figures below are point-in-time API snapshots. The API links expose the same fields but will return newer values later. These rankings are within the inspected set.

| Repository | Stars | Forks | Relevant category | Primary evidence |
|---|---:|---:|---|---|
| obra/superpowers | 296,210 | 26,443 | Design, planning, implementation, verification skills | [GitHub API](https://api.github.com/repos/obra/superpowers) |
| mattpocock/skills | 278,889 | 23,361 | Grilling, glossary, architecture, engineering skills | [GitHub API](https://api.github.com/repos/mattpocock/skills) |
| anthropics/skills | 179,999 | 21,291 | Broad official skill examples; limited direct fit for these five needs | [GitHub API](https://api.github.com/repos/anthropics/skills) |
| github/spec-kit | 140,485 | 12,568 | Specification and design workflow with reusable commands/templates | [GitHub API](https://api.github.com/repos/github/spec-kit) |
| addyosmani/agent-skills | 102,396 | 10,728 | Portable engineering process skills | [GitHub API](https://api.github.com/repos/addyosmani/agent-skills) |
| gsd-build/get-shit-done | 64,361 | 5,431 | Archived predecessor; not the current development home | [GitHub API](https://api.github.com/repos/gsd-build/get-shit-done) |
| bmad-code-org/BMAD-METHOD | 53,889 | 6,065 | Broad method suite with current installable skills | [GitHub API](https://api.github.com/repos/bmad-code-org/BMAD-METHOD) |
| wshobson/agents | 40,268 | 4,287 | Plugin collection containing architecture and migration skills | [GitHub API](https://api.github.com/repos/wshobson/agents) |
| github/awesome-copilot | ~39,800 | ~5,100 | GitHub-hosted community catalog; includes refactor skill | [Repository display](https://github.com/github/awesome-copilot) |
| anthropics/claude-plugins-official | 37,492 | 4,223 | Official plugin catalog; code-simplifier agent | [GitHub API](https://api.github.com/repos/anthropics/claude-plugins-official) |
| vercel-labs/agent-skills | 32,028 | 2,808 | Mainly frontend/framework-specific engineering | [GitHub API](https://api.github.com/repos/vercel-labs/agent-skills) |
| open-gsd/gsd-core | 10,262 | 738 | Current GSD home; includes phase discussion skill | [GitHub API](https://api.github.com/repos/open-gsd/gsd-core) |
| supabase/agent-skills | 2,706 | 217 | Database-specific guidance | [GitHub API](https://api.github.com/repos/supabase/agent-skills) |
| getsentry/skills | 1,038 | 53 | Smaller engineering pack; code-simplifier skill | [GitHub API](https://api.github.com/repos/getsentry/skills) |
| ruvnet/agentic-flow | 816 | 178 | Agent framework; project-specific DDD architecture skill | [GitHub API](https://api.github.com/repos/ruvnet/agentic-flow) |

Do not interpret Anthropic's broad `skills` repository or `claude-code` product popularity as adoption of its code-simplifier. The relevant verified source lives in `claude-plugins-official/plugins/code-simplifier/agents/code-simplifier.md`. It is an **agent definition**, while Addy and Sentry provide `SKILL.md` adaptations that explicitly credit it. [Official agent](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md), [Addy adaptation](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md), [Sentry adaptation](https://github.com/getsentry/skills/blob/main/skills/code-simplifier/SKILL.md).

GSD's archived predecessor README redirects to `open-gsd/gsd-core`. The successor's default branch was `next`, and it was not archived at inspection. Its roughly 10K stars must not be represented as the predecessor's 64K. [Predecessor redirect](https://github.com/gsd-build/get-shit-done/blob/main/README.md), [successor](https://github.com/open-gsd/gsd-core).

## Individual skill adoption

The high-count Matt Pocock and Superpowers entries below were displayed on the first-party all-time leaderboard. Other entries were verified on their detail pages. These are displayed values, not independently audited installation records. [All-time leaderboard](https://skills.sh/).

| Skill | Upstream | Displayed installs | Selection implication | Source |
|---|---|---:|---|---|
| grill-me | mattpocock/skills | 1.3M | Leading relevant interrogation option; already installed | [Detail](https://www.skills.sh/mattpocock/skills/grill-me) |
| grill-with-docs | mattpocock/skills | 1.1M | Leading code-grounded design discussion; already installed | [Detail](https://www.skills.sh/mattpocock/skills/grill-with-docs) |
| improve-codebase-architecture | mattpocock/skills | 1.1M | Leading architecture improvement option; already installed | [Detail](https://www.skills.sh/mattpocock/skills/improve-codebase-architecture) |
| tdd | mattpocock/skills | 1.0M | Popular supporting verification discipline; already installed | [Detail](https://www.skills.sh/mattpocock/skills/tdd) |
| domain-modeling | mattpocock/skills | 771.4K | Popular vocabulary/decision foundation; already installed | [Detail](https://www.skills.sh/mattpocock/skills/domain-modeling) |
| codebase-design | mattpocock/skills | 748.3K | Popular interface and module design foundation; already installed | [Detail](https://www.skills.sh/mattpocock/skills/codebase-design) |
| code-review | mattpocock/skills | 682.3K | Popular standards/spec review; already installed | [Detail](https://www.skills.sh/mattpocock/skills/code-review) |
| brainstorming | obra/superpowers | 382.9K | Popular alternative design dialogue; already installed | [Detail](https://www.skills.sh/obra/superpowers/brainstorming) |
| code-review-and-quality | addyosmani/agent-skills | 56.6K | Alternative review process; overlaps existing reviews | [Detail](https://www.skills.sh/addyosmani/agent-skills/code-review-and-quality) |
| documentation-and-adrs | addyosmani/agent-skills | 48.5K | Alternative decision documentation; overlaps domain-modeling | [Detail](https://www.skills.sh/addyosmani/agent-skills/documentation-and-adrs) |
| code-simplification | addyosmani/agent-skills | 47.9K | First readability addition by verified adoption | [Detail](https://www.skills.sh/addyosmani/agent-skills/code-simplification) |
| api-and-interface-design | addyosmani/agent-skills | 47.0K | High-adoption compatibility/interface addition | [Detail](https://www.skills.sh/addyosmani/agent-skills/api-and-interface-design) |
| deprecation-and-migration | addyosmani/agent-skills | 39.9K | Leading inspected lifecycle/migration addition | [Detail](https://www.skills.sh/addyosmani/agent-skills/deprecation-and-migration) |
| architecture-patterns | wshobson/agents | 23.1K | Strongest verified tactical DDD candidate in this search | [Detail](https://www.skills.sh/wshobson/agents/architecture-patterns) |
| refactor | github/awesome-copilot | 22.0K | Popular secondary readability/refactoring alternative | [Detail](https://www.skills.sh/github/awesome-copilot/refactor) |
| database-migration | wshobson/agents | 17.0K | Additional ORM/schema-specific migration guidance | [Detail](https://www.skills.sh/wshobson/agents/database-migration) |
| dependency-upgrade | wshobson/agents | 10.6K | Direct fit for library/framework major-version upgrades | [Detail](https://www.skills.sh/wshobson/agents/dependency-upgrade) |
| code-simplifier | getsentry/skills | 8.3K | Compact alternative with lower measured adoption | [Detail](https://www.skills.sh/getsentry/skills/code-simplifier) |

Known freshness limits: Addy's simplification page was crawled on the access date; its migration page was crawled the preceding week. The database-migration detail page was crawled the preceding day. Other displayed detail counts can also lag actual telemetry. The ordering should be read as a substantial adoption difference, not a real-time race between close numbers. No comparable verified individual install count was found for BMAD's current architecture/elicitation skills, GSD's current discussion skill, or Anthropic's agent definition.

## Fit across the five requested concerns

“Strong” means the inspected instructions directly address the concern. “Supporting” means they help but leave essential decisions to another procedure. “Limited” means it is not their main job. These are qualitative judgments, not measured outcomes.

| Candidate | Grilling | Entity design | Domain design | Readability | Upgradability |
|---|---|---|---|---|---|
| Matt: grill-with-docs + domain-modeling | Strong | Supporting | Strong vocabulary | Supporting | Supporting decisions |
| Matt: codebase-design + improve-codebase-architecture | Supporting | Supporting | Supporting seams | Strong structure | Strong evolvability |
| Superpowers: brainstorming | Strong | Supporting | Supporting | Supporting design | Supporting |
| Addy: code-simplification | Limited | Limited | Limited | Strong | Supporting maintainability |
| Addy: api-and-interface-design | Supporting | Supporting contracts | Supporting | Supporting interfaces | Strong compatibility design |
| Addy: deprecation-and-migration | Limited | Supporting transitions | Supporting | Supporting deletion | Strong migration lifecycle |
| wshobson: architecture-patterns | Limited | Strong | Strong tactical/strategic patterns | Supporting structure | Strong separation |
| wshobson: dependency-upgrade | Limited | Limited | Limited | Limited | Strong dependency execution |
| wshobson: database-migration | Limited | Supporting persistence | Limited | Limited | Strong schema execution |
| GitHub: refactor | Limited | Supporting types | Supporting structure | Strong | Supporting maintainability |
| BMAD: advanced-elicitation + architecture | Strong | Supporting | Strong architecture decisions | Supporting consistency | Supporting constraints |
| Spec Kit: clarify + plan | Strong | Strong explicit data-model artifact | Supporting | Supporting contracts | Supporting specification |
| GSD Core: discuss-phase | Strong | Supporting | Supporting | Limited | Supporting decision continuity |

No single skill directly excels at all five. The fit assessments below explain what each source actually contains and where a recommendation is inference.

## Detailed findings

### 1. Keep Matt Pocock as the main grilling and domain foundation

`grilling` represents decisions as a dependency tree and asks the currently answerable questions in rounds, with recommendations. Facts are investigated separately from human decisions. The latest upstream also makes “yes” accept the recommendation. This is a particularly close fit for your stated desire to improve grilling. [Current grilling source](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).

`grill-with-docs` is the engineering-oriented entrypoint for questioning grounded in the repository and domain documentation. It pairs naturally with your established domain modeling procedure. [Current source](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md).

`domain-modeling` challenges conflicting or overloaded terms, uses concrete edge cases, checks claims against the code, and records resolved vocabulary. ADRs are reserved for meaningful, difficult-to-reverse tradeoffs. The current upstream uses `GLOSSARY.md` and `GLOSSARY-MAP.md`; your installed revision uses `CONTEXT.md` and `CONTEXT-MAP.md`. This naming change is a real compatibility concern for any future update. [Current domain-modeling source](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md), [local installed source](../skills/domain-modeling/SKILL.md).

`codebase-design` focuses on substantial behavior behind simple interfaces, locality of changes, and seams that earn their complexity. Its design comparison references are useful when multiple plausible module interfaces exist. It is module design guidance, not a complete entity/aggregate workshop. [Current codebase-design source](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md).

`improve-codebase-architecture` searches for architectural friction, gives extra attention to frequently changed areas, presents candidate changes visually, and develops the selected opportunity through questioning. This is useful for improving an existing system rather than inventing an architecture in isolation. [Current architecture source](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md).

**Recommendation:** keep this family. Its individual adoption is far higher than the inspected alternatives, and you already have it. Improve the questions and entity outputs it produces before replacing the family wholesale. Preserve your local manual invocation policy and established confirmation behavior during any later upstream merge.

### 2. Addy's code-simplification is the first readability addition

This skill aims to preserve inputs, outputs, effects, errors, and edge cases while improving expression. It follows project conventions, prefers explicit code, avoids unrelated cleanup, and asks the agent to understand the existing behavior before changing it. It recommends small verified changes and warns against speculative abstractions or simplification that requires changing expected tests. [Skill source](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md).

**Recommendation:** use it as the source for a scoped readability procedure. Its 47.9K displayed installs exceed the inspected GitHub `refactor` and Sentry simplifier alternatives. It fills a clearer gap than adding another broad review skill. Your `unslop` can remain a prose editor, while this handles code naming, control flow, cohesion, and unnecessary abstraction. [Local unslop](../skills/unslop/SKILL.md).

The current skill includes automatic-looking downstream process suggestions, such as separate refactoring PRs and a commit-or-continue step. If integrated later, adapt those instructions to your existing authorization and delivery policy rather than importing new permission to commit. That recommendation follows from reading the source alongside your repository's policy.

### 3. Addy's API/interface and migration skills cover maintainable evolution

`api-and-interface-design` treats observable behavior as a potential consumer contract, favors intentional interfaces and additive changes, and covers consistent errors and boundary validation. Its newer material includes concrete idempotency concerns such as retry identity, atomic ownership, mismatched payloads, and uncertain external outcomes. [Skill source](https://github.com/addyosmani/agent-skills/blob/main/skills/api-and-interface-design/SKILL.md).

`deprecation-and-migration` covers replacement ownership, consumer migration, incremental cutover, and eventual removal. Its schema section uses expand/migrate/contract phases, batch backfills, and separation of destructive changes from additive rollout. It emphasizes that reverting code does not itself restore changed data. [Skill source](https://github.com/addyosmani/agent-skills/blob/main/skills/deprecation-and-migration/SKILL.md).

**Recommendation:** add both to a future curated selection. The first helps design interfaces that can evolve; the second supplies a process when old behavior must be retired. Their displayed 47.0K and 39.9K installs support this choice over less-used generic alternatives. Keep your Caveman migration's explicit stage boundary and destruction authorization rules when adapting the second skill. [Local migration](../plugins/caveman/skills/migration/SKILL.md).

A practical integration issue: Addy's upstream README warns that single-skill installs may omit shared repository references. A future import must include the actual referenced resources or adapt references to your repository layout. Do not assume a copied `SKILL.md` is the complete installation. [Upstream README](https://github.com/addyosmani/agent-skills/blob/main/README.md).

### 4. wshobson's architecture-patterns supplies the tactical entity gap

The current skill covers Clean Architecture, ports/adapters, and DDD. It distinguishes stable-identity entities, immutable value objects, aggregates as consistency units, repositories, and domain events. It includes guidance about framework-free domain models, dependency direction, in-memory test adapters, and preventing models from bleeding across bounded contexts. More detailed patterns live in declared reference files. [Skill source](https://github.com/wshobson/agents/blob/main/plugins/backend-development/skills/architecture-patterns/SKILL.md).

**Recommendation:** prefer this as the popularity-backed supplement for entity and aggregate design. It has 23.1K displayed installs in a 40K-star collection, while the dedicated DDD packs examined below had little repository adoption. This is not proof that its architecture rules are universally better; it is the strongest verified tactical-modeling adoption evidence found in this search.

Use the domain model to decide whether separate entities, value types, aggregate behavior, and persistence models are useful in the target application. Do not mechanically create repository interfaces, events, and layers for every CRUD screen. That is a proposed scope rule, not a claim that the skill's examples prove such machinery is necessary.

There is also a concrete composition conflict: the architecture-patterns instructions cross layer boundaries through abstract interfaces, while Matt's codebase-design asks for a demonstrated reason for a seam. Import the tactical modeling guidance selectively and resolve abstraction policy against the actual project. Stacking both sets of imperatives would leave the agent with contradictory design defaults. [Architecture-patterns](https://github.com/wshobson/agents/blob/main/plugins/backend-development/skills/architecture-patterns/SKILL.md), [codebase-design](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md).

### 5. wshobson's dependency-upgrade fills a separate operational gap

This skill includes dependency tree inspection, compatibility analysis, changelog/migration review, staged upgrades, codemods, validation, lockfiles, peer dependencies, and rollback planning. Its examples are heavily JavaScript ecosystem oriented. [Skill source](https://github.com/wshobson/agents/blob/main/plugins/framework-migration/skills/dependency-upgrade/SKILL.md).

**Recommendation:** use it for actual framework/library upgrades, with target-version facts checked against the libraries' current official migration guides. Do not treat sample version matrices as current compatibility facts. Its 10.6K installs are smaller than Addy's lifecycle skills but address a different job directly.

`database-migration` is a separate skill with ORM examples, schema/data transformations, rollback, and deployment considerations. It has 17.0K displayed installs. Its examples need adaptation to the real database engine, table size, write traffic, and data preservation requirements; a syntactically valid `down` migration is not proof that dropped data can be recovered. [Database migration source](https://github.com/wshobson/agents/blob/main/plugins/framework-migration/skills/database-migration/SKILL.md).

### 6. Readability alternatives

GitHub's community-contributed `refactor` skill offers gradual behavior-preserving changes, small verified steps, and common code-smell examples. It is broader than a narrow simplification pass and includes extraction, type safety, and structural changes. Its 22.0K installs make it a credible secondary candidate. It overlaps your existing `caveman:safe-refactor`; choose a main procedure rather than layering both on every task. [Refactor source](https://github.com/github/awesome-copilot/blob/main/skills/refactor/SKILL.md), [local safe-refactor](../plugins/caveman/skills/safe-refactor/SKILL.md).

Anthropic's official `code-simplifier` is an agent definition oriented to clarity, project conventions, preserved functionality, and recently modified code. Sentry provides a real `SKILL.md` adaptation with similar priorities and examples. With 8.3K displayed installs, Sentry is a compact, credible alternative, but it loses the popularity-first comparison to Addy. [Official agent source](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md), [Sentry skill source](https://github.com/getsentry/skills/blob/main/skills/code-simplifier/SKILL.md).

### 7. Superpowers remains a popular alternative, not an entity specialist

The current `brainstorming` source distinguishes feasibility probes, bounded changes, and architectural work; it grounds designs in existing code, asks clarifying questions, and compares alternatives. It also contains extensive approval gates and prescribed transitions. Its useful design focus is understanding purpose, constraints, boundaries, and validation before implementation. It does not provide a dedicated entity identity/invariant/aggregate procedure. [Brainstorming source](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md).

**Recommendation:** retain your adapted installed version as an explicitly selected alternative. Its 296K-star ecosystem and 382.9K individual brainstorming installs satisfy the popularity requirement, but another brainstorming installation would duplicate a capability you already own. Future updates should preserve your selective activation policy instead of reinstating upstream's broad “MUST use” language or automatic handoffs.

### 8. Spec Kit is the most popular inspected specification framework

`clarify` systematically inspects ambiguity, including entities, relationships, identity, uniqueness, lifecycle, external integrations, and acceptance criteria. Its current questioning process caps the session at five questions and asks one at a time. `plan` produces explicit data-model, interface-contract, and validation artifacts. [Clarify source](https://github.com/github/spec-kit/blob/main/templates/commands/clarify.md), [plan source](https://github.com/github/spec-kit/blob/main/templates/commands/plan.md).

**Recommendation:** consider Spec Kit when you want a repository-wide specification process with durable feature artifacts. For your current collection, borrow its coverage categories and data-model output contract conceptually before adopting another whole workflow. Its 140K stars establish broad interest; they are not individual adoption counts for `clarify` or `plan`. The inspected sources are command templates in a toolkit, not interchangeable standalone skills.

### 9. BMAD offers richer critique and architecture facilitation

Current BMAD has real `bmad-advanced-elicitation` and `bmad-architecture` skill entrypoints. The former selects critique methods, applies them to recent work, and asks the user whether to accept proposed changes. The latter records durable architecture invariants, offers coaching and faster assumption-marked drafting paths, and uses shared configuration/memory scripts. [Elicitation skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad-advanced-elicitation/SKILL.md), [architecture skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad-architecture/SKILL.md).

**Recommendation:** use BMAD as an optional broader method suite if you want repeated critique from different perspectives and architecture coaching. Its 53K stars make it a meaningful ecosystem comparison. It introduces shared `_bmad` scripts and configuration, so it is a larger integration than copying a single questionnaire. Do not label its current design skills as obsolete YAML-only workflows; their inspected entrypoints are `SKILL.md` files.

### 10. Current GSD is useful for decision continuity across phases

`gsd-discuss-phase` loads prior project and phase context, identifies undecided gray areas, lets the user select topics, and writes decisions for downstream research/planning. Its questioning guide favors concrete scenarios and clarity about purpose, audience, and completion rather than mechanically walking a questionnaire. [Current skill](https://github.com/open-gsd/gsd-core/blob/next/skills/gsd-discuss-phase/SKILL.md), [questioning reference](https://github.com/open-gsd/gsd-core/blob/next/gsd-core/references/questioning.md).

**Recommendation:** consider it if long projects repeatedly lose prior decisions or re-ask questions. It is a framework with runtime tools and phase conventions. For this collection, decision continuity is a useful pattern to borrow, but it does not outrank Matt's more heavily adopted grilling skills or replace tactical modeling.

## Specialist DDD packs: relevant but not popularity leaders

The following repositories were discovered and checked because they directly mention DDD, entities, aggregates, or domain architecture. Their low adoption is a reason to keep them as reference candidates under your stated preference, not a judgment that their content is poor.

| Repository | Stars | Why it was considered | Evidence |
|---|---:|---|---|
| ForceInjection/domain-driven-design-skills | 82 | DDD aggregation with strategic and tactical material | [Repository/API](https://api.github.com/repos/ForceInjection/domain-driven-design-skills) |
| full-stack-skills/ddd-skills | 14 | Multiple DDD/clean/hexagonal skill groups and entity/aggregate references | [Repository](https://github.com/full-stack-skills/ddd-skills) |
| joabgonzalez/ai-agents-skills | 9 | Dedicated domain-driven-design skill/reference structure | [Repository/API](https://api.github.com/repos/joabgonzalez/ai-agents-skills) |
| deeparchi-ai/ddd-skill | 4 | Dedicated DDD modeling/architecture pack | [Repository/API](https://api.github.com/repos/deeparchi-ai/ddd-skill) |
| joeyave/golang-ddd-skills | 4 | Go-specific architecture, CQRS, infrastructure, refactoring skills | [Repository/API](https://api.github.com/repos/joeyave/golang-ddd-skills) |
| TU-hayaoki/ddd-agent-skills | 1 | Domain-specific skill pack | [Repository/API](https://api.github.com/repos/TU-hayaoki/ddd-agent-skills) |
| aristorinjuang/ddd-agent-skill | 0 | Dedicated DDD skill candidate | [Repository/API](https://api.github.com/repos/aristorinjuang/ddd-agent-skill) |

ruvnet's `v3-ddd-architecture` is explicitly tied to Claude Flow v3's architecture rather than a neutral workshop for arbitrary product entities. Even its parent repository's 816 stars would not establish adoption of that one skill. [Skill source](https://github.com/ruvnet/agentic-flow/blob/main/.claude/skills/v3-ddd-architecture/SKILL.md).

Other inspected repositories included `magnus919/agent-skills` (112 stars), `joshuadavidthomas/agent-skills` (54), and `prisma/skills` (67). They did not displace the leading generic candidates under the popularity criterion. Database vendor guidance remains useful when the actual project uses that vendor; repository size alone does not decide implementation correctness. [Magnus API](https://api.github.com/repos/magnus919/agent-skills), [Joshua API](https://api.github.com/repos/joshuadavidthomas/agent-skills), [Prisma API](https://api.github.com/repos/prisma/skills).

Vercel's broad frontend guidance and Anthropic's frontend-design/examples were considered but have less direct fit for entity semantics or generic upgrade workflows. Supabase's pack is a database-specific candidate rather than a replacement for domain analysis. Avoid conflating **UI design**, **relational table design**, **entity behavior**, and **bounded-context design** merely because all include “design” in their names. [Vercel collection](https://github.com/vercel-labs/agent-skills), [Anthropic collection](https://github.com/anthropics/skills), [Supabase collection](https://github.com/supabase/agent-skills).

## What to improve in your existing collection

The following are proposed changes for a later implementation task. They are synthesis from the inspected sources and the local baseline, not claims that a popular upstream already implements this exact combined procedure. No skill files were changed for this research.

### Make grilling produce a decision record with coverage

Keep your dependency-aware rounds. Add a small internal coverage map for the particular feature: intended outcome, actor, identity, lifecycle, invariants, authorization, concurrency, external contracts, failure handling, and measurable acceptance. Do not ask every category mechanically. Ask only where an unresolved answer changes the design or its verification.

For each important decision, record the question, accepted answer, evidence, affected concepts, and still-open dependencies. This makes a resumed discussion know what is settled. Distinguish discovered facts from user decisions; a source-code observation is not authorization to change a business rule.

Useful patterns to borrow are Spec Kit's coverage taxonomy and GSD's prior-decision loading. Keep the current local rule that unanswered questions remain unanswered. Addy's strict interview stop behavior and upstream Superpowers handoffs should be reviewed as policy differences, not silently activated. [Local grilling](../skills/grilling/SKILL.md), [Spec Kit clarify](https://github.com/github/spec-kit/blob/main/templates/commands/clarify.md), [GSD discussion](https://github.com/open-gsd/gsd-core/blob/next/skills/gsd-discuss-phase/SKILL.md).

### Add an entity design output that a glossary cannot supply

For each concept that needs design work, require a short record containing:

| Design question | Required answer | Example |
|---|---|---|
| Identity | What makes it the same thing over time, and where is that identity unique? | Order ID is unique within a tenant |
| Value versus entity | Is historical identity needed, or are equal values interchangeable? | Currency amount is a value; invoice is tracked over time |
| Invariants | What must always be true, and which operation enforces it? | A captured amount cannot exceed the authorized amount |
| Lifecycle | Which transitions are allowed or rejected? | Draft to confirmed is legal; fulfilled to draft is rejected |
| Ownership | Which context and operation may change the fact? | Billing owns settlement; ordering consumes its outcome |
| Consistency | Which facts must change atomically? | Reserving quantity and updating remaining capacity |
| Concurrency | How are stale updates and duplicate commands handled? | Version conflict rejects an old edit |
| Time/history | What is effective time versus recorded time, and what must remain auditable? | A price correction does not rewrite an issued invoice |
| Persistence/integration | What translation separates domain concepts from stored or external representations? | Third-party payment statuses map to local settlement states |
| Verification | Which scenario proves each important rule? | Concurrent reservations cannot oversell available inventory |

This is a proposed artifact contract. Entity identity, value semantics, and aggregate consistency have authoritative DDD support; the full table is a practical synthesis for agent work. Keep it outside the glossary, which your installed procedure deliberately reserves for vocabulary. The output can be a design note or spec section under the target repository's existing convention. [Microsoft tactical DDD](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design), [local glossary procedure](../skills/domain-modeling/SKILL.md).

Stress-test the model with a normal scenario, an invalid transition, a concurrent action, a repeated command, an external failure, and an evolution case. For a simple feature, two or three relevant examples may be enough. For a payment or inventory model, make the concurrency and uncertain-outcome cases explicit.

### Separate context design from entity implementation

Define which business responsibility owns each fact before discussing classes or tables. Mark terms that mean different things in different contexts. Give each integration an explicit contract and translation owner. Then decide entity and aggregate behavior inside a context. A context can remain a package in one application; this research does not imply introducing microservices.

Use the glossary for terminology, a model note for invariants and ownership, and ADRs for durable tradeoffs. Do not force implementation details into `CONTEXT.md` merely to preserve all decisions in one file. Microsoft's strategic/tactical distinction and the installed glossary scope support this separation; the document organization is a proposed local convention. [Strategic domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis), [local domain-modeling](../skills/domain-modeling/SKILL.md).

### Give readability review a purpose and a behavior boundary

Run a simplification pass on a named diff or module once its behavior is understood. State which observable behavior must remain stable. Target concrete friction: misleading names, deep conditionals, scattered rules, accidental dependencies, duplicated decisions, or unnecessary forwarding. Do not optimize for minimum lines or minimum functions.

Use the target project's existing checks, and add proof only for behavior that the change can plausibly alter. A useful review result names what became easier to understand and why the evidence supports preserved behavior. Your current code review already has a smell baseline and a separate spec axis; the addition should improve expression without replacing those correctness checks. [Local code-review](../skills/code-review/SKILL.md), [local safe-refactor](../plugins/caveman/skills/safe-refactor/SKILL.md), [Addy simplification](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md).

### Make upgradability explicit in both design and migration

During design, identify stable consumer contracts, volatile dependencies, and what a caller must know. Ask which realistic future change would spread through many files. Improve that locality where there is demonstrated variation; do not add plugin systems or abstractions for hypothetical needs.

For a concrete upgrade, identify current and target versions, official migration guidance, consumers, persisted data, mixed-version operation, rollback limits, and acceptance evidence. Separate dependency compatibility from API/data compatibility. For a data transition, model both forward and recovery paths and define the exact requested stage.

Your Caveman migration already provides readers/writers mapping, compatibility windows, idempotent retries, expand/migrate/verify/contract, and explicit later-stage limits. Retain these. Addy's deprecation process can supply consumer ownership and retirement; wshobson's dependency skill can supply upgrade mechanics. A stronger imported checklist should not weaken the installed restriction on implicit destructive contraction. [Local migration](../plugins/caveman/skills/migration/SKILL.md), [Addy migration](https://github.com/addyosmani/agent-skills/blob/main/skills/deprecation-and-migration/SKILL.md), [dependency upgrade](https://github.com/wshobson/agents/blob/main/plugins/framework-migration/skills/dependency-upgrade/SKILL.md).

## Proposed adoption order

1. **Keep and tune the existing Matt foundation.** It already wins the relevant individual adoption comparison. Resolve the local `CONTEXT` versus upstream `GLOSSARY` convention deliberately in any future update.
2. **Add Addy's code-simplification.** This is the highest-adoption inspected direct readability addition and fills a real local gap.
3. **Add Addy's api-and-interface-design and deprecation-and-migration.** They cover designing compatible contracts and retiring old ones.
4. **Add wshobson's architecture-patterns with its declared references.** Use it to strengthen entity/value/aggregate design outputs. It is the best adoption-backed tactical DDD supplement found, despite a smaller audience than the main Matt family.
5. **Add wshobson's dependency-upgrade when needed.** Add database-migration only if the target stack and operational needs justify the extra procedure.
6. **Keep alternative frameworks optional.** Spec Kit is the most popular inspected specification toolkit; BMAD has richer elicitation and architecture coaching; current GSD focuses on multi-phase continuity. Adopt one broader framework only if its artifact conventions and runtime actually solve a recurring problem.

Popularity supports this order, with fit as a prerequisite. It does not establish that installing more overlapping skills will improve outcomes. One main procedure per job, a clear output, and an evaluation on real tasks will make the selection reviewable.

## Evaluate before making the collection larger

A later trial can use four representative tasks: clarify an underspecified feature, design a stateful domain concept, simplify a working module, and upgrade a dependency or persisted contract. Keep the same starting code and acceptance criteria when comparing procedures.

Measure whether the interview surfaces consequential decisions, the model defines and tests its invariants, the simplification is easier to follow without behavior changes, and the migration supports the required compatibility window. Record needless questions, speculative abstractions, unrelated edits, and missing recovery evidence as failures. This is a proposed evaluation plan; this research did not run it.

## Research limitations and completion record

- Repository popularity and CLI installs are adoption signals, not quality experiments. No source established causal improvement to readability or upgrade safety for this exact combination.
- Live GitHub API values and cached skills.sh pages have different freshness. Rounded install counts should not be treated as exact active-user counts.
- Smaller specialists were included for breadth but deprioritized by the user's popularity preference. The search cannot establish that no larger DDD specialist exists anywhere.
- An inspected agent definition, a command template, and a framework-specific skill are different integration units. The Agent Skills specification defines the `SKILL.md` format and optional bundled resources; dependencies and runtime conventions still need inspection. [Specification](https://agentskills.io/specification).
- The relevant installed baseline was inspected directly: `MANIFEST.md`, grilling, grill-with-docs, domain-modeling, codebase-design, improve-codebase-architecture, code-review, unslop, blast-radius, and Caveman migration. [Local manifest](../MANIFEST.md).
- No existing skill was upgraded or invoked as a coding workflow during this research. No installs, commits, external posts, or changes to invocation policy were performed.

The result is a popularity-first shortlist, a comparison across all five concerns, concrete gaps in the existing collection, and proposed improvement patterns that can be implemented in a separately scoped task.
