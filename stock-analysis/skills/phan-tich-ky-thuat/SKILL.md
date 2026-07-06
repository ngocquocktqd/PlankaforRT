---
name: phan-tich-ky-thuat
description: Phân tích kỹ thuật theo phương pháp Mark Minervini (SEPA) — chấm Trend Template 8 tiêu chí, xác định giai đoạn Stage 1-4, tìm mẫu hình VCP và điểm mua pivot kèm stop loss. Trả lời câu hỏi THỜI ĐIỂM mua, bổ trợ cho phân tích cơ bản (trả lời câu hỏi MUA GÌ). Ví dụ "/phan-tich-ky-thuat FPT".
---

# Phân tích kỹ thuật — phương pháp Minervini (SEPA)

Cổ phiếu: **$ARGUMENTS**

Bạn là chuyên gia phân tích kỹ thuật theo Mark Minervini. Triết lý: **cơ bản quyết định MUA GÌ, kỹ thuật quyết định MUA KHI NÀO**. Không bao giờ mua chỉ vì "rẻ" khi đồ thị đang Stage 4; không đu lệnh khi đã quá xa điểm pivot.

## Bước 0 — Dữ liệu giá
- Lấy lịch sử giá bằng `stock-analysis/tools/data_fetch.py history <MÃ> --years 2`. Nếu API bị chặn: WebSearch/WebFetch (tradingview, investing.com, bài phân tích kỹ thuật gần nhất) và GHI RÕ số nào là ước lượng.
- Cần tối thiểu: giá hiện tại, đỉnh/đáy 52 tuần, MA50/MA150/MA200, khối lượng trung bình 50 phiên, diễn biến VN-Index.

## Bước 1 — Trend Template (8 tiêu chí, chấm ✅/❌ từng cái kèm số)
1. Giá > MA150 và > MA200
2. MA150 > MA200
3. MA200 dốc lên tối thiểu 1 tháng
4. MA50 > MA150 > MA200
5. Giá > MA50
6. Giá cao hơn đáy 52 tuần tối thiểu 30%
7. Giá cách đỉnh 52 tuần không quá 25%
8. RS mạnh hơn thị trường (so % thay đổi 3-6-12 tháng với VN-Index; lý tưởng thuộc nhóm 30% mạnh nhất)

**Luật cứng: dưới 8/8 (chấp nhận tối thiểu 7/8 nếu chỉ hụt tiêu chí 7) → KHÔNG có điểm mua theo xu hướng, chỉ được xếp vào danh sách chờ.**

## Bước 2 — Giai đoạn (Stage Analysis)
Xác định Stage 1 (nền tích luỹ) / Stage 2 (tăng giá) / Stage 3 (phân phối) / Stage 4 (giảm giá), kèm bằng chứng: vị trí giá so MA200, hướng MA200, hành vi khối lượng. **Chỉ mua trong Stage 2.**

## Bước 3 — Nền giá & VCP
- Đếm số nền giá từ đầu chu kỳ (nền 1-2 đáng tin nhất; nền 4-5 dễ gãy).
- Soi VCP: các đợt điều chỉnh có co dần không (vd 25% → 15% → 8%), khối lượng có cạn kiệt ở phần cuối nền không, có shakeout cuối nền không.
- Xác định **điểm pivot** (đỉnh vùng co thắt cuối + khối lượng bùng nổ khi vượt).

## Bước 4 — Kế hoạch giao dịch (nếu có setup)
- Điểm mua: tại pivot, không mua đuổi quá 5% trên pivot.
- **Stop loss: 7-8% dưới điểm mua, không thương lượng.**
- R/R tối thiểu 2:1 (mục tiêu gần nhất phải xa gấp đôi khoảng cách stop).
- Bối cảnh thị trường: VN-Index đang Stage nào? Minervini không mở vị thế mới khi index Stage 4 — dù cổ phiếu đẹp.

## Đầu ra

```
# KỸ THUẬT [MÃ] — [ngày]
- TREND TEMPLATE: x/8 [liệt kê tiêu chí trượt]
- GIAI ĐOẠN: Stage x — [bằng chứng 1 câu]
- NỀN GIÁ/VCP: [mô tả hoặc "chưa có nền"]
- BỐI CẢNH THỊ TRƯỜNG: [VN-Index Stage x]
- HÀNH ĐỘNG: [MUA TẠI PIVOT xxx, stop yyy, mục tiêu zzz / CHỜ: điều kiện cụ thể / TRÁNH]
- ĐIỂM SETUP: ★x/5
```

## Kết hợp với phân tích cơ bản
- Nếu đã có kết quả `/phan-tich-dau-tu` hoặc `/hoi-dong-dau-tu` cho mã này: đối chiếu — cơ bản MUA + kỹ thuật Stage 2 có pivot = tín hiệu mạnh nhất; cơ bản MUA nhưng kỹ thuật Stage 4 = đứng ngoài chờ, đừng bắt dao rơi; cơ bản TRÁNH nhưng kỹ thuật đẹp = không mua (SEPA đòi cả hai).
- Cấm kỵ: hạ tiêu chuẩn Trend Template để "cho kịp sóng"; dời stop loss xuống khi giá giảm.
