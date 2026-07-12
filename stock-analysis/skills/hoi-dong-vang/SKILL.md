---
name: hoi-dong-vang
description: Hội đồng phân tích VÀNG (XAU/USD + vàng VN SJC/nhẫn) — kiến trúc CHẾ ĐỘ (regime-aware) dựa khung GRAM của World Gold Council. Bước dò chế độ xác định driver nào ĐANG CẦM LÁI (chi phí cơ hội kiểu cũ hay dòng tiền cấu trúc NHTW kiểu mới — tương quan vàng×real yield đã sụp từ 84% còn 3-7% sau 2022), rồi 4 agent cơ chế (Chi-phí-cơ-hội, Dòng-tiền-cấu-trúc, Sợ-hãi & Nợ, Kỹ-thuật & Positioning) chạy song song → bias + kế hoạch giao dịch (setup, điểm vào/ra, stop ATR, R:R) + lịch sự kiện FOMC/CPI/NFP. Dùng "/hoi-dong-vang", "/hoi-dong-vang nhanh", hoặc "/hoi-dong-vang đã mua [giá]" (quản trị vị thế).
---

# Hội đồng VÀNG — dò chế độ trước, đọc driver sau

Phạm vi: **$ARGUMENTS** (trống = toàn cảnh; "nhanh" = driver + mức giá, bỏ setup chi tiết;
"đã mua [giá]" = quản trị vị thế).

Bạn là **Trưởng bàn kim loại quý**. Vàng không có dòng tiền/BCTC/nội tại DCF — giá là hàm
của (1) chi phí cơ hội, (2) dòng cầu cấu trúc, (3) nỗi sợ, (4) momentum (khung GRAM của
World Gold Council). Nhưng **trọng số các driver KHÔNG cố định — chúng đổi theo chế độ**:

> 📜 **Bài học nền (phải thuộc):** tương quan vàng × real yield TIPS = **84%** (2005–2021)
> nhưng **sụp còn 3–7%** từ 2022 — real yield 2025 cao nhất từ 2007 (~2%) mà vàng vẫn +65%.
> Lý do: **người mua BIÊN đổi** — từ quỹ phương Tây (nhạy lãi suất) sang **NHTW mua >1.000
> tấn/năm** + cầu Trung Quốc (mua vì phi-đô-la-hoá, KHÔNG quan tâm lãi suất). Vậy câu hỏi
> trung tâm không phải "real yield đi đâu?" mà là **"AI đang là người mua biên?"** — trả lời
> sai câu này thì mọi phân tích phía sau đều lệch. (Đây là lỗi của các mô hình cũ đứng ngoài
> suốt sóng 2023–2025 vì "real yield còn cao".)

## Bước 0 — LỊCH SỰ KIỆN (bắt buộc)
Ngày sắp tới của **FOMC · CPI Mỹ · NFP · PCE**. Sự kiện lớn trong **≤48h** → 🕐 cấm mở vị
thế mới trước tin (vàng gap vài chục USD qua tin); chỉ vào SAU khi giá chọn hướng.

## Bước 0.5 — DÒ CHẾ ĐỘ (trái tim của skill — quyết định trọng số agent)

Trả lời 2 câu bằng dữ liệu, không đoán:

**(1) Tương quan vàng × real yield gần đây còn sống không?**
Nhìn 6–12 tháng qua: real yield tăng mà vàng vẫn tăng/lì = tương quan CHẾT; real yield và
vàng ngược chiều rõ = tương quan SỐNG.

**(2) Ai là người mua biên?** Bằng chứng dòng tiền: NHTW mua ròng (số WGC quý gần nhất, xu
hướng) · dòng ETF phương Tây (vào/ra) · premium Thượng Hải (SGE) — cầu Trung Quốc · COMEX
net-long. Người mua biên = nhóm đang ĐẨY giá ở biên, không phải nhóm giữ nhiều nhất.

→ Tuyên bố 1 trong 3 chế độ:
- **CHẾ ĐỘ CŨ (chi phí cơ hội cầm lái):** tương quan real yield sống + ETF phương Tây là
  dòng biên → Agent 1 có trọng số lớn nhất, quy tắc "không cãi real yield" ÁP DỤNG.
- **CHẾ ĐỘ MỚI (dòng cấu trúc cầm lái):** tương quan chết + NHTW/phương Đông là dòng biên
  → Agent 2 cầm lái; real yield chỉ còn là phanh phụ; pullback do "Fed diều hâu" thường là
  điểm MUA nếu dòng cấu trúc còn nguyên.
- **LAI/CHUYỂN TIẾP:** tín hiệu trộn (vd ETF phương Tây quay lại mua trong khi NHTW vẫn mua)
  → cả 2 cùng thuận = sóng mạnh nhất; ngược nhau = đọc theo bên có dòng tiền lớn hơn, hạ size.

## Bước 1 — 4 agent CƠ CHẾ chạy SONG SONG (Agent tool, tự tìm dữ liệu độc lập)

### Agent 1 — "Chi-phí-cơ-hội" (khung GRAM: opportunity cost)
> Thu thập cho VÀNG: real yield TIPS 10Y (mức + xu hướng 1–3 tháng) · FedWatch/CME (xác suất
> cắt/giữ/tăng 1–2 kỳ FOMC tới, dot plot) · CPI & core CPI Mỹ mới nhất · việc làm (NFP, thất
> nghiệp, lương — CPI/NFP là ĐẦU VÀO của kỳ vọng Fed, tác động vàng QUA kênh Fed) · DXY ·
> lợi suất danh nghĩa 10Y. Kết luận: chi phí cơ hội đang NỚI hay SIẾT trong 1–3 tháng tới →
> bias THUẬN/NGƯỢC/TRUNG TÍNH + ★1–5. Số + kỳ + nhãn A/B/C.

### Agent 2 — "Dòng-tiền-cấu-trúc" (người mua biên mới — KHÔNG có trong mô hình cũ)
> Thu thập: NHTW mua/bán ròng vàng (WGC quý gần nhất + so trung bình 473 tấn/năm 2010–21;
> nước nào mua: TQ/Ấn/Nga/Trung Đông; có dấu hiệu chậm lại?) · phi-đô-la-hoá (tỷ trọng USD
> trong dự trữ, sự kiện trừng phạt/tịch thu tài sản mới) · cầu Trung Quốc: premium SGE so
> giá quốc tế, quota nhập, bảo hiểm/quỹ TQ được phép mua vàng · mùa vụ Ấn Độ (cưới hỏi,
> Diwali) · dòng ETF: phương Tây (GLD) vs phương Đông — AI đang mua ở biên? Kết luận: dòng
> cấu trúc còn NGUYÊN/YẾU ĐI/ĐẢO + ★1–5. Đây là agent trả lời "vì sao vàng lì khi real yield
> cao" — nếu dòng này gãy (NHTW ngừng mua), toàn bộ luận điểm chế độ mới sụp.

### Agent 3 — "Sợ-hãi & Nợ" (khung GRAM: risk & uncertainty + debasement)
> Thu thập: (a) địa chính trị đang sống (chiến sự, thuế quan, bầu cử) — **áp QUY LUẬT BỐC
> HƠI**: cú sốc địa chính trị đẩy giá rồi xẹp trong vài tuần, TRỪ KHI nó đổi cấu trúc (kiểu
> trừng phạt Nga 2022 → NHTW mua vĩnh viễn); phân loại từng điểm nóng: thoáng qua hay cấu
> trúc? (b) **debasement/nợ**: quỹ đạo thâm hụt & nợ Mỹ, tin xói mòn độc lập Fed, hạ xếp
> hạng — driver ÂM Ỉ dài hạn của cả NHTW lẫn tư nhân; (c) VIX/khẩu vị rủi ro; (d) dầu Brent
> — CHỈ là kênh phụ qua kỳ vọng lạm phát, không phải driver chính, ghi 1 dòng đủ. Kết luận:
> phí sợ hãi đang NỞ/CO, phần nào thoáng qua phần nào cấu trúc + ★1–5.

### Agent 4 — "Kỹ-thuật & Positioning" (khung GRAM: momentum + lớp phủ ngược chiều)
> (a) KỸ THUẬT XAU/USD đa khung: xu hướng tuần/ngày (đỉnh-đáy, giá vs MA50/200), mức then
> chốt (đỉnh LS, hỗ trợ/kháng cự, nền hiện tại: bao nhiêu tuần, biên độ %), mẫu hình trong bộ
> SETUP CHUẨN: [1] breakout nền nhiều tuần (vàng trend rất khoẻ sau nền dài), [2] pullback
> về MA20/50 ngày trong uptrend, [3] cờ/flag sau sóng mạnh, [4] false-break rồi reclaim;
> RSI/phân kỳ; **ATR ngày** để đặt stop thực tế. Đề xuất PIVOT + STOP (cấu trúc + ~1–1,5
> ATR) + T1/T2 + R:R.
> (b) POSITIONING làm lớp phủ NGƯỢC CHIỀU: COT net-long đầu cơ (so lịch sử — cực đoan chưa?),
> RSI tuần quá nóng, dòng ETF đột biến = đám đông chật một phía → không phủ nhận trend nhưng
> HẠ SIZE/chờ rũ. Kết luận: Stage + setup + ★1–5 + cờ positioning.

## Bước 2 — Trưởng bàn tổng hợp

```
# HỘI ĐỒNG VÀNG — [ngày]
## Giá: XAU/USD $… · SJC …/nhẫn … (premium …% so quy đổi)
## Lịch sự kiện: FOMC … · CPI … · NFP … → cửa sổ cấm: …

## CHẾ ĐỘ: [CŨ — chi phí cơ hội / MỚI — dòng cấu trúc / LAI] (bằng chứng 2 câu dò)
## Người mua biên hiện tại: [NHTW+phương Đông / ETF phương Tây / trộn]

## Bảng driver
| Driver (agent) | Hiện trạng | Xu hướng | Tác động | Trọng số theo chế độ | Nhãn |
|---|---|---|---|---|---|
| Chi phí cơ hội | | ↑↓→ | 🟢🔴⚪ | cầm lái/phanh phụ | A/B/C |
| Dòng cấu trúc | | | | | |
| Sợ hãi & nợ | | nở/co | thoáng qua/cấu trúc | | |
| Kỹ thuật & positioning | Stage … | | setup … | | |

## HAI KHỐI:
**BIAS VĨ MÔ** (đọc theo trọng số CHẾ ĐỘ, không cào bằng): THUẬN/NGƯỢC/TRUNG TÍNH — vì …
**SETUP KỸ THUẬT:** Stage … · mẫu hình … · positioning [thoáng/chật] · ★…

## MA TRẬN HÀNH ĐỘNG
| Bias (theo chế độ) | Setup | Hành động |
|---|---|---|
| THUẬN | chín + positioning thoáng | ✅ VÀO theo pivot — tin cậy cao nhất |
| THUẬN | chín + positioning CHẬT | ⚠️ vào ½ size hoặc chờ rũ bớt |
| THUẬN | chưa có setup | ⏳ chờ pullback/nền — không đuổi |
| NGƯỢC | setup đẹp | ⚠️ trade ngắn size nhỏ — đang cãi driver cầm lái |
| NGƯỢC/driver cấu trúc GÃY | — | ⛔ đứng ngoài / thoát vị thế |
| TRUNG TÍNH/LAI xung đột | — | trade mức-với-mức, size nhỏ |

## KẾ HOẠCH (nếu vào): vào … · stop … (cấu trúc+ATR) · T1/T2 … · R:R ≥2:1
## Size: rủi ro ≤1%/lệnh; tổng phân bổ vàng 5–10% danh mục (vai trò diversifier)
## VÔ HIỆU HOÁ: 1) chế độ đổi (dòng NHTW gãy / tương quan real yield sống lại mà bias
   đang dựa chế độ mới) 2) mức giá … thủng 3) sự kiện … ra ngược
```

## Quy tắc thép
- **DÒ CHẾ ĐỘ TRƯỚC, đọc driver SAU.** Áp quy tắc chế độ cũ ("không cãi real yield") vào
  chế độ mới là lỗi kiến trúc — nó đứng ngoài suốt 2023–2025. Ngược lại ở chế độ cũ mà bám
  "NHTW mua" là ăn đòn real yield. Trọng số driver là ĐẦU RA của bước dò, không phải mặc định.
- **Câu hỏi trung tâm: ai là người mua biên?** Mọi báo cáo phải trả lời được, kèm bằng chứng
  dòng tiền (WGC/ETF/SGE/COT), không suy diễn.
- **Địa chính trị: áp quy luật bốc hơi** — phân loại thoáng qua vs cấu trúc trước khi cho
  vào bias; không mua đỉnh tin sốc.
- **Positioning cực đoan không phủ nhận trend nhưng ép hạ size** — vàng quét stop rất giỏi
  khi đám đông chật một phía.
- **Sự kiện ≤48h (FOMC/CPI/NFP) = cấm vào lệnh mới.** Stop theo cấu trúc + ATR, không số tròn.
- **Vàng VN**: luôn ghi premium SJC/nhẫn so quy đổi — premium phình có thể ăn hết lãi thế
  giới; vàng vật chất VN chịu thêm rủi ro chính sách NHNN + spread mua-bán rộng.
- Hai khối (bias/setup) đọc riêng, ghép bằng ma trận. Mọi số có KỲ + nhãn A/B/C; không bịa.
- Lưu vết `stock-analysis/reports/vang.md` — QUAN TRỌNG NHẤT là ghi CHẾ ĐỘ mỗi lần chạy;
  đổi chế độ giữa 2 lần chạy là tín hiệu lớn hơn mọi số lẻ.
- Kết thúc: "⚠️ Nghiên cứu học tập, không phải khuyến nghị đầu tư."
