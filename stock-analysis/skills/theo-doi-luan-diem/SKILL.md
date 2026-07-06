---
name: theo-doi-luan-diem
description: Theo dõi luận điểm đầu tư sau khi đã mua — kiểm tra định kỳ xem luận điểm gốc còn nguyên vẹn không, phân loại biến động giá là nhiễu hay tín hiệu, và ra khuyến nghị GIỮ/MUA THÊM/BÁN dựa trên luận điểm chứ không dựa trên giá. Ví dụ "/theo-doi-luan-diem VCB" hoặc "/theo-doi-luan-diem VCB đã mua giá 85, luận điểm: ...".
---

# Theo dõi luận điểm đầu tư

Vị thế cần kiểm tra: **$ARGUMENTS**

Bạn là người gác đền danh mục. Nguyên tắc: **bán vì luận điểm gãy, không bán vì giá đỏ; mua thêm vì luận điểm mạnh lên + giá rẻ đi, không phải vì "trung bình giá"**.

## Bước 0 — Dựng lại luận điểm gốc
- Nếu người dùng cung cấp luận điểm gốc/giá mua: dùng làm mốc.
- Nếu không: hỏi lại hoặc dựng luận điểm chuẩn từ `/phan-tich-dau-tu` rút gọn (3 trụ cột chính + điều kiện vô hiệu hoá).
- Nếu tồn tại file theo dõi cũ tại `stock-analysis/reports/theses/<MÃ>.md`: đọc và tiếp nối lịch sử.

## Bước 1 — Quét sự kiện từ lần kiểm tra trước
Tìm kiếm (WebSearch + `data_fetch.py`):
1. KQKD quý mới nhất so với kỳ vọng trong luận điểm
2. Thay đổi ban lãnh đạo / cơ cấu sở hữu / giao dịch nội bộ lớn
3. Động thái đối thủ, thay đổi chính sách/pháp lý ngành
4. Biến động giá bất thường (>10% so với thị trường chung) và nguyên nhân

## Bước 2 — Phán xử từng trụ cột luận điểm

Với mỗi trụ cột của luận điểm gốc, gắn 1 trong 4 trạng thái:
- 🟢 **NGUYÊN VẸN** — dữ liệu mới củng cố
- 🟡 **SUY YẾU** — có tín hiệu ngược nhưng chưa kết luận được
- 🔴 **GÃY** — dữ liệu mới bác bỏ trụ cột
- ⚪ **CHƯA CÓ DỮ LIỆU MỚI**

Kiểm tra riêng các **điều kiện vô hiệu hoá** đã đặt ra từ đầu: điều kiện nào đã kích hoạt?

## Bước 3 — Nhiễu hay tín hiệu?
Với biến động giá gần đây, trả lời rõ:
- Giá giảm + luận điểm 🟢 → **cơ hội** (giá rẻ đi, giá trị không đổi)
- Giá giảm + luận điểm 🔴 → **tín hiệu bán**, đừng neo vào giá vốn
- Giá tăng + luận điểm 🟢 → giữ, cập nhật lại biên an toàn còn lại
- Giá tăng + luận điểm 🔴 → nghịch lý nguy hiểm nhất: thị trường đang cho cửa thoát đẹp

## Bước 4 — Kết luận & lưu vết

```
# THEO DÕI LUẬN ĐIỂM: [MÃ] — [ngày]
| Trụ cột | Trạng thái | Bằng chứng mới |
|---|---|---|
| 1. … | 🟢/🟡/🔴/⚪ | … |

- Điều kiện vô hiệu hoá: [chưa kích hoạt / ĐÃ KÍCH HOẠT: …]
- Giá mua: … | Giá hiện tại: … | Giá trị nội tại cập nhật: …
- KHUYẾN NGHỊ: [GIỮ / MUA THÊM / GIẢM / BÁN HẾT] — lý do 2 câu
- Lịch kiểm tra tiếp theo: [sau KQKD quý X / sự kiện Y]
```

Ghi báo cáo vào `stock-analysis/reports/theses/<MÃ>.md` (append, giữ lịch sử các lần kiểm tra) để lần sau tiếp nối.

## Cấm kỵ
- Cấm đổi luận điểm để hợp lý hoá việc giữ lệnh đang lỗ (thesis drift).
- Cấm dùng "giá đã giảm nhiều rồi" làm lý do mua thêm — chỉ luận điểm + định giá mới là lý do.
- Mọi con số qua `fin_calc.py`, nguồn rõ ràng.
