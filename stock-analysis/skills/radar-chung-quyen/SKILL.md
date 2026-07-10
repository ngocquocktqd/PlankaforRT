---
name: radar-chung-quyen
description: Radar quét chứng quyền (CW) — TÌM mã CW đáng theo dõi để lướt vài tuần, đứng TRƯỚC /hoi-dong-chung-quyen. Lọc GIAO của 2 tập (cơ sở đang Stage 2 + có catalyst gần VÀ bản thân mã CW có cấu trúc tốt: đủ đáo hạn, ATM–ITM, đòn bẩy hiệu dụng 3–6x, IV không thổi, thanh khoản). Phân nhóm watchlist CW theo mức hành động kèm chỉ số (đòn bẩy hiệu dụng, IV, % hòa vốn, theta, đáo hạn). Dùng "/radar-chung-quyen" (toàn thị trường) hoặc "/radar-chung-quyen FPT" (theo cơ sở).
---

# Radar chứng quyền — quét mã CW đáng theo dõi (vài tuần)

Phạm vi: **$ARGUMENTS** (trống = quét CW trên các cơ sở VN30 đang khỏe; hoặc theo cơ sở
chỉ định như "FPT", "HPG").

Bạn là **người vận hành radar CW**. Nhiệm vụ: lọc ra 3–5 mã CW đáng đưa vào watchlist,
mỗi mã kèm cơ sở + chỉ số CW + điểm kích hoạt sơ bộ. Radar chỉ **SÀNG** — mã CW lọt phải
qua `/hoi-dong-chung-quyen` (3 vai) trước khi vào lệnh thật.

> 🎯 Nguyên tắc sống còn: một mã CW chỉ đáng nếu ở **GIAO của 2 tập** —
> **(A) CƠ SỞ** đang Stage 2 + catalyst trong 2–6 tuần + biên độ kỳ vọng đủ, **VÀ**
> **(B) BẢN THÂN CW** có cấu trúc tốt (đủ đáo hạn, ATM–ITM, đòn bẩy 3–6x, IV không thổi,
> thanh khoản). Cơ sở đẹp mà chỉ có CW rác (sắp đáo hạn/IV cao/OTM sâu) = **loại**. CW
> "rẻ" trên cơ sở đi ngang = theta bào chết. Thiếu một trong hai = loại.

## Bước 0 — Bối cảnh (CW khắt khe hơn cổ phiếu)
CW chỉ có call + đòn bẩy cực đại → chỉ quét khi thị trường thực sự thuận:
- 🟢 **THUẬN** (VN-Index Stage 2, breadth tốt) → quét bình thường.
- 🟡 **HẸP** → chỉ CW trên nhóm dẫn dắt, ưu tiên ITM (delta cao, ít phụ thuộc IV), cảnh báo.
- 🔴 **Stage 4** → trả "đứng ngoài, CW cấm chơi" và DỪNG. Không nặn mã.

## Bước 0.5 — Bản đồ CƠ SỞ khỏe (tập A)
CW chỉ phát hành trên **rổ VN30 thanh khoản cao**. Xác định **2–4 cơ sở** vừa **Stage 2**
vừa có **catalyst 2–6 tuần** vừa **biến động đủ lớn** để CW chạy (cơ sở lờ đờ → loại ngay,
CW chỉ chết vì theta). Nếu vừa chạy `/radar-luot-song`, lấy các mã nhóm 🟢 A thuộc VN30 làm
cơ sở ứng viên — đây là cầu nối tự nhiên giữa 2 radar.

## Chọn chế độ dữ liệu
- **Bảng giá CW của CTCK** (SSI/HSC/VND/MBS/KIS/VCSC, cafef "chứng quyền", vietstock) là nguồn
  gốc cho mã CW/giá TH/tỷ lệ/đáo hạn/giá/bid-ask. Đây là dữ liệu THAY ĐỔI HÀNG NGÀY.
- **WebSearch (mặc định sandbox):** tổng hợp nhanh 3–5 lượt, phần lớn nhãn **C** vì trễ →
  radar CW chỉ là danh sách THEO DÕI, mọi con số phải kiểm lại trên bảng giá sống trước lệnh.
- Tính chỉ số bằng `stock-analysis/tools/cw_calc.py metrics` cho từng CW.

## Vòng 1 — QUÉT: gom CW trên các cơ sở tập A
Với mỗi cơ sở khỏe (Bước 0.5), liệt kê các mã CW đang niêm yết + tham số thô:
`Mã CW | Cơ sở | Issuer | Giá TH | Tỷ lệ | Đáo hạn (còn ~ngày) | Giá CW`.
Bỏ ngay CW trên cơ sở KHÔNG Stage 2 (không thuộc tập A) — dù CW đó "rẻ".

## Vòng 2 — LỌC GIAO 2 TẬP: giữ CW đạt CẢ HAI
Chạy `cw_calc.py metrics` từng mã, chỉ giữ CW qua **tất cả** (rớt tiêu chí nào ghi 1 dòng):
- **Đáo hạn ≥ ~2 tháng** (loại < 45 ngày — vách theta / gần ngày GD cuối).
- **ATM đến hơi ITM** (delta ~0,5–0,75) — loại OTM sâu (vé số) và quá sâu ITM (hết đòn bẩy).
- **Đòn bẩy HIỆU DỤNG ~3–6x** (loại < 2x vô nghĩa, > 8x bom gamma/theta).
- **IV không bị thổi** — so IV giữa các CW cùng cơ sở và với biến động lịch sử; loại mã IV
  cao bất thường (trả đắt, dễ IV crush), đặc biệt nếu cơ sở sắp có KQKD.
- **% cơ sở cần tăng để hòa vốn < biên độ kỳ vọng** của cơ sở (nếu không, toán không ra).
- **Thanh khoản đủ + spread hẹp** (nhà tạo lập niêm yết đều, có khối lượng).
- **Tối đa 2 CW/cơ sở**, và tránh dồn nhiều CW cùng một nhóm ngành cơ sở.

Bảng: `Mã CW | Cơ sở(Stage) | Đáo hạn | Trạng thái | Đòn bẩy HD | IV | %hòa vốn | Theta/ngày | Cờ`.

## Vòng 3 — PHÂN NHÓM HÀNH ĐỘNG cho TOP 3–5
- 🟢 **A — SẴN ĐÁNH**: cơ sở vừa/đang phá pivot + CW đạt chuẩn → kích hoạt theo tín hiệu cơ sở.
- 🟡 **B — CHỜ CƠ SỞ**: CW tốt nhưng cơ sở chưa phá pivot → đặt alert trên GIÁ CƠ SỞ.
- 🔴 **C — LOẠI/CẢNH BÁO**: cơ sở extended hoặc CW dính cờ (đáo hạn gần/IV cao) → không đuổi.

Mỗi CW nhóm A–B ghi: mã CW, kích hoạt = **pivot của CƠ SỞ** (không phải giá CW), đòn bẩy
hiệu dụng, % hòa vốn, đáo hạn còn bao ngày, catalyst, cờ 🕐 (KQKD trong ≤2 tuần → IV crush).

```
# RADAR CW: [phạm vi] — [ngày]
## Bối cảnh: VN-Index Stage x · breadth [tốt/hẹp] → CW [chơi/hạn chế/cấm]
## Cơ sở khỏe (tập A): 1[Stage] 2[Stage] 3[Stage]
## Watchlist CW
| Nhóm | Mã CW | Cơ sở | Đáo hạn | Trạng thái | Đòn bẩy HD | IV | %hòa vốn | Kích hoạt (cơ sở) | Cờ |
|---|---|---|---|---|---|---|---|---|---|
| 🟢 A | … | …(St2) | …ngày | ATM/ITM | ~kx | n% | +m% | phá pivot … | |
| 🟡 B | … | …(St2) | …ngày | … | ~kx | n% | +m% | alert cơ sở … | 🕐 |
## Đã loại Vòng 2 (1 dòng/mã: đáo hạn gần / IV thổi / OTM sâu / cơ sở không Stage 2)
## Bước tiếp: /hoi-dong-chung-quyen cho các CW nhóm A–B trước khi vào lệnh
```

**Lưu vết:** ghi vào `stock-analysis/reports/chungquyen.md` (kèm ngày). CW đổi nhanh (đáo hạn
trôi, IV đổi) nên "độ bền" ít ý nghĩa hơn cổ phiếu — thay vào đó theo dõi **cơ sở** có giữ
Stage 2 giữa các lần quét không; cơ sở gãy Stage 2 → xoá mọi CW của nó khỏi watchlist.

## Quy tắc thép
- Radar chỉ SÀNG: CW nhóm A–B phải qua `/hoi-dong-chung-quyen` (3 vai) mới vào lệnh.
- **Cơ sở là gốc**: không quét CW trên cơ sở ngoài Stage 2; cơ sở Stage 4 → cả rổ CW của nó bị loại.
- CẤM surface CW "đòn bẩy khủng" mà thực chất OTM sâu/sắp đáo hạn (đòn bẩy đơn giản cao nhưng
  delta thấp = bom theta) — dùng **đòn bẩy HIỆU DỤNG** (delta × đòn bẩy đơn giản), không phải đòn bẩy đơn giản.
- Kích hoạt & stop luôn theo **GIÁ CƠ SỞ**, không theo giá CW.
- 🔴 Stage 4 hoặc breadth quá hẹp → đứng ngoài, không nặn CW.
- Mọi số CW nhãn C (WebSearch trễ) → PHẢI kiểm lại trên bảng giá chứng quyền sống trước lệnh.
- Kết thúc bằng: "⚠️ Nghiên cứu học tập, không phải khuyến nghị đầu tư. CW là đòn bẩy rủi ro
  rất cao, có thể mất toàn bộ vốn."
