#!/usr/bin/env bash
# Đẩy TOÀN BỘ code vàng (thư mục gold-analysis/) sang repo độc lập github.com/ngocquocktqd/goldtrading.
#
# Vì sao cần script này: sandbox của Claude chỉ có quyền với repo Planka, KHÔNG push sang
# goldtrading được. Bạn chạy script này TỪ MÁY MÌNH (đã đăng nhập git/gh).
#
# Cách chạy:
#   1. Ở máy bạn: git clone <plankaforrt> && cd PlankaforRT
#   2. git checkout claude/stock-analysis-tool-vohi9e && git pull
#   3. bash gold-analysis/scripts/push-to-goldtrading.sh   [thư-mục-đích]
#   (repo goldtrading đã tạo TRỐNG trên GitHub rồi — script sẽ init + push main)
set -euo pipefail

DEST="${1:-$HOME/goldtrading}"
REMOTE="https://github.com/ngocquocktqd/goldtrading.git"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # .../gold-analysis

echo "▶ Nguồn : $SRC"
echo "▶ Đích  : $DEST"
echo "▶ Remote: $REMOTE"

# 1. Dựng cây repo độc lập: đưa nội dung gold-analysis/ lên GỐC repo mới
rm -rf "$DEST"
mkdir -p "$DEST"
cp -r "$SRC"/. "$DEST"/
rm -f "$DEST/scripts/push-to-goldtrading.sh"   # script tách không cần trong repo mới
cd "$DEST"

# 2. Sửa đường dẫn nội bộ: gold-analysis/X -> X (giờ gold-analysis LÀ gốc repo)
find . -name '*.md' -not -path './.git/*' -print0 | xargs -0 sed -i 's#gold-analysis/##g'

# 3. Tạo .claude/skills để Claude Code nhận skill khi mở repo mới
mkdir -p .claude
rm -rf .claude/skills
cp -r skills .claude/skills

# 4. Khởi tạo git và push
git init -q
git add -A
git commit -q -m "init: gold trading toolkit — hội đồng vàng (dò chế độ) + lướt sóng vàng"
git branch -M main
git remote add origin "$REMOTE"

cat <<EOF

✅ Repo độc lập đã sẵn ở: $DEST
BƯỚC CUỐI (chạy khi đã đăng nhập git):
    cd "$DEST"
    git push -u origin main

Nếu goldtrading đã có commit sẵn (README GitHub tạo tự động), dùng:
    git push -u --force origin main     # ghi đè commit khởi tạo trống
EOF
