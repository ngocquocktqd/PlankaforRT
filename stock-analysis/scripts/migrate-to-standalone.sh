#!/usr/bin/env bash
# Tách stock-analysis/ ra thành REPO ĐỘC LẬP, giữ lịch sử git CHỈ của phần này
# (bỏ toàn bộ lịch sử Planka), sửa hết đường dẫn nội bộ, tạo .claude/skills.
#
# Chạy TỪ MÁY BẠN (không phải trong sandbox — sandbox chặn push repo mới):
#   1. git clone <plankaforrt> && cd PlankaforRT
#   2. git checkout claude/stock-analysis-tool-vohi9e
#   3. bash stock-analysis/scripts/migrate-to-standalone.sh [thư-mục-đích] [tên-repo]
#   4. Tạo repo TRỐNG trên GitHub (vd: ngocquocktqd/ai-berkshire-vn)
#   5. Làm theo lệnh script in ra ở cuối (add remote + push)
set -euo pipefail

DEST="${1:-$HOME/ai-berkshire-vn}"
REPO_NAME="${2:-ai-berkshire-vn}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$REPO_ROOT"
echo "▶ Repo nguồn : $REPO_ROOT"
echo "▶ Thư mục đích: $DEST"

# 1. Tách subtree — chỉ giữ commit chạm stock-analysis/, đưa nó thành gốc, GIỮ lịch sử
echo "▶ Đang tách subtree (giữ lịch sử chỉ của stock-analysis)..."
git branch -D _sa_standalone 2>/dev/null || true
git subtree split -P stock-analysis -b _sa_standalone

# 2. Clone nhánh đó thành repo mới, cắt liên kết với Planka
rm -rf "$DEST"
git clone -q -b _sa_standalone . "$DEST"
cd "$DEST"
git checkout -q -b main
git branch -D _sa_standalone 2>/dev/null || true
git remote remove origin

# 3. Sửa đường dẫn nội bộ: stock-analysis/X -> X (giờ stock-analysis LÀ gốc repo)
echo "▶ Đang sửa đường dẫn nội bộ..."
find . -name '*.md' -not -path './.git/*' -print0 | xargs -0 sed -i \
  -e 's#stock-analysis/tools/#tools/#g' \
  -e 's#stock-analysis/skills/#skills/#g' \
  -e 's#stock-analysis/reports/#reports/#g' \
  -e 's#stock-analysis/scripts/#scripts/#g' \
  -e 's#stock-analysis/requirements.txt#requirements.txt#g' \
  -e 's#stock-analysis/README.md#README.md#g'

# 4. Tạo .claude/skills để Claude Code nhận skill khi mở repo mới
echo "▶ Đang tạo .claude/skills..."
mkdir -p .claude
rm -rf .claude/skills
cp -r skills .claude/skills

# 5. Commit dọn dẹp
git add -A
git commit -q -m "chore: tách thành repo độc lập, sửa đường dẫn về gốc repo"

# Quay lại repo Planka dọn nhánh tạm
cd "$REPO_ROOT" && git branch -D _sa_standalone 2>/dev/null || true

cat <<EOF

✅ XONG — repo độc lập đã sẵn ở: $DEST  (giữ nguyên lịch sử git của stock-analysis)

BƯỚC TIẾP (bạn làm):
  1. Tạo repo TRỐNG trên GitHub: https://github.com/new  → tên: $REPO_NAME
  2. Chạy:
       cd "$DEST"
       git remote add origin git@github.com:<user>/$REPO_NAME.git
       git push -u origin main

Sau khi repo mới OK, có thể gỡ stock-analysis khỏi Planka (chạy trong repo Planka):
       git rm -r stock-analysis .claude/skills
       git commit -m "chore: chuyển stock-analysis sang repo riêng \$REPO_NAME"
       git push
EOF
