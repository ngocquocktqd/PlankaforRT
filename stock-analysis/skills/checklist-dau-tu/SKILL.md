---
name: checklist-dau-tu
description: Checklist 6 cổng kiểu Buffett — chấm nhanh một hoặc nhiều cổ phiếu qua 6 cổng tuần tự (hiểu được, con hào, ban lãnh đạo, tài chính, định giá, rủi ro đảo ngược); rớt cổng nào dừng ở cổng đó. Dùng để sàng nhanh trước khi phân tích sâu, ví dụ "/checklist-dau-tu MWG, FPT, PNJ".
---

# Checklist 6 cổng

Danh sách cổ phiếu: **$ARGUMENTS** (một hoặc nhiều mã, phân cách bằng dấu phẩy)

Chạy **tuần tự từng cổng** cho từng mã. Nguyên tắc phanh gấp: **rớt cổng nào, dừng ngay tại cổng đó** — không phân tích tiếp, ghi rõ lý do rớt. Điều này tiết kiệm thời gian và ép kỷ luật.

## Cổng 1 — Vòng tròn hiểu biết
- Mô tả mô hình kinh doanh trong đúng 2 câu mà một người ngoài ngành hiểu được.
- Kể tên: khách hàng trả tiền là ai, sản phẩm cạnh tranh trực tiếp là gì.
- ❌ Rớt nếu: mô hình quá phức tạp, doanh thu phụ thuộc yếu tố không thể dự đoán (giá hàng hoá thuần tuý, đầu cơ tài chính chéo).

## Cổng 2 — Con hào
- Xác định ≥1 lợi thế cạnh tranh CÓ CẤU TRÚC: hiệu ứng mạng, chi phí chuyển đổi, thương hiệu định giá được, lợi thế chi phí/quy mô, giấy phép độc quyền.
- Bằng chứng định lượng: biên gộp ổn định/cao hơn ngành, ROIC > WACC liên tục 5 năm.
- ❌ Rớt nếu: chỉ có "giá rẻ hơn đối thủ" hoặc "ngành đang hot" làm lợi thế.

## Cổng 3 — Ban lãnh đạo
- Lịch sử phân bổ vốn 5 năm: cổ tức, mua lại, M&A có tạo giá trị không?
- Giao dịch nội bộ 12 tháng: lãnh đạo đang mua hay bán? Cầm cố cổ phiếu?
- Có bê bối, án phạt, giải trình bất thường với sở giao dịch không?
- ❌ Rớt nếu: có dấu hiệu chiếm đoạt giá trị cổ đông nhỏ (phát hành riêng lẻ giá rẻ cho bên liên quan, giao dịch lòng vòng).

## Cổng 4 — Sức khoẻ tài chính
Tính bằng `stock-analysis/tools/fin_calc.py` với dữ liệu từ `data_fetch.py`:
- ROE 5 năm ≥ 15% (hoặc ≥ 12% nếu không dùng đòn bẩy)
- CFO/LNST 5 năm ≥ 0.8
- Nợ ròng/EBITDA ≤ 2.5×
- Tăng trưởng EPS 5 năm > 0 (không bị pha loãng ăn mòn)
- ❌ Rớt nếu: vi phạm ≥2 chỉ tiêu, hoặc CFO/LNST < 0.5.

## Cổng 5 — Định giá
- DCF nhanh kịch bản thận trọng (`fin_calc.py dcf`) HOẶC so P/E, EV/EBITDA với trung vị lịch sử 10 năm của chính nó.
- ❌ Rớt nếu: giá hiện tại > 90% giá trị nội tại thận trọng (không còn biên an toàn).

## Cổng 6 — Đảo ngược kiểu Munger
- Nêu 3 kịch bản giết chết khoản đầu tư và tự đánh giá xác suất.
- ❌ Rớt nếu: tồn tại ≥1 kịch bản xác suất CAO mà không có cách phòng vệ.

## Đầu ra

```
# CHECKLIST 6 CỔNG
| Mã | C1 | C2 | C3 | C4 | C5 | C6 | Kết quả |
|---|---|---|---|---|---|---|---|
| MWG | ✅ | ✅ | ✅ | ❌ | – | – | RỚT CỔNG 4: CFO/LNST 0.45 |
| FPT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | QUA — đáng chạy /phan-tich-dau-tu |

## Chi tiết từng mã
[với mỗi mã: bằng chứng ngắn gọn từng cổng đã chạy, số liệu kèm nguồn]
```

## Quy tắc
- So sánh nhiều mã thì format phải đồng nhất để đặt cạnh nhau được.
- Cổng 4–5 bắt buộc có số thật, không ước lượng chay.
- "QUA cả 6 cổng" ≠ khuyến nghị mua — chỉ có nghĩa là xứng đáng nghiên cứu sâu.
