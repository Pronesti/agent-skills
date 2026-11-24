# Local edition changes

Updated selected skills from Caveman 4.1.0 on 2026-11-07. This distribution retains 20 existing skills and their local supporting files; it does not bundle the upstream engine or register hooks.

Local changes preserve the selective invocation allowlist, task-scoped modes, explicit selection of other workflows, host-native capabilities, and project runtime, verification, and delivery requirements. The Caveman voice entrypoint preserves local intensity commands without invoking unbundled voice skills. The stats helper remains manual.

On 2026-11-19, `verify-and-stop` gained a claim-to-proof table and a hedged-wording check, adapted from obra/superpowers `verification-before-completion`. It keeps reuse of still-current results.

On 2026-11-24, five skills took upstream changes from Caveman 4.2.0 (`47c61be`), and the edition version moved to the 4.2.0 base: the `cavecrew` subagent-briefing rules, the `caveman-compress` Codex provider with its locked-down permission profile and stricter validation, the `caveman-explore` fork/Explore frontmatter (manual invocation kept), the `caveman-stats` Oh My Pi pointer, and removal of the upstream-only `caveman-learn/CLAUDE.md` maintainer note.

Updated upstream files are covered by LICENSE (Apache-2.0) and NOTICE. Pre-3.0 files retain the MIT notice in LICENSE-MIT. The retained historical LICENSE.BSL applies only to any previously bundled files within its declared scope.
