# 🎯 SSI Thesis Trading — bàn luận điểm

Web app đóng **vòng lặp đầu tư**: `luận điểm → lệnh → P&L THEO TỪNG LUẬN ĐIỂM`. Nối các
luận điểm từ framework (`/hoi-dong-dau-tu`, `/hoi-dong-luot-song`…) với dữ liệu & giao
dịch thật qua **SSI FastConnect** (`ssi-sdk`), để biết luận điểm nào *thực sự* kiếm tiền.

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
└── main.py      # FastAPI REST + phục vụ dashboard
frontend/index.html   # dashboard 1 trang (theme-aware): thẻ luận điểm, P&L live, đổi trạng thái trụ, thêm lệnh giấy
scripts/seed.py       # nạp DBC + PVD từ phân tích thật
```

## Nguyên tắc
- **Tiền dùng `Decimal`** (no float) — nhất quán với `stock-analysis/tools`.
- **Trading thật là hành động không undo** → mặc định tắt, sau nút xác nhận + dry-run.
- Mọi màn hình kết thúc: *nghiên cứu học tập, không phải khuyến nghị đầu tư.*
