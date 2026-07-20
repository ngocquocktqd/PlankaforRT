# 🎯 SSI Thesis Trading — bàn luận điểm

Web app đóng **vòng lặp đầu tư**: `luận điểm → lệnh → P&L THEO TỪNG LUẬN ĐIỂM`. Nối các
luận điểm từ framework (`/hoi-dong-dau-tu`, `/hoi-dong-luot-song`…) với dữ liệu & giao
dịch thật qua **SSI FastConnect** (`ssi-sdk`), để biết luận điểm nào *thực sự* kiếm tiền.

![Dashboard bàn luận điểm](dashboard-preview.png)

## Chạy nhanh (chế độ MOCK — không cần credential)
```bash
cd ssi-trading-app
pip install -r requirements.txt
python -m scripts.seed              # nạp 2 luận điểm mẫu (DBC, PVD) + 1 lệnh giấy
uvicorn app.main:app --reload       # mở http://127.0.0.1:8000
```
Không có credential → app chạy **MOCK**: giá giả có nhịp, lệnh **giấy (paper)**, P&L theo
luận điểm tính đầy đủ. An toàn tuyệt đối để phát triển.

## Lên LIVE (dữ liệu thật SSI)
Sao chép `.env.example` → `.env`, điền `SSI_CLIENT_ID / API_KEY / API_SECRET`. App tự
chuyển sang lấy giá thật qua `ssi-sdk`. Đặt lệnh **THẬT** vẫn TẮT cho tới khi bật rõ ràng
`SSI_TRADING_ENABLED=1` + có `SSI_PRIVATE_KEY` (ký RS256) + `SSI_ACCOUNT_NO`.

## Hai giai đoạn (an toàn trước, tiền thật sau)
- **GĐ1 (hiện tại):** FC Data (chỉ đọc) + **paper trading** + P&L/luận điểm + cảnh báo mốc giá.
- **GĐ2:** bật đặt lệnh thật (`place_limit_order`…), đồng bộ vị thế/số dư (`get_equity_*`),
  realtime qua WebSocket (`subscribe_symbol_quote`, `subscribe_order_status`). Đã chừa chỗ.

## Kiến trúc
```
app/
├── config.py    # nạp env → quyết định MOCK/LIVE; trading thật mặc định TẮT
├── models.py    # SQLModel: Thesis · Pillar (trụ + điều kiện vô hiệu) · Level (mốc giá) · Trade
├── market.py    # giá: LIVE qua ssi-sdk get_ohlc_1day, fallback MOCK
├── engine.py    # VỊ THẾ + P&L theo luận điểm (Decimal, giá vốn bình quân) + cảnh báo mốc
├── db.py        # SQLite
├── importer.py  # parse luận điểm markdown (format /theo-doi-luan-diem) → Thesis+Pillar+Level
├── stream.py    # realtime: vòng tick 2s đẩy giá + cảnh báo mốc qua WebSocket (re-arm 1,5%)
└── main.py      # FastAPI REST + WS /ws + phục vụ dashboard
frontend/index.html   # dashboard 1 trang (theme-aware): thẻ luận điểm, P&L live, đổi trạng thái trụ, thêm lệnh giấy
scripts/seed.py       # nạp DBC + PVD từ phân tích thật
```

## Import luận điểm từ framework (đóng vòng chat → app)
Nút **📥 Import luận điểm** trên dashboard (hoặc API):
```
GET  /api/import/scan                    # liệt kê file trong stock-analysis/reports/theses/
POST /api/import/file/DBC.md?dry_run=true    # preview — KHÔNG ghi DB (mặc định)
POST /api/import/file/DBC.md?dry_run=false   # ghi thật (chặn 409 nếu mã đã có luận điểm mở)
POST /api/import/markdown                # dán markdown trực tiếp {markdown, symbol_hint, dry_run}
```
Parser đọc đúng format do skill `/theo-doi-luan-diem` sinh: trụ cột 🟢🟡🔴⚪ + điều kiện
vô hiệu hoá + mốc giá (tích luỹ/mua hời/pivot/stop). Không chắc trường nào → bỏ trống,
không đoán bừa; luôn preview trước khi ghi.

## Van an toàn SIZE (luật /phan-bo-von — bật mặc định)
Mọi lệnh MUA bị kiểm trước khi nhận (`422` nếu vi phạm):
1. **Rủi ro/lệnh**: `(giá − stop) × SL ≤ NAV × risk_pct` (mặc định 1,5%) — cần mốc STOP
   trong luận điểm; không có stop → cảnh báo "chỉ trần tỷ trọng đang bảo vệ bạn".
2. **Trần mã theo hạng**: giá trị vị thế sau lệnh ≤ NAV × (A 15% / B 8% / C 3%).
Thông báo chặn kèm **số cp tối đa còn mua được** theo từng luật. Vẫn có thể cố vượt
(`force=true` — dashboard hỏi confirm) nhưng lệnh bị đóng dấu **"⚠️ VƯỢT LUẬT SIZE"**
vào ghi chú — nhật ký kỷ luật không nói dối. NAV + risk% chỉnh ở badge NAV trên header
(`GET/PATCH /api/settings`).

## Equity curve + max drawdown + benchmark
- Mỗi ngày app tự chụp `EquitySnapshot` (equity = NAV + tổng P&L; kèm VN-Index) —
  `POST /api/equity/snapshot` để chụp tay.
- `GET /api/equity`: chuỗi equity + **benchmark VN-Index chuẩn hoá cùng vốn gốc**
  ("nếu chỉ mua index thì sao?") + drawdown từng ngày + **max drawdown**.
- Dashboard vẽ SVG 2 đường (xanh: sổ của bạn · xám đứt: index) + tile Max DD +
  chênh lệch vs index — câu trả lời cho "toàn bộ công sức này có thắng ETF không?".

## Sổ lệnh, R:R & hiệu suất
- **R:R trên thẻ luận điểm**: kế hoạch `(target−entry)/(entry−stop)` từ Levels + **R hiện tại**
  của vị thế mở `(giá−giá vốn)/(giá vốn−stop)` — biết đang lời/lỗ bao nhiêu "R" so rủi ro chấp nhận.
- **📒 Sổ lệnh** (`GET /api/trades`): mọi lệnh mới nhất trước; **ghi chú sửa được** ngay trên
  bảng (`PATCH /api/trades/{id}`) — nhật ký vì sao vào/ra, nguyên liệu để review kỷ luật.
- **Thống kê** (`GET /api/stats`): tổng P&L (chốt + tạm), phí, **win rate tính trên luận điểm
  đã có lãi/lỗ chốt** (không tô vẽ khi dữ liệu ít), gộp theo mode, xếp hạng từng luận điểm.

## Realtime (WebSocket `/ws`)
- Server tick ~2s (chỉ khi có client xem): đẩy `{type:"quote", prices:{sym:price}}` cho mọi
  mã đang có luận điểm mở — dashboard nhảy giá + P&L **tại chỗ**, không reload.
- Giá chạm mốc luận điểm (vùng mua/stop/pivot/target) → `{type:"alert", ...}`: toast +
  thẻ nháy vàng. Chống spam: mỗi mốc chỉ báo lại sau khi giá rời xa ≥1,5% (re-arm).
- MOCK và LIVE dùng chung đường ống; WS rớt tự reconnect (backoff), fallback poll 30s.

## Backtest chân cơ học (`backtest/` + `scripts/backtest.py`)
Backtest **CHỈ phần máy móc hoá được** của framework — Trend Template + breakout nền
(vol ≥1,5× TB50) + bộ lọc thị trường (index > MA200) + stop 7%/hoà vốn +1R/trailing
MA20/gãy MA50/time-stop 120 phiên + sizing rủi ro 1% equity, trần 15%, tối đa 5 vị thế.
Vào lệnh Ở PHIÊN SAU tín hiệu (không look-ahead), phí 0,15% + trượt 0,1%/chiều, gap qua
stop khớp tại giá mở (lỗ >1R như đời thật).
```bash
# máy local (cần credential SSI_* — sandbox bị chặn mạng):
python -m scripts.backtest fetch --symbols vn30 --from 2019-01-01 --csv-dir data/ohlc
python -m scripts.backtest run --csv-dir data/ohlc --json-out kq.json
```
Đầu ra: số lệnh, win rate, **avg R (expectancy)**, profit factor, CAGR, max drawdown,
so buy-hold VN-Index, đếm lý do thoát. **Mọi báo cáo in kèm GIỚI HẠN bắt buộc đọc**:
không có chân O'Neil (earnings) + phán đoán hội đồng → kết quả là cận trên lạc quan
của riêng chân kỹ thuật; survivorship bias; <30 lệnh đừng kết luận. Đã test 5 kịch bản
tổng hợp (thắng trail +1,96R · gãy MA50 thoát sớm −0,49R · gap stop −2,67R · index
nghịch chặn vào lệnh · thiếu index cảnh báo).

## Nguyên tắc
- **Tiền dùng `Decimal`** (no float) — nhất quán với `stock-analysis/tools`.
- **Trading thật là hành động không undo** → mặc định tắt, sau nút xác nhận + dry-run.
- Mọi màn hình kết thúc: *nghiên cứu học tập, không phải khuyến nghị đầu tư.*
