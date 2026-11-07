# Skill source update — 2026-11-07

Checked all 73 managed skills: 41 had upstream file changes, 30 had unchanged upstream content, and two were removed upstream and remain available locally. Full source revisions, file hashes, and per-skill outcomes are in [upstream-check.json](upstream-check.json).

## Reconciliation decisions

- Preserve all seven automatic triggers, the 66 manual entrypoints, picker metadata, task-scoped modes, existing authorization, focused verification, and the hook-free Caveman edition.
- Keep `resolving-merge-conflicts` at `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` under a separate retained source pin; its skill directory is absent at Matt’s current revision. Keep Taste `image-to-code` at `b482f7a970abb98c4108d4a9f761e458c64cefc8`; the current Taste skill is a different workflow. No silent replacement or deletion.
- Adopt the rewritten Brainstorming workflow, lighter implementation-plan format, and disclosed subagent-development references. Adapt automatic workflow handoffs and unrequested delegation to local policy; preserve focused verification and evidence reuse.
- Adopt `GLOSSARY.md` naming for new domain documents. Existing project `CONTEXT.md` layouts remain authoritative until migration is authorized. Replace the retired format reference.
- Adapt new Pstack model guidance to the host’s supported API and models; do not introduce a dependency on unbundled `poteto-mode`. Preserve separately selected reviewer behavior.
- Update Caveman compression safety and concurrency helpers and UI/UX search/data. Keep existing Caveman intensity commands inside the local voice skill; do not add unbundled voice skills or hooks.
- Bump the local Caveman manifests to `4.1.0+selective.20261107`. Preserve Apache-2.0 LICENSE/NOTICE and the earlier MIT notice for retained material; record local adaptations in the plugin’s LOCAL-CHANGES.md.
- Correct the stale blanket manual-only statement in the local writing-for-agents reference to match the existing selective allowlist.

## Sources

| Source | Previous revision | Checked revision |
|---|---|---|
| superpowers | `5bf4e78011075bcfc0dc295f0724994cd123ee71` | `22f0b463e7a5e579904dd6211a520321035526f7` |
| mattpocock | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` |
| pstack | `032be146865d973682535de75f2287da438550bf` | `6b0300214a09fd6029cfb7077043125758cd1fd2` |
| ponytail | `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` | `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` |
| humanlayer | `ca7c8088db69e315a8b2deea43820270457f8f3c` | `4d69d20f6e9b57b4fcf0d501ccfb1be961f0f329` |
| vercel | `7407f3893ad4dceab546ac002c3ef806e4000c73` | `d3701c11b1101251af14c9d148f026e1a47ebe17` |
| caveman | `542442bab314973709f95b85b1ac0b3f6f5b5dc6` | `c310c9d300df13a1dd9f5c086120ffd857a164a1` |
| wshobson | `46891e7e60da0e52baf1050b7b6391b64e84c6d9` | `4bde3168b43c0655c4d00ea2726e631719908a6d` |
| addyosmani | `1401c8b8030e023baeebb31781a6653fe8e93026` | `301b02b12bff98e4688e6984af6556802322bbde` |
| severity1 | `50aae187bb4f08b852f318234b654df3332726a4` | `50aae187bb4f08b852f318234b654df3332726a4` |
| vercel-agent-browser | `f7c8b071343dda29477a56cb336ea76144c05496` | `d44f6989bf5e9a9a1c6dd6d97175f8c33b138eca` |
| taste | `b482f7a970abb98c4108d4a9f761e458c64cefc8` | `f6b76575f949707b4e3c37cd86cb44b0b98643e8` |
| onewave | `fc5b7851a6c7ba367e05797df46ad3679df355dd` | `b2267d9171af4f56848d82992381b20b89b44056` |
| mattpocock-pr | `49dd158d1076134a641b33efb035946536778336` | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` |
| warpdotdev | `7c4eb852de8d7c3e68c81802e1c59db9a611f914` | `8792394ff1b655e0af451b8fabb68ef0cfcbd208` |
| anthropics-frontend | `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | `2c5958ecac7cee2b583967a2c4981d0f4a75c579` |
| nextlevelbuilder | `56ea9cf174ed86786187daa9de0e6247cb0747e4` | `b7d5353e0130feb8c5574ef1251f8a1db1873ccb` |

## Skills with upstream changes

- `brainstorming` (5 upstream file changes)
- `executing-plans` (3 upstream file changes)
- `requesting-code-review` (1 upstream file changes)
- `subagent-driven-development` (14 upstream file changes)
- `systematic-debugging` (6 upstream file changes)
- `writing-plans` (2 upstream file changes)
- `grilling` (1 upstream file changes)
- `research` (1 upstream file changes)
- `wait-what` (1 upstream file changes)
- `wizard` (1 upstream file changes)
- `code-review` (1 upstream file changes)
- `codebase-design` (1 upstream file changes)
- `diagnosing-bugs` (1 upstream file changes)
- `domain-modeling` (3 upstream file changes)
- `handoff` (1 upstream file changes)
- `implement` (1 upstream file changes)
- `improve-codebase-architecture` (1 upstream file changes)
- `setup-matt-pocock-skills` (5 upstream file changes)
- `tdd` (1 upstream file changes)
- `teach` (1 upstream file changes)
- `to-tickets` (1 upstream file changes)
- `triage` (1 upstream file changes)
- `wayfinder` (1 upstream file changes)
- `blast-radius` (1 upstream file changes)
- `how` (2 upstream file changes)
- `recall` (1 upstream file changes)
- `show-me-your-work` (2 upstream file changes)
- `technical-writing` (1 upstream file changes)
- `unslop` (1 upstream file changes)
- `why` (9 upstream file changes)
- `ponytail` (1 upstream file changes)
- `caveman:cavecrew` (1 upstream file changes)
- `caveman:caveman` (2 upstream file changes)
- `caveman:caveman-compress` (7 upstream file changes)
- `caveman:caveman-explore` (1 upstream file changes)
- `caveman:caveman-help` (2 upstream file changes)
- `caveman:caveman-learn` (5 upstream file changes)
- `caveman:caveman-stats` (1 upstream file changes)
- `architecture-patterns` (1 upstream file changes)
- `code-simplification` (1 upstream file changes)
- `ui-ux-pro-max` (12 upstream file changes)

## Verification

- **metadata**: 73 manifests passed: 7 automatic, 66 manual; supporting references and hook-free plugin manifests passed.
- **repository tests**: 38 passed
- **ui ux runtime and data tests**: 150 passed
- **ui ux upstream repository maintenance tests**: 4 test modules could not load because upstream maintenance scripts and repository layout are not bundled. Excluded from the focused runtime/data run.
- **caveman metadata tests**: 10 passed
- **caveman compression tests**: 128 run: 127 passed, 1 skipped (Windows-specific); upstream tests loaded from c310c9d300df13a1dd9f5c086120ffd857a164a1, with repository-path adaptation and temporary state directories. No model API calls.
- **helper smoke checks**: Passed: exact task IDs, unterminated-fence rejection, current-checkout workspace selection, task-start/task-done with silent success, review package, append-only log.
- **syntax**: Changed Python ASTs, Bash scripts, and Node server passed.
- **git diff check**: passed

The first unrestricted UI/UX discovery run reported four import errors for `test_catalog_refresh`, `test_catalog_summary_line_endings`, `test_relevance_evaluator`, and `test_skill_script_paths`. They expect upstream repository maintenance tools (`refresh-google-fonts.py`, `refresh-icon-catalog.py`, `generate-catalog-summary.py`, and `evaluate-relevance.py`) and source/template layouts outside the installed skill. The 150 runtime/data tests were then run without those four modules. This is an existing packaging limit, not a passing full upstream suite.

Compression tests first encountered blocked writes to the default user state directory. Rerunning with temporary XDG/LOCALAPPDATA state passed; user state was not modified.

## Delivery state

The user authorized direct delivery on `main`, pushing to origin, and a local skill refresh after reviewing the update. Standalone skills link to the canonical source files. Refresh the cached Caveman edition through the hosts’ plugin commands; preserve existing global instructions rather than replacing them with the narrower shared template. Commit and installation results are reported in the delivery chat. Existing `.DS_Store`, `.idea/`, and `reports/2026-09-19-skill-audit/` changes are excluded from delivery.
