#!/usr/bin/env bash
# Cài các skill vào Claude Code (~/.claude/skills) để dùng làm slash command
# ở mọi nơi. Chạy lại script này sau khi cập nhật skill để đồng bộ.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

mkdir -p "$DEST"

installed=0
for skill_dir in "$ROOT"/skills/*/; do
  name="$(basename "$skill_dir")"
  rm -rf "${DEST:?}/$name"
  cp -r "$skill_dir" "$DEST/$name"
  echo "  ✓ /$name"
  installed=$((installed + 1))
done

echo ""
echo "Đã cài $installed skill vào $DEST"
echo "Mở Claude Code và gõ, ví dụ: /phan-tich-dau-tu FPT"
echo ""
echo "(Tuỳ chọn) Cài thư viện dữ liệu: pip install -r $ROOT/requirements.txt"
