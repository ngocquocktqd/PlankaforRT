#!/usr/bin/env bash
# Cài các skill vàng vào Claude Code (~/.claude/skills)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$HOME/.claude/skills"
mkdir -p "$DEST"
for s in hoi-dong-vang luot-song-vang; do
  rm -rf "$DEST/$s"
  cp -r "$ROOT/skills/$s" "$DEST/$s"
  echo "✓ Đã cài /$s"
done
echo "Xong. Mở Claude Code và gõ /hoi-dong-vang hoặc /luot-song-vang."
