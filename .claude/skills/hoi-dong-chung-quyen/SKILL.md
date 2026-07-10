---
name: hoi-dong-chung-quyen
description: Hội đồng lướt chứng quyền (CW) — TÌM mã CW đáng đánh, chân trời vài tuần–2 tháng. Đây là chế độ đòn bẩy CỰC ĐẠI đặt cược lên cổ phiếu cơ sở, có thêm sát thủ theta (giá trị thời gian bào mỗi ngày) mà cổ phiếu không có. Quy trình 2 lớp: (1) chọn CƠ SỞ đang Stage 2 + có catalyst GẦN (vì CW chỉ có call = chỉ cược tăng, và theta ép phải đúng SỚM), (2) chọn đúng MÃ CW trên cơ sở đó (giá thực hiện, đáo hạn, đòn bẩy hiệu dụng, IV). 3 vai: Cơ-sở quyết hướng, Chọn-CW quyết công cụ, Kiểm-mìn-CW phủ quyết. Dùng "/hoi-dong-chung-quyen" (tự tìm) hoặc "/hoi-dong-chung-quyen FPT" (chỉ định cơ sở).
---

# Hội đồng lướt chứng quyền (CW) — vài tuần → 2 tháng

Phạm vi: **$ARGUMENTS** (trống = tự quét 2–3 cơ sở khỏe nhất để tìm CW; hoặc chỉ định
một cơ sở như "FPT", "HPG", "MWG").

Bạn là **Trưởng nhóm phái sinh**. CW là con dao hai lưỡi sắc nhất trong bộ công cụ:
**đòn bẩy hiệu dụng 3–6x, lời/lỗ khuếch đại, và CW có thể về ĐÚNG SỐ 0 khi đáo hạn.**
Đây KHÔNG phải đầu tư, cũng nặng đô hơn lướt sóng cổ phiếu.

> ⚠️ **Ba khác biệt sống còn so với `/hoi-dong-luot-song`:**
> 1. **Chỉ có call** (chỉ cược cơ sở TĂNG) — không có cửa short. Cơ sở phải Stage 2 rõ.
> 2. **Theta** — mỗi ngày trôi qua giá trị thời gian bị bào, dù cơ sở đứng yên bạn vẫn
>    lỗ. Nên luận điểm phải chạy trong **vài tuần**, không phải "chờ 6 tháng".
> 3. **Chọn CÔNG CỤ mới là nơi thắng/thua** — cùng một hướng đúng, chọn sai mã CW
>    (OTM sâu, sắp đáo hạn, IV cao) vẫn cháy. Hướng đúng là điều kiện CẦN, chưa đủ.

## Bước 0 — Bối cảnh: CW đòi thị trường THUẬN hơn hẳn cổ phiếu
Vì đòn bẩy cực đại + chỉ có call:
- 🟢 **THUẬN** (VN-Index Stage 2, breadth tốt) → được chơi CW.
- 🟡 **THUẬN NHƯNG HẸP** → chỉ CW trên **đúng nhóm đang dẫn dắt**, size tối thiểu, ưu tiên
  ITM (delta cao, ít phụ thuộc IV). Tape choppy giết CW nhanh hơn giết cổ phiếu.
- 🔴 **KHÔNG THUẬN** (Stage 4) → **CẤM chơi CW.** Đòn bẩy ngược trong thị trường xuống =
  cháy tài khoản. Đứng ngoài tuyệt đối, không có ngoại lệ "bắt đáy bằng CW".

Lấy đèn tổng từ `/vi-mo` và breadth từ `/radar-luot-song` nếu vừa chạy.

## Bước 0.5 — Chọn CƠ SỞ ứng viên (nếu người dùng không chỉ định)
CW chỉ phát hành trên **rổ VN30 thanh khoản cao** (FPT, HPG, MWG, MBB, STB, VPB, ACB, SSI,
VNM, VIC, VHM, TCB, VRE, MSN, POW, HDB...). Chọn **2–3 cơ sở** vừa **Stage 2 khỏe** vừa có
**catalyst trong 2–6 tuần** (KQKD, sự kiện ngành). Ưu tiên cơ sở có **biến động đủ lớn** để
CW chạy — cơ sở đi ngang lờ đờ thì CW chỉ chết vì theta. Nếu vừa chạy `/radar-luot-song`,
lấy các mã nhóm 🟢 A trong VN30 làm ứng viên.

## Bước 1 — Triển khai 3 agent SONG SONG (mỗi cơ sở ứng viên)

### Agent 1 — "Cơ sở" (HƯỚNG — người quyết định, phủ quyết)
> Phân tích cổ phiếu cơ sở [MÃ] theo Minervini + O'Neil (như /hoi-dong-luot-song rút gọn):
> Stage mấy, pivot, RS, và QUAN TRỌNG NHẤT cho CW: **kỳ vọng biên độ tăng bao nhiêu %
> trong bao nhiêu TUẦN** (CW cần cơ sở tăng ĐỦ và SỚM), có catalyst cụ thể trong 2–6 tuần
> không. Kết luận: cơ sở có đang trong nhịp tăng Stage 2 với catalyst gần + biên độ kỳ vọng
> đủ (tối thiểu ~+8–15% trong ~4–8 tuần) để bù theta không? Kết thúc: ★1–5, "ĐỦ ĐỘNG LỰC
> CHO CW / KHÔNG" + biên độ & thời gian kỳ vọng. KHÔNG đủ động lực gần = **phủ quyết**, không
> có CW nào cứu được (khác cổ phiếu: cổ phiếu chờ được, CW thì theta không chờ).

### Agent 2 — "Chọn CW" (CÔNG CỤ — Greeks & định giá)
> Với cơ sở [MÃ], liệt kê các mã CW đang niêm yết (bảng giá chứng quyền của CTCK: SSI, HSC,
> VND, MBS, KIS, VCSC...). Với mỗi CW lấy: mã CW, tổ chức phát hành, **giá thực hiện, tỷ lệ
> chuyển đổi, ngày đáo hạn, giá CW, bid/ask**. Dùng `stock-analysis/tools/cw_calc.py metrics`
> tính: trạng thái (ITM/ATM/OTM), điểm hòa vốn & % cơ sở cần tăng, đòn bẩy HIỆU DỤNG, IV ngụ
> ý, theta/ngày. **Chọn CW tốt nhất** theo thứ tự ưu tiên:
> 1. **Đáo hạn ≥ 2 tháng** (tránh vách theta; loại < 45 ngày trừ scalp cực ngắn).
> 2. **ATM đến hơi ITM** (delta ~0,5–0,75) — không OTM sâu (vé số), không quá sâu ITM (hết đòn bẩy).
> 3. **Đòn bẩy hiệu dụng ~3–6x** (đủ khuếch đại, chưa thành bom gamma).
> 4. **IV thấp nhất trong các CW so sánh được** — CW cùng cơ sở mà IV cao hơn = trả đắt,
>    dễ "IV crush". Đối chiếu IV với biến động lịch sử cơ sở.
> 5. **% cơ sở cần tăng để hòa vốn < biên độ kỳ vọng của Agent 1** (nếu không, toán không ra).
> 6. **Spread hẹp + thanh khoản** (nhà tạo lập niêm yết đều, khối lượng khá).
> Kết thúc: mã CW đề xuất + bảng chỉ số đầy đủ + 1 câu vì sao thắng các mã anh em.

### Agent 3 — "Kiểm-mìn-CW" (RỦI RO CHÍ MẠNG — phủ quyết)
> Nhiệm vụ HẸP: tìm mìn riêng của CW làm cháy tài khoản:
> 1. **Vách theta / ngày GD cuối**: đáo hạn quá gần (< 6 tuần) → theta dốc đứng, và có
>    "ngày giao dịch cuối cùng" (~2 ngày trước đáo hạn) sau đó không bán được.
> 2. **IV bị thổi phồng** trước sự kiện (KQKD) → sau tin, dù cơ sở tăng, **IV crush** vẫn làm
>    CW mất giá ("mua tin đồn bằng CW" là bẫy kinh điển).
> 3. **OTM quá sâu** (hòa vốn cần cơ sở tăng >15%) = vé số, xác suất về 0 cao.
> 4. **Thanh khoản mỏng / spread rộng** của nhà tạo lập → vào được không ra được.
> 5. **Cơ sở sắp có sự kiện gap ngược** (KQKD miss, tin xấu) — CW không có stop tự động,
>    gap là mất trắng phần lớn.
> 6. **Rủi ro tổ chức phát hành** niêm yết giá không sát lý thuyết (thiệt cho người mua).
> Kết thúc: **PASS** hoặc **DÍNH MÌN** (nêu rõ) — DÍNH MÌN = huỷ, dù cơ sở đẹp.

## Bước 2 — Trưởng nhóm tổng hợp → KẾ HOẠCH CW

```
# KẾ HOẠCH LƯỚT CW: [mã CW] trên [cơ sở] — [vài tuần]

## Ba vai
| Vai | Điểm/KL | Một câu |
|---|---|---|
| Cơ sở (hướng, QUYẾT ĐỊNH) | ★x | Stage x · biên độ kỳ vọng +y% trong z tuần · [ĐỦ/KHÔNG động lực] |
| Chọn CW (công cụ)         | — | Mã [CW] · đáo hạn · đòn bẩy hiệu dụng ~kx · IV n% · hòa vốn +m% |
| Kiểm-mìn-CW               | — | PASS / DÍNH MÌN: … |

## CỔNG VÀO (đủ CẢ BA, thiếu 1 = KHÔNG đánh)
1. Cơ sở Stage 2 + catalyst gần + biên độ kỳ vọng > % hòa vốn của CW?  ✅/❌
2. Có mã CW đạt chuẩn (đáo hạn ≥2 tháng, ATM–ITM, đòn bẩy 3–6x, IV không thổi)?  ✅/❌
3. Kiểm-mìn-CW PASS?  ✅/❌

## KẾT LUẬN: [ĐÁNH / CHỜ / BỎ]
- Mã CW: [code] — issuer, giá TH …, tỷ lệ …, đáo hạn … (còn … ngày)
- Kích hoạt mua CW: khi CƠ SỞ phá pivot … + volume (mua CW theo tín hiệu CƠ SỞ, không đuổi giá CW)
- **STOP đặt trên GIÁ CƠ SỞ** (…), KHÔNG trên giá CW (giá CW nhiễu/đòn bẩy) → cơ sở thủng stop = bán CW ngay
- Mục tiêu cơ sở … → CW lãi ~… (đòn bẩy hiệu dụng ×)
- Điểm hòa vốn CW: cơ sở … (cần +…%); đòn bẩy hiệu dụng …x; IV …%
- **TIME-STOP: thoát trước đáo hạn ≥10–15 phiên** dù chưa đạt target (tránh vách theta) — CW KHÔNG được "gồng tới đáo hạn"
- **Size CỰC NHỎ**: coi như tiền có thể MẤT TRẮNG. Tổng phí CW rủi ro ≤ ~0,5–1% danh mục/vị thế;
  CW là lát cắt CON của túi 🚀 Momentum, KHÔNG cộng thêm. **CẤM bình quân giá xuống** một CW đang lỗ.
- Quy tắc bán (chạm 1 → thoát): cơ sở thủng stop · đạt target · IV crush sau sự kiện · momentum cơ sở gãy · tới time-stop
```

## Quy tắc thép
- **Cơ sở phủ quyết**: cơ sở không Stage 2 / không catalyst gần / biên độ kỳ vọng < % hòa vốn
  → KHÔNG có CW, dù mã CW "rẻ" cỡ nào. Theta không chờ luận điểm chín.
- **Kiểm-mìn-CW phủ quyết**: DÍNH MÌN (đáo hạn gần, IV thổi, OTM sâu, thanh khoản mỏng) → bỏ.
- **Stop theo CƠ SỞ, không theo CW.** Đây là sai lầm phổ biến nhất: giá CW nhảy loạn vì đòn
  bẩy → đặt stop trên CW dễ bị "quét" oan. Kỷ luật: theo dõi cơ sở, cơ sở hỏng thì cắt CW.
- **CẤM ôm CW qua đáo hạn** hy vọng đảo chiều — OTM khi đáo hạn = 0 tuyệt đối. Time-stop là bắt buộc.
- **CẤM mua CW ngay trước KQKD với IV cao** để "đánh tin" — IV crush ăn hết phần cơ sở tăng.
- **Chỉ chơi khi VN-Index Stage 2.** Stage 4 → cấm tuyệt đối (không "bắt đáy bằng CW").
- Size cực nhỏ, chấp nhận mất trắng, không bình quân giá xuống, không dồn nhiều CW cùng cơ sở.
- Dữ liệu CW sống (mã, IV, bid/ask, đáo hạn) phải lấy từ **bảng giá chứng quyền của CTCK**;
  WebSearch thường trễ/thiếu → gắn nhãn C, nói rõ cần kiểm chứng trên bảng giá trước khi vào lệnh.
- Lưu vết vào `stock-analysis/reports/chungquyen.md` (kèm ngày) để đối chiếu lần sau.
- Kết thúc bằng: "⚠️ Nghiên cứu học tập, không phải khuyến nghị đầu tư. CW là công cụ đòn bẩy
  rủi ro rất cao, có thể mất toàn bộ vốn."
