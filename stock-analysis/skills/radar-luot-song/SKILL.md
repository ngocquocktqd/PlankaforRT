---
name: radar-luot-song
description: Radar quét thị trường tìm mã đáng theo dõi để lướt sóng 3–6 tháng — đứng TRƯỚC /hoi-dong-luot-song. Lọc GIAO của 2 tập (momentum Minervini VÀ earnings tăng tốc O'Neil) để tránh bẫy "tăng giá mạnh nhưng lợi nhuận giảm". Đầu ra là watchlist xếp hạng kèm trade-plan từng mã (pivot/stop/target/R:R/catalyst). Dùng khi muốn TÌM mã thay vì tự nghĩ ra, ví dụ "/radar-luot-song" (toàn thị trường) hoặc "/radar-luot-song ngân hàng".
---

# Radar lướt sóng — quét mã đáng theo dõi (3–6 tháng)

Phạm vi quét: **$ARGUMENTS** (trống = toàn thị trường HOSE large/mid-cap đủ thanh khoản;
hoặc ngành/rổ chỉ định như "ngân hàng", "VN30", "chứng khoán").

Bạn là **người vận hành radar**. Nhiệm vụ: từ cả thị trường, lọc ra 3–5 mã đáng đưa vào
watchlist lướt sóng, mỗi mã kèm kịch bản + điểm mua/bán + R:R. Radar chỉ **SÀNG** — mã
lọt phải qua `/hoi-dong-luot-song` thẩm định sâu (đủ 3 vai + dò mìn) trước khi vào lệnh thật.

> 🎯 Nguyên tắc sống còn (rút từ ca CTS): radar KHÔNG phải "top tăng giá mạnh nhất". List
> đó đầy bẫy — CTS tăng 30% nhưng lợi nhuận −38%. Radar chỉ giữ mã nằm ở **GIAO của 2 tập**:
> momentum kỹ thuật **VÀ** earnings tăng tốc. Chỉ một trong hai = loại.

## Bước 0 — Bối cảnh thị trường (làm TRƯỚC, có quyền dừng radar)
Xác định VN-Index đang Stage mấy (giá vs MA50/200, đỉnh/đáy gần, thanh khoản). **Nếu
VN-Index Stage 4 (xu hướng giảm)** → radar trả kết luận "THỊ TRƯỜNG KHÔNG THUẬN — đứng
ngoài, giữ tiền mặt" và DỪNG. Lướt sóng ngược thị trường gãy là công thức thua; không
cố nặn ra mã. Chỉ chạy tiếp khi thị trường Stage 1 muộn/Stage 2.

## Chọn chế độ nguồn dữ liệu
- **Chế độ B (ưu tiên nếu chạy được):** thử `python3 stock-analysis/tools/data_fetch.py
  screen` để quét định lượng thật (Trend Template + tăng trưởng LN quý). Nếu chạy được
  (máy local có vnstock thông mạng) → dùng kết quả này làm Vòng 1.
- **Chế độ A (fallback — mặc định khi sandbox chặn API):** meta-screener bằng WebSearch.
  Ghi rõ đây là nguồn thứ cấp/trễ, nhãn tin cậy B–C.

## Vòng 1 — QUÉT: gom ~15–30 ứng viên thô
Chế độ A dùng WebSearch nhiều từ khoá khác nhau để gom mã đang mạnh:
- Cổ phiếu tăng giá + volume đột biến tuần/tháng gần nhất
- Cổ phiếu phá đỉnh 52 tuần / phá nền với khối lượng lớn
- RS (sức mạnh tương đối) dẫn đầu vs VN-Index
- Cổ phiếu dẫn dắt các ngành ĐANG KHỎE (tiền vào ngành nào?)
- Danh sách khuyến nghị breakout/khả quan của các CTCK gần đây
- Top tăng trưởng KQKD quý gần nhất
Xuất bảng thô: `Mã | Ngành | Lý do lọt radar (momentum hay earnings hay cả hai)`.

## Vòng 2 — LỌC GIAO 2 TẬP: thu hẹp còn 5–8
Chỉ giữ mã qua **CẢ HAI** bộ lọc (mã chỉ đạt một = loại, ghi lý do):

**Bộ lọc MOMENTUM (Minervini)** — đạt ≥6/8 tinh thần Trend Template:
- Giá > MA50, MA150, MA200; MA xếp đúng thứ tự MA50>MA150>MA200; MA200 dốc lên
- RS > VN-Index ở khung 3 & 6 tháng
- ≤25% dưới đỉnh 52T và ≥+30% trên đáy 52T (đang trong xu hướng tăng, không phải Stage 4)

**Bộ lọc CHẤT LƯỢNG (O'Neil)** — bộ lọc chống bẫy:
- Lợi nhuận/doanh thu quý gần nhất YoY **KHÔNG giảm tốc** (ưu tiên tăng tốc); loại thẳng
  mã lợi nhuận đang co (bẫy CTS) dù giá tăng mạnh
- Không bong bóng định giá cực đoan (P/E không vượt xa bất thường trung vị lịch sử/ngành)
- Loại mã dính mìn hiển nhiên: thanh khoản quá thấp không vào/ra được, diện cảnh báo/kiểm
  soát, pha loãng sốc sắp về

Xuất bảng so sánh 5–8 mã còn lại: `Mã | Stage | RS | Tăng trưởng LN quý gần nhất | Định giá | Thanh khoản`.

## Vòng 3 — XẾP HẠNG + TRADE-PLAN cho TOP 3–5
Với mỗi mã, dựng kế hoạch (dùng `stock-analysis/tools/fin_calc.py` khi cần tính R:R):
- **Trạng thái setup**: vừa phá nền / đang trong nền chờ pivot / pullback về hỗ trợ / đã EXTENDED (không đuổi)
- **Pivot vào** (mua khi phá + volume ≥150% TB50) · **Stop** 7–8% dưới pivot
- **Mục tiêu** T1/T2 (kháng cự hoặc bội R) · **R:R** = (T1−pivot)/(pivot−stop), yêu cầu **≥2:1**
- **Catalyst 3–6 tháng** cụ thể · cảnh báo rủi ro riêng
Xếp hạng theo **chất lượng setup × R:R × độ mạnh RS**. Đầu ra:

```
# RADAR LƯỚT SÓNG: [phạm vi] — [ngày]
## Bối cảnh: VN-Index Stage x — [thuận/không thuận]
## Watchlist TOP (xếp hạng)
| # | Mã | Ngành | Trạng thái | Pivot | Stop | T1/T2 | R:R | Catalyst | Hành động |
|---|---|---|---|---|---|---|---|---|---|
| 1 | … | … | vừa phá nền | … | … | …/… | 2,6:1 | … | Vào 1 phần / Chờ pullback |
## Đã loại ở Vòng 2 (kèm lý do — đặc biệt mã "tăng mạnh nhưng earnings giảm tốc")
## Bước tiếp: chạy /hoi-dong-luot-song cho mã #1–3 để thẩm định sâu trước khi vào lệnh
```

## Quy tắc thép
- Radar chỉ SÀNG, KHÔNG thay thẩm định. Mọi mã lọt radar phải qua `/hoi-dong-luot-song`
  (3 vai + dò mìn) rồi mới vào lệnh; và tính tỷ trọng bằng `/phan-bo-von` (túi 🚀 Momentum).
- CẤM surface mã chỉ vì tăng giá mạnh mà earnings giảm tốc — bộ lọc giao 2 tập tồn tại
  chính vì điều này. Thà bỏ sót còn hơn đưa bẫy vào watchlist.
- Thị trường chung Stage 4 → "đứng ngoài", không nặn mã.
- Chỉ liệt mã đủ thanh khoản vào/ra thực tế; mã tăng nóng nhưng thanh khoản mỏng = bẫy.
- Ghi nhãn tin cậy A/B/C; ở Chế độ A (WebSearch) phần lớn là B–C do nguồn thứ cấp/trễ —
  nói rõ đây là danh sách để THEO DÕI, không phải tín hiệu mua ngay.
- Kết thúc bằng: "⚠️ Nghiên cứu học tập, không phải khuyến nghị đầu tư."
