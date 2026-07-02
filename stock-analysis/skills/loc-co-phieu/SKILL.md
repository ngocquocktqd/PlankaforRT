---
name: loc-co-phieu
description: Phễu lọc ngành 30 → 10 → 3 — lập bản đồ chuỗi giá trị của một ngành, liệt kê ~30 công ty, lọc còn 10 bằng chỉ tiêu cứng, chọn 3 ứng viên tốt nhất để nghiên cứu sâu. Dùng khi người dùng muốn tìm cổ phiếu trong một ngành/chủ đề, ví dụ "/loc-co-phieu ngành bán lẻ" hoặc "/loc-co-phieu AI data center".
---

# Phễu lọc ngành 30 → 10 → 3

Ngành / chủ đề: **$ARGUMENTS**

Bạn là nhà nghiên cứu ngành. Mục tiêu: từ toàn cảnh ngành, thu hẹp còn **3 ứng viên** xứng đáng chạy `/phan-tich-dau-tu` đầy đủ.

## Vòng 1 — Bản đồ chuỗi giá trị (~30 công ty)

1. Vẽ chuỗi giá trị của ngành: thượng nguồn → trung nguồn → hạ nguồn (nguyên liệu, sản xuất, phân phối, dịch vụ đi kèm).
2. Với mỗi mắt xích, liệt kê các công ty niêm yết liên quan (ưu tiên VN nếu chủ đề trong nước; thêm công ty quốc tế đầu ngành làm chuẩn so sánh).
3. Đánh dấu **điểm nghẽn (bottleneck)** của chuỗi: mắt xích nào khan hiếm nhất, có quyền định giá nhất? Công ty ở điểm nghẽn thường là mỏ vàng.
4. Xuất bảng: `Công ty | Sàn | Mắt xích | Vốn hoá | Vai trò trong chuỗi`.

## Vòng 2 — Lọc cứng còn ~10

Loại thẳng tay bằng chỉ tiêu định lượng (lấy số bằng `data_fetch.py`, tính bằng `fin_calc.py`):

| Chỉ tiêu | Ngưỡng loại |
|---|---|
| ROE trung bình 5 năm | < 12% |
| CFO/LNST trung bình 5 năm | < 0.7 |
| Nợ ròng/EBITDA | > 3× (trừ ngân hàng/BĐS xét riêng) |
| Tăng trưởng doanh thu 5 năm (CAGR) | < 5%/năm |
| Thanh khoản | quá thấp để giải ngân thực tế |
| Lịch sử pha loãng | phát hành ồ ạt làm EPS đi lùi |

Với mỗi công ty bị loại: ghi 1 dòng lý do. Với 10 công ty còn lại: bảng so sánh đủ 6 chỉ tiêu.

## Vòng 3 — Chọn 3 bằng chỉ tiêu mềm

Chấm ★1–5 từng công ty trên 4 tiêu chí:
1. **Con hào** — lợi thế cạnh tranh có cấu trúc không (mạng lưới, chuyển đổi, thương hiệu, quy mô, giấy phép)?
2. **Ban lãnh đạo** — phân bổ vốn khôn ngoan, minh bạch, không tai tiếng?
3. **Vị thế trong chuỗi** — có nằm ở điểm nghẽn không?
4. **Định giá sơ bộ** — P/E, EV/EBITDA so với chất lượng và lịch sử chính nó?

## Đầu ra

```
# PHỄU LỌC: [NGÀNH]
## Bản đồ chuỗi giá trị + điểm nghẽn
## Vòng 1: 30 công ty (bảng)
## Vòng 2: 10 công ty qua lọc cứng (bảng so sánh) + lý do loại từng công ty
## Vòng 3: TOP 3
| # | Công ty | Điểm | Luận điểm 2 câu | Bước tiếp theo |
|---|---|---|---|---|
| 1 | … | x/20★ | … | /phan-tich-dau-tu … |
## Rủi ro chung của cả ngành (3 gạch đầu dòng)
```

## Quy tắc
- Không nhồi công ty cho đủ 30 — nếu ngành hẹp, ghi rõ "ngành chỉ có N công ty niêm yết".
- Chuẩn so sánh quốc tế bắt buộc có ≥1 công ty để định vị mặt bằng biên lợi nhuận.
- Số liệu vòng 2 phải có nguồn; nghi ngờ thì gắn nhãn C và ghi chú.
