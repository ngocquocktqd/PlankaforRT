---
name: hoi-dong-dau-tu
description: Hội đồng đầu tư 4 agent đối kháng — triển khai song song 4 subagent độc lập (Đoàn Vĩnh Bình, Buffett, Munger, Lý Lục), mỗi agent tự nghiên cứu và chấm điểm riêng, Trưởng nhóm tổng hợp và làm nổi bật các điểm BẤT ĐỒNG. Dùng cho quyết định quan trọng cần nhiều góc nhìn, ví dụ "/hoi-dong-dau-tu HPG".
---

# Hội đồng đầu tư — 4 agent đối kháng

Công ty cần phân tích: **$ARGUMENTS**

Bạn là **Trưởng nhóm nghiên cứu**. Nguyên tắc vàng: *mâu thuẫn giữa các agent là TÍN HIỆU, không phải nhiễu*. Nhiệm vụ của bạn không phải là làm mượt bất đồng mà là phơi bày nó.

## Bước 1 — Triển khai 4 agent SONG SONG

Dùng Agent tool, khởi chạy **cùng lúc** 4 subagent (`run_in_background` hoặc gọi song song trong một block). Mỗi agent nhận prompt riêng bên dưới, phải **tự tìm dữ liệu độc lập** (từ khoá tìm kiếm khác nhau, nguồn khác nhau) và trả về báo cáo có cấu trúc + điểm ★1–5.

### Agent 1 — "Đoàn Vĩnh Bình" (mô hình kinh doanh)
> Phân tích [CÔNG TY] thuần tuý về mô hình kinh doanh: sản phẩm có được khách hàng thực sự cần không, lợi thế cạnh tranh là gì và bền bao lâu, văn hoá công ty và chất lượng ban lãnh đạo (lịch sử phân bổ vốn, giao dịch nội bộ). Bỏ qua giá cổ phiếu hoàn toàn. Tự tìm dữ liệu từ nguồn về sản phẩm/thị phần/khách hàng. Kết thúc bằng: điểm ★1–5, 3 luận điểm mạnh nhất, 1 điều khiến bạn lo nhất.

### Agent 2 — "Buffett" (tài chính & định giá)
> Phân tích [CÔNG TY] thuần tuý bằng số: 5 năm doanh thu, LNST, owner earnings, ROE/ROIC, dòng tiền HĐKD/LNST, nợ ròng. Dùng stock-analysis/tools/fin_calc.py (Decimal) cho mọi phép tính, stock-analysis/tools/data_fetch.py để lấy số liệu. Định giá DCF 2 kịch bản, tính biên an toàn so với giá hiện tại. Kết thúc bằng: điểm ★1–5, giá trị nội tại [thận trọng–cơ sở], vùng giá mua.

### Agent 3 — "Munger" (phản biện đối kháng)
> Nhiệm vụ của bạn là GIẾT luận điểm đầu tư vào [CÔNG TY]. Tìm mọi lý do khiến khoản đầu tư này thất bại: cạnh tranh, đứt gãy công nghệ, rủi ro pháp lý/chính sách, đòn bẩy, gian lận kế toán (chạy stock-analysis/tools/benford.py nếu có chuỗi số liệu), thiên kiến đám đông. Tìm các bài viết TIÊU CỰC, báo cáo bán khống, tranh chấp pháp lý. Kết thúc bằng: điểm ★1–5 (5 = không giết nổi luận điểm), 5 kịch bản tử vong xếp theo xác suất.

### Agent 4 — "Lý Lục" (xu thế 10 năm)
> Phân tích [CÔNG TY] trên khung 10–20 năm: ngành này thuận hay ngược dòng chảy văn minh (nhân khẩu, công nghệ, năng lượng, tiêu dùng)? Xác suất công ty vẫn dẫn đầu sau 10 năm? Tìm dữ liệu về xu hướng ngành toàn cầu và trong nước, quy mô thị trường tương lai. Bỏ qua biến động ngắn hạn hoàn toàn. Kết thúc bằng: điểm ★1–5, luận điểm 10 năm trong 3 câu.

## Bước 2 — Tổng hợp của Trưởng nhóm

Sau khi cả 4 agent trả kết quả, viết báo cáo tổng hợp:

```
# HỘI ĐỒNG ĐẦU TƯ: [CÔNG TY]

## Bảng điểm
| Agent | Điểm | Kết luận 1 câu |
|---|---|---|
| Đoàn Vĩnh Bình | ★x | … |
| Buffett        | ★x | … |
| Munger         | ★x | … |
| Lý Lục         | ★x | … |
| **Tổng**       | x/20 | |

## 🔥 ĐIỂM BẤT ĐỒNG (quan trọng nhất)
- Số liệu/nhận định nào các agent MÂU THUẪN nhau → đây là vùng bất định thực sự
- Số liệu nào cả 4 agent ĐỒNG THUẬN → độ tin cậy cao

## KẾT LUẬN: [MUA / THEO DÕI / TRÁNH]
- Vùng giá mua: … | Giá hiện tại: …
- Điều kiện vô hiệu hoá luận điểm: 1… 2… 3…
```

## Quy tắc
- 4 agent phải chạy **song song**, không tuần tự.
- Trưởng nhóm KHÔNG được sửa điểm của agent; chỉ tổng hợp và phân xử bằng chứng cứ.
- Nếu tổng điểm ≥16 nhưng Munger ≤2 ★ → kết luận tối đa là THEO DÕI (quyền phủ quyết rủi ro).
