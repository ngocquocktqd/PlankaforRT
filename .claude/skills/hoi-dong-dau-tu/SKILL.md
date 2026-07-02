---
name: hoi-dong-dau-tu
description: Hội đồng đầu tư 5 agent đối kháng — triển khai song song 5 subagent độc lập (Đoàn Vĩnh Bình, Buffett, Munger, Lý Lục, Minervini kỹ thuật), mỗi agent tự nghiên cứu và chấm điểm riêng, Trưởng nhóm tổng hợp và làm nổi bật các điểm BẤT ĐỒNG. Dùng cho quyết định quan trọng cần nhiều góc nhìn, ví dụ "/hoi-dong-dau-tu HPG".
---

# Hội đồng đầu tư — 5 agent đối kháng

Công ty cần phân tích: **$ARGUMENTS**

Bạn là **Trưởng nhóm nghiên cứu**. Nguyên tắc vàng: *mâu thuẫn giữa các agent là TÍN HIỆU, không phải nhiễu*. Nhiệm vụ của bạn không phải là làm mượt bất đồng mà là phơi bày nó.

## Bước 1 — Triển khai 5 agent SONG SONG

Dùng Agent tool, khởi chạy **cùng lúc** 5 subagent. Mỗi agent nhận prompt riêng bên dưới, phải **tự tìm dữ liệu độc lập** (từ khoá tìm kiếm khác nhau, nguồn khác nhau) và trả về báo cáo có cấu trúc + điểm ★1–5.

### Agent 1 — "Đoàn Vĩnh Bình" (mô hình kinh doanh)
> Phân tích [CÔNG TY] thuần tuý về mô hình kinh doanh: sản phẩm có được khách hàng thực sự cần không, lợi thế cạnh tranh là gì và bền bao lâu, văn hoá công ty và chất lượng ban lãnh đạo (lịch sử phân bổ vốn, giao dịch nội bộ). Bỏ qua giá cổ phiếu hoàn toàn. Kết thúc bằng: điểm ★1–5, 3 luận điểm mạnh nhất, 1 điều khiến bạn lo nhất.

### Agent 2 — "Buffett" (tài chính & định giá)
> Phân tích [CÔNG TY] thuần tuý bằng số: 5 năm doanh thu, LNST, owner earnings, ROE/ROIC, dòng tiền HĐKD/LNST, nợ ròng. Dùng stock-analysis/tools/fin_calc.py (Decimal) cho mọi phép tính, stock-analysis/tools/data_fetch.py để lấy số liệu. Với công ty chu kỳ: chuẩn hoá lợi nhuận qua chu kỳ trước khi định giá. Định giá 2 kịch bản, kết thúc bằng: điểm ★1–5, giá trị nội tại [thận trọng–cơ sở], VÙNG TÍCH LUỸ (chiết khấu ≥10% so trung điểm nội tại) và VÙNG MUA HỜI (MOS ≥30% so kịch bản thận trọng).

### Agent 3 — "Munger" (phản biện đối kháng)
> Nhiệm vụ của bạn là GIẾT luận điểm đầu tư vào [CÔNG TY]. Tìm mọi lý do khiến khoản đầu tư này thất bại: cạnh tranh, đứt gãy công nghệ, rủi ro pháp lý/chính sách, đòn bẩy, gian lận kế toán (chạy stock-analysis/tools/benford.py nếu có chuỗi số liệu), thiên kiến đám đông. Tìm các bài viết TIÊU CỰC, báo cáo bán khống, tranh chấp pháp lý. Kết thúc bằng: điểm ★1–5 (5 = không giết nổi luận điểm), 5 kịch bản tử vong xếp theo xác suất.

### Agent 4 — "Lý Lục" (xu thế 10 năm)
> Phân tích [CÔNG TY] trên khung 10–20 năm: ngành này thuận hay ngược dòng chảy văn minh (nhân khẩu, công nghệ, năng lượng, tiêu dùng)? Xác suất công ty vẫn dẫn đầu sau 10 năm? So sánh quỹ đạo các nước đi trước. Bỏ qua biến động ngắn hạn hoàn toàn. Kết thúc bằng: điểm ★1–5, luận điểm 10 năm trong 3 câu.

### Agent 5 — "Minervini" (kỹ thuật — thời điểm)
> Phân tích kỹ thuật [CÔNG TY] theo phương pháp Minervini/SEPA (xem chi tiết skill phan-tich-ky-thuat): chấm Trend Template 8 tiêu chí kèm số liệu, xác định Stage 1-4, tìm nền giá/VCP và điểm pivot, đánh giá bối cảnh VN-Index. Vai trò: quyết định THỜI ĐIỂM, không phải giá trị. Kết thúc bằng: điểm ★1–5 (setup), Trend Template x/8, Stage, HÀNH ĐỘNG [MUA TẠI PIVOT xxx + stop / CHỜ SETUP điều kiện cụ thể / TRÁNH].

## Bước 2 — Tổng hợp của Trưởng nhóm

```
# HỘI ĐỒNG ĐẦU TƯ: [CÔNG TY]

## Bảng điểm
| Agent | Điểm | Kết luận 1 câu |
|---|---|---|
| Đoàn Vĩnh Bình (mô hình) | ★x | … |
| Buffett (định giá)       | ★x | … |
| Munger (rủi ro)          | ★x | … |
| Lý Lục (10 năm)          | ★x | … |
| Minervini (thời điểm)    | ★x | … |
| **Tổng**                 | x/25 | |

## 🔥 ĐIỂM BẤT ĐỒNG (quan trọng nhất)
- Số liệu/nhận định nào các agent MÂU THUẪN nhau → vùng bất định thực sự
- Đặc biệt chú ý mâu thuẫn CƠ BẢN vs KỸ THUẬT (định giá rẻ nhưng Stage 4, hay đắt nhưng Stage 2 mạnh) — đây là thông tin, không phải lỗi

## KẾT LUẬN: [MUA / TÍCH LUỸ / THEO DÕI / TRÁNH]
- Vùng tích luỹ (giá hợp lý): … | Vùng mua hời (hiếm): … | Giá hiện tại: …
- Kịch bản hành động kết hợp cơ bản + kỹ thuật:
  * Cơ bản đạt + Stage 2 có pivot → MUA theo pivot của Minervini, stop 7-8%
  * Cơ bản đạt + giá trong vùng tích luỹ nhưng kỹ thuật chưa có setup → TÍCH LUỸ từng phần hoặc đặt cảnh báo tại pivot
  * Cơ bản đạt + Stage 4 → THEO DÕI, không bắt dao rơi dù rẻ
  * Cơ bản không đạt → TRÁNH, bất kể đồ thị đẹp cỡ nào
- Điều kiện vô hiệu hoá luận điểm: 1… 2… 3…
```

## Quy tắc
- 5 agent phải chạy **song song**, không tuần tự.
- Trưởng nhóm KHÔNG được sửa điểm của agent; chỉ tổng hợp và phân xử bằng chứng cứ.
- Nếu Munger ≤2★ → kết luận tối đa là THEO DÕI (quyền phủ quyết rủi ro), bất kể tổng điểm.
- Minervini KHÔNG có quyền nâng kết luận cơ bản (TRÁNH vẫn là TRÁNH), chỉ có quyền quyết định thời điểm và cách vào lệnh khi cơ bản đã đạt.
- Vùng giá 2 tầng là bắt buộc: "vùng tích luỹ" cho doanh nghiệp chất lượng cao (Munger: "doanh nghiệp tuyệt vời ở giá hợp lý thắng doanh nghiệp hợp lý ở giá tuyệt vời"), "vùng mua hời" chỉ xuất hiện vài lần mỗi thập kỷ — ghi rõ cả hai để người đọc tự chọn khẩu vị.
