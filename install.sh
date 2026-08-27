#!/usr/bin/env bash
# Idempotently symlink every skills/<slug> into each agent's skill directory.
# Safe to re-run: prunes repo-owned links whose source vanished, never touches
# real files/dirs or links owned by anything else.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO_DIR/skills"

TARGETS=(
  "$HOME/.claude/skills"
  "$HOME/.codex/skills"
  "$HOME/.cursor/skills-cursor"
)

for target in "${TARGETS[@]}"; do
  mkdir -p "$target"

  for link in "$target"/*; do
    [ -L "$link" ] || continue
    dest="$(readlink "$link")"
    case "$dest" in
      "$SRC"/*)
        if [ ! -e "$dest" ]; then
          rm "$link"
          echo "pruned  $link"
        fi
        ;;
    esac
  done

  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"
    link="$target/$name"
    if [ -L "$link" ]; then
      if [ "$(readlink "$link")" != "$SRC/$name" ]; then
        rm "$link"
        ln -s "$SRC/$name" "$link"
        echo "relinked $link"
      fi
    elif [ -e "$link" ]; then
      echo "SKIP    $link (real file/dir exists, not touching)"
    else
      ln -s "$SRC/$name" "$link"
      echo "linked  $link"
    fi
  done
done
