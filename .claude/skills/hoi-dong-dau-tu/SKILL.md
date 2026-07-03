---
name: hoi-dong-dau-tu
description: Hội đồng đầu tư 5 agent đối kháng — triển khai song song 5 subagent độc lập (Đoàn Vĩnh Bình, Buffett, Munger, Lý Lục về CƠ BẢN + Minervini về KỸ THUẬT), mỗi agent tự nghiên cứu và chấm điểm riêng. Trưởng nhóm đọc thành 2 khối (không cộng gộp), tuyên bố chế độ đầu tư giá trị hay trader momentum, rồi ra quyết định theo ma trận cơ bản × kỹ thuật. Dùng cho quyết định quan trọng cần nhiều góc nhìn, ví dụ "/hoi-dong-dau-tu HPG".
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

## Bảng điểm — ĐỌC THÀNH 2 KHỐI, KHÔNG CỘNG GỘP
> Điểm cơ bản (giá trị) và điểm kỹ thuật (momentum) là hai đơn vị khác nhau —
> cộng chúng thành một con số /25 là phép cộng sai đơn vị (như cộng nhiệt độ với
> vận tốc). Đọc riêng từng khối rồi ra quyết định theo ma trận ở Bước 3.

**KHỐI CƠ BẢN** (trả lời: có nên sở hữu doanh nghiệp này, và đáng giá bao nhiêu?)
| Agent | Điểm | Kết luận 1 câu |
|---|---|---|
| Đoàn Vĩnh Bình (mô hình) | ★x | … |
| Buffett (định giá)       | ★x | … |
| Munger (rủi ro)          | ★x | … |
| Lý Lục (10 năm)          | ★x | … |
| **Đồng thuận cơ bản**    | ĐẠT / KHÔNG ĐẠT | [đạt = mô hình + định giá + 10 năm đều ổn và Munger không phủ quyết] |

**KHỐI KỸ THUẬT** (trả lời: dòng tiền sẵn sàng chưa, vào lệnh lúc nào?)
| Agent | Điểm | Kết luận 1 câu |
|---|---|---|
| Minervini (thời điểm) | ★x | Trend Template x/8 · Stage x · [MUA PIVOT/CHỜ/TRÁNH] |

## 🔥 ĐIỂM BẤT ĐỒNG (quan trọng nhất)
- Số liệu/nhận định nào các agent MÂU THUẪN nhau → vùng bất định thực sự
- Đặc biệt chú ý mâu thuẫn CƠ BẢN vs KỸ THUẬT (định giá rẻ nhưng Stage 4, hay đắt nhưng Stage 2 mạnh) — đây là thông tin, không phải lỗi

## TUYÊN BỐ CHẾ ĐỘ (Trưởng nhóm chọn 1 trước khi kết luận)
Cơ bản và kỹ thuật là hai trò chơi khác nhau (khác chu kỳ nắm giữ, khác quy tắc
bán, khác cắt lỗ). Không trộn — chọn chế độ cho vị thế này:
- **Chế độ ĐẦU TƯ GIÁ TRỊ**: cơ bản quyết định tất cả, chỉ mua DƯỚI giá trị nội
  tại; kỹ thuật chỉ để định thời điểm bên trong vùng tích luỹ (tránh bắt dao rơi).
  Cắt lỗ theo luận điểm, giữ nhiều năm.
- **Chế độ TRADER MOMENTUM**: cơ bản chỉ là bộ lọc chất lượng; kỹ thuật quyết định
  vào/ra hoàn toàn; chấp nhận trả TRÊN giá trị nội tại; stop giá 7–8% cứng; giữ
  tuần–tháng. (Lưu ý: "cơ bản" của Minervini là tăng trưởng lợi nhuận làm bộ lọc,
  KHÔNG phải biên an toàn.)

## MA TRẬN QUYẾT ĐỊNH (đọc mâu thuẫn cơ bản × kỹ thuật)
| Cơ bản | Kỹ thuật | Hành động |
|---|---|---|
| ĐẠT (rẻ) | Stage 2, có nền/pivot | ✅ Cả 2 chế độ đồng ý — hiếm, tin cậy cao nhất. MUA theo pivot, stop 7–8% |
| ĐẠT (rẻ) | Stage 4 đang rơi | ⚠️ Coi chừng BẪY GIÁ TRỊ. Chế độ giá trị: chờ đáy xác nhận + về vùng tích luỹ. Không bắt dao rơi dù rẻ |
| KHÔNG ĐẠT (đắt) | Stage 2 mạnh | ⚠️ TRADE MOMENTUM THUẦN. Chỉ vào nếu ở chế độ trader, stop chặt. Cấm gọi đây là "đầu tư" |
| KHÔNG ĐẠT (đắt) | Stage 4 | ⛔ Tệ cả hai — TRÁNH |

**Quy tắc vàng:** khi cơ bản và kỹ thuật ĐỘC LẬP cùng nói "CHỜ" (dù ở giá kích hoạt
khác nhau), không cần phân xử bên nào đúng — cả hai đồng ý về HÀNH ĐỘNG. Đây là tín
hiệu tin cậy cao nhất framework tạo ra.

## KẾT LUẬN: [MUA / TÍCH LUỸ / THEO DÕI / TRÁNH]
- CHẾ ĐỘ đã chọn: [Đầu tư giá trị / Trader momentum] — vì …
- Vùng tích luỹ (giá hợp lý): … | Vùng mua hời (hiếm): … | Giá hiện tại: …
- Điểm vào kỹ thuật (nếu chơi momentum): pivot … + stop … — GHI RÕ nếu điểm này
  cao hơn vùng tích luỹ giá trị (nghĩa là đây là trade, không phải đầu tư)
- Điều kiện vô hiệu hoá luận điểm: 1… 2… 3…
```

## Quy tắc
- 5 agent phải chạy **song song**, không tuần tự.
- Trưởng nhóm KHÔNG được sửa điểm của agent; chỉ tổng hợp và phân xử bằng chứng cứ.
- **CẤM cộng điểm cơ bản với điểm kỹ thuật thành một con số** — đọc thành 2 khối, quyết định theo ma trận.
- Nếu Munger ≤2★ → khối cơ bản tối đa là KHÔNG ĐẠT/THEO DÕI (quyền phủ quyết rủi ro).
- Minervini KHÔNG có quyền nâng kết luận cơ bản: cơ bản KHÔNG ĐẠT thì đồ thị đẹp cỡ nào cũng chỉ là trade momentum, cấm gọi là đầu tư; Minervini chỉ quyết thời điểm/cách vào lệnh.
- Vùng giá 2 tầng là bắt buộc: "vùng tích luỹ" cho doanh nghiệp chất lượng cao (Munger: "doanh nghiệp tuyệt vời ở giá hợp lý thắng doanh nghiệp hợp lý ở giá tuyệt vời"), "vùng mua hời" chỉ xuất hiện vài lần mỗi thập kỷ — ghi rõ cả hai để người đọc tự chọn khẩu vị.
- Khi điểm vào kỹ thuật (pivot) CAO hơn vùng tích luỹ giá trị → phải nói thẳng: mã này là cú trade, value và momentum không đồng ý ở bất kỳ giá nào, không phải khoản nắm giữ dài hạn kiểu Berkshire.
