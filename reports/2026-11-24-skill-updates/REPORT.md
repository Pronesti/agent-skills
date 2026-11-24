# Skill source update — 2026-11-24

Checked all 78 managed skills against 20 recorded sources. 14 sources had new revisions. 13 skills took upstream file changes, 61 had no upstream change to their files, `how` and `why` stay at their 7 November base by user decision, and two skills removed upstream remain retained locally. Per-skill outcomes are in [upstream-check.json](upstream-check.json).

## Reconciliation decisions

- Keep all seven automatic triggers, the 71 manual entrypoints, picker metadata, the authorization overlay, and the hook-free Caveman edition.
- Keep `how` and `why` at `6b0300214a09fd6029cfb7077043125758cd1fd2` under a new `pstack-retained` source. Upstream reduced `why` to one paragraph and `how` to a single subagent prompt, and deleted all of their references. The user chose to keep the investigative versions.
- Adopt the shorter upstream `technical-writing` and `unslop`. The `unslop` rule numbers stay stable.
- Merge the removal of the `why` coupling in `blast-radius` and the `recall` intro, keeping the local wording for PR reading, proof, requested review, the `recall` step 4 sweep, and host-supported subagent settings. Replace the remaining `poteto-mode` reference in `show-me-your-work` with host-supported settings.
- Caveman: adopt the `cavecrew` subagent briefing, the `caveman-compress` Codex provider and validator changes (scripts reviewed: fixed argument lists, a permission profile that denies filesystem and network access, no shell), the `caveman-explore` fork frontmatter next to the manual invocation flag, and the `caveman-stats` OMP pointer. Drop the upstream-only `caveman-learn/CLAUDE.md`. Upstream released Caveman 4.2.0 in this range; the local edition is now `4.2.0+selective.20261124`.
- `incremental-implementation`: upstream added an identical-text Definition of Done under `references/shared/`. Keep the adapted local copy and link at `references/definition-of-done.md`.
- `ui-ux-pro-max`: adopt the data refresh, design tokens (`--tokens`), static preview (`--preview`), and new tests. Point the new examples at `${SKILL_DIR}`. Replace the local `design_system.py`, which had a blank line after every line, with upstream's file with trailing whitespace stripped.
- Impeccable: move from `skill-v4.8.0` to `skill-v4.10.0` (engine 0.1.27, checksum-verified launcher). The local path rewrite and overlay were first replayed on 4.8.0 and matched the committed copy byte for byte, then applied to 4.10.0. The Windows launcher keeps CRLF.
- Matt Pocock sources moved to `d65391149dbb5fe76478e76fa8d5122b2aa5a70e` with no change to any vendored Matt skill file. No new upstream skills were imported.

## Sources

| Source | Previous revision | Checked revision |
|---|---|---|
| superpowers | `22f0b463e7a5e579904dd6211a520321035526f7` | `22f0b463e7a5e579904dd6211a520321035526f7` |
| mattpocock | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | `d65391149dbb5fe76478e76fa8d5122b2aa5a70e` |
| pstack | `6b0300214a09fd6029cfb7077043125758cd1fd2` | `ca782ed8b3c2c521cead8e1720d55c3a5dbf2347` |
| ponytail | `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` | `ebd8654c2c627f721eb8f9c0d1bd4090a29f9e10` |
| humanlayer | `4d69d20f6e9b57b4fcf0d501ccfb1be961f0f329` | `4d69d20f6e9b57b4fcf0d501ccfb1be961f0f329` |
| vercel | `d3701c11b1101251af14c9d148f026e1a47ebe17` | `57217cf86ba38148a57af9e90d14a4c049558330` |
| caveman | `c310c9d300df13a1dd9f5c086120ffd857a164a1` | `47c61be2d10a354f0c5cbe2b90959d24c06b16c6` |
| wshobson | `4bde3168b43c0655c4d00ea2726e631719908a6d` | `c96b5f6552dba32e4492307493ee613581430715` |
| addyosmani | `301b02b12bff98e4688e6984af6556802322bbde` | `e997ac5b9a74eab332d5e9793bb38a38c8cfdd74` |
| severity1 | `50aae187bb4f08b852f318234b654df3332726a4` | `50aae187bb4f08b852f318234b654df3332726a4` |
| vercel-agent-browser | `d44f6989bf5e9a9a1c6dd6d97175f8c33b138eca` | `0a923358ea989d7602f0d06507ad3447c62ffe9b` |
| taste | `b482f7a970abb98c4108d4a9f761e458c64cefc8` | `6c0b5c78f5d31776e2210305abaa210cdc0030bf` |
| onewave | `b2267d9171af4f56848d82992381b20b89b44056` | `b2267d9171af4f56848d82992381b20b89b44056` |
| mattpocock-pr | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | `d65391149dbb5fe76478e76fa8d5122b2aa5a70e` |
| warpdotdev | `8792394ff1b655e0af451b8fabb68ef0cfcbd208` | `8792394ff1b655e0af451b8fabb68ef0cfcbd208` |
| anthropics-frontend | `2c5958ecac7cee2b583967a2c4981d0f4a75c579` | `e4bb5d960d87126ff3b3a8af1a104b7db67560ba` |
| nextlevelbuilder | `b7d5353e0130feb8c5574ef1251f8a1db1873ccb` | `cc7b20d85d64d8fa022292cfad731995d3cd4eeb` |
| mattpocock-conflicts | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` | `d65391149dbb5fe76478e76fa8d5122b2aa5a70e` |
| impeccable | `414603bf14c7a344edb466bb1f85690c77ce8b7d` | `b49177d32788f2dc585c42831d845dacf1ebed2c` |
| tstack | `11e37a74d0a6868c121cd0910ab2b3bd9873b92a` | `11e37a74d0a6868c121cd0910ab2b3bd9873b92a` |

## Skills with upstream changes

- `blast-radius` (1 upstream file changes)
- `recall` (1 upstream file changes)
- `show-me-your-work` (1 upstream file changes)
- `technical-writing` (1 upstream file changes)
- `unslop` (1 upstream file changes)
- `caveman:cavecrew` (1 upstream file changes)
- `caveman:caveman-compress` (5 upstream file changes)
- `caveman:caveman-explore` (2 upstream file changes)
- `caveman:caveman-learn` (1 upstream file changes)
- `caveman:caveman-stats` (1 upstream file changes)
- `incremental-implementation` (2 upstream file changes)
- `ui-ux-pro-max` (23 upstream file changes)
- `impeccable` (39 upstream file changes)

## Verification

- `python3 -m unittest discover tests`: OK.
- `python3 scripts/validate.py`: 78 manifests, 7 automatic, 71 manual.
- `ui-ux-pro-max` bundled tests: 189 pass. 5 modules cannot import because they look for upstream's full repository layout, which is not vendored.
- `caveman-explore` bundled test: 5 pass.
- `caveman-compress` and Impeccable were not run against a live model or engine download.

## Executable review scope

- Read in full: the `caveman-compress` `compress.py` and `validate.py` diffs, and the Impeccable POSIX launcher diff. The launcher still verifies every engine download against `engine-checksums.txt`.
- Checked, not read line by line: `impeccable.cmd` (same release, CRLF kept), `live-browser.js` (bundled browser script), and the `ui-ux-pro-max` `preview.py`, `search.py`, `core.py`, and `design_system.py` (imports scanned: no subprocess or network calls; `preview.py` only references Google Fonts URLs in generated HTML).
- The Impeccable path rewrite touches one non-Markdown file, `agents/impeccable_asset_producer.toml`, the same file as in 4.8.0.
