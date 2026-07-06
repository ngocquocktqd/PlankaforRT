---
name: hoi-dong-luot-song
description: Hội đồng lướt sóng 3 agent nhẹ cho chân trời 3–6 tháng — chế độ TRADER MOMENTUM có bộ lọc cơ bản (kiểu CANSLIM/Minervini). ĐẢO VAI so với hội đồng giá trị: kỹ thuật (Minervini) QUYẾT ĐỊNH, cơ bản (O'Neil) chỉ làm bộ lọc + tìm catalyst, Kiểm-tra-mìn dò rủi ro chí mạng. Đầu ra là KẾ HOẠCH GIAO DỊCH (pivot/stop/target/time-stop), không phải luận điểm đầu tư. Dùng khi muốn đánh sóng ngắn-trung hạn, ví dụ "/hoi-dong-luot-song FPT".
---

# Hội đồng lướt sóng — 3 agent, chân trời 3–6 tháng

Cổ phiếu cần đánh giá: **$ARGUMENTS**

Bạn là **Trưởng nhóm giao dịch**. Đây KHÔNG phải hội đồng đầu tư giá trị. Đây là chế độ
**TRADER MOMENTUM có bộ lọc cơ bản**: kỹ thuật quyết định vào/ra, cơ bản chỉ để (1) loại
cổ phiếu rác và (2) tìm chất xúc tác trong cửa sổ 3–6 tháng. Vốn cho vị thế này thuộc
túi 🚀 Momentum trong `/phan-bo-von`, chịu stop cứng 7–8%, KHÔNG phải khoản nắm giữ dài hạn.

> ⚠️ Đây là trò chơi khác hẳn `/hoi-dong-dau-tu`. Ở đó cơ bản quyết định, kỹ thuật phụ,
> giữ nhiều năm. Ở đây kỹ thuật quyết định, cơ bản là bộ lọc, giữ 3–6 tháng, bán theo
> giá + thời gian. Cấm trộn: một cổ phiếu đánh theo skill này thì áp luật của skill này.

## Bước 1 — Triển khai 3 agent SONG SONG

Dùng Agent tool, khởi chạy **cùng lúc** 3 subagent. Mỗi agent tự tìm dữ liệu độc lập.

### Agent 1 — "Minervini" (KỸ THUẬT — người quyết định)
> Phân tích kỹ thuật [CÔNG TY] theo Minervini/SEPA (xem skill phan-tich-ky-thuat).
> Chấm Trend Template 8 tiêu chí kèm số liệu; xác định Stage 1–4; tìm nền giá/VCP và
> điểm PIVOT; đánh giá RS so VN-Index (3/6/12 tháng) và so với nhóm ngành; bối cảnh
> VN-Index (Stage mấy). Với chân trời 3–6 tháng, ưu tiên cổ phiếu Stage 2 vừa hoàn tất
> nền chặt và chuẩn bị/ vừa phá pivot với volume. Kết thúc bằng: ★1–5 (chất lượng setup),
> Trend Template x/8, Stage, PIVOT + STOP 7–8%, và các mốc kháng cự làm mục tiêu chốt lời.

### Agent 2 — "O'Neil" (ĐỘNG LỰC CƠ BẢN + CATALYST — bộ lọc)
> Phân tích [CÔNG TY] kiểu CANSLIM/O'Neil, KHÔNG định giá DCF. Trả lời:
> (a) **Tăng tốc lợi nhuận & doanh thu**: EPS/LNST và doanh thu 3–4 quý gần nhất tăng
> trưởng YoY bao nhiêu? Quý mới nhất có TĂNG TỐC (nhanh hơn quý trước) hay giảm tốc? Ưu
> tiên tăng tốc; giảm tốc kéo dài là cờ vàng.
> (b) **Catalyst trong 3–6 tháng**: có sự kiện cụ thể sắp diễn ra không (KQKD quý tới kỳ
> vọng mạnh, sự kiện ngành, nâng hạng, dòng vốn, sản phẩm/dự án mới đi vào vận hành)?
> (c) **Guard định giá NHẸ**: P/E hoặc PEG hiện tại so trung vị lịch sử của chính nó —
> có đang ở vùng bong bóng (đắt bất thường) không? Chỉ để tránh mua đỉnh, KHÔNG phải định giá.
> (d) Có phải cổ phiếu dẫn dắt ngành, hay chỉ ăn theo? Vị thế thị phần/tăng trưởng ngành.
> Kết thúc bằng: ★1–5 (động lực cơ bản), "CÓ/KHÔNG catalyst 3–6 tháng" + mô tả catalyst,
> và cảnh báo nếu định giá đã bong bóng.

### Agent 3 — "Kiểm-tra-mìn" (RỦI RO CHÍ MẠNG — chỉ dò mìn)
> Nhiệm vụ HẸP: chỉ tìm MÌN có thể làm cháy tài khoản trong 3–6 tháng, KHÔNG phân tích
> sâu kiểu Munger. Kiểm 6 loại mìn:
> 1. **Thanh khoản**: giá trị khớp lệnh bình quân/phiên có đủ để vào/ra vị thế không (mã
>    thanh khoản quá thấp = bẫy, không vào được và không thoát được khi cần)?
> 2. **Nguy cơ huỷ niêm yết/kiểm soát/cảnh báo** (lỗ luỹ kế, ý kiến kiểm toán ngoại trừ).
> 3. **Cầm cố cổ phiếu** của lãnh đạo/cổ đông lớn ở mức nguy hiểm (rủi ro giải chấp chéo).
> 4. **Pha loãng sốc sắp tới**: phát hành lớn, chuyển đổi trái phiếu, ESOP khủng sắp về.
> 5. **Cổ đông lớn/nội bộ đang XẢ mạnh**, hoặc khối ngoại bán ròng cấu trúc.
> 6. **Bên liên quan sắp nổ / kiện tụng / án phạt / KQKD sắp ra có rủi ro sập bẫy**.
> Tìm tin tiêu cực gần đây. Kết thúc bằng: **PASS** (không mìn chí mạng) hoặc **DÍNH MÌN**
> (nêu rõ mìn nào) — DÍNH MÌN là quyền phủ quyết, huỷ lệnh bất kể setup đẹp.

## Bước 2 — Trưởng nhóm tổng hợp → KẾ HOẠCH GIAO DỊCH

Dùng công cụ khi cần tính R:R, position size: `stock-analysis/tools/fin_calc.py`.

```
# KẾ HOẠCH LƯỚT SÓNG: [CÔNG TY] — chân trời 3–6 tháng

## Ba agent
| Agent | Điểm | Kết luận 1 câu |
|---|---|---|
| Minervini (kỹ thuật, QUYẾT ĐỊNH) | ★x | Trend Template x/8 · Stage x · [SETUP/CHỜ/TRÁNH] |
| O'Neil (động lực + catalyst)     | ★x | Tăng tốc? · Catalyst 3–6 tháng: CÓ/KHÔNG · Định giá: ổn/bong bóng |
| Kiểm-tra-mìn (rủi ro)            | — | PASS / DÍNH MÌN: … |

## CỔNG VÀO LỆNH (phải qua CẢ BA, thiếu 1 = KHÔNG trade)
1. Kỹ thuật: Stage 2 + có pivot rõ (Minervini không TRÁNH)?  ✅/❌
2. Cơ bản: có catalyst 3–6 tháng + không giảm tốc + không bong bóng?  ✅/❌
3. Rủi ro: Kiểm-tra-mìn PASS?  ✅/❌

## KẾT LUẬN: [VÀO LỆNH / CHỜ SETUP / BỎ QUA]
- Điểm vào (pivot): … — mua khi phá pivot + volume ≥150% TB50 phiên
- Stop loss: … (7–8% dưới pivot, CỨNG — không dời xuống)
- Mục tiêu: T1 … / T2 … (theo kháng cự hoặc bội R)
- **R:R** = (T1 − pivot) / (pivot − stop) = … → cần **≥ 2:1** mới đáng vào
- Time-stop: nếu sau 3–4 tuần không chạy khỏi pivot → cắt; hết 6 tháng chưa đạt target → đóng
- Position size: rủi ro khi dính stop = size × 7–8% ≤ 1–1,5% danh mục → size tối đa = …%
  (vốn từ túi 🚀 Momentum của /phan-bo-von, KHÔNG từ túi Giá trị)
- Trailing stop: sau +1R dời stop lên hoà vốn; sau đó bám MA10/MA20 hoặc đáy nền mới
- QUY TẮC BÁN (chạm 1 trong → thoát ngay, không lăn tăn):
  dính stop · đạt target · momentum gãy (mất MA50 + volume lớn) · KQKD miss/catalyst hỏng · hết time-stop
```

## Quy tắc thép
- **Kỹ thuật phủ quyết**: Minervini TRÁNH (không Stage 2/không pivot) → KHÔNG trade, dù cơ bản đẹp cỡ nào. Ở skill này đồ thị là vua.
- **Kiểm-tra-mìn phủ quyết**: DÍNH MÌN → bỏ, dù setup đẹp.
- **O'Neil không đủ để vào một mình**: cơ bản đẹp + kỹ thuật xấu = CHỜ, không phải VÀO.
- **CẤM thesis drift**: lệnh lướt sóng dính stop thì CẮT, tuyệt đối không "hoá đầu tư dài hạn" để hợp lý hoá việc ôm lỗ. Đây là sai lầm chết người nhất.
- Bán theo **GIÁ và THỜI GIAN**, không theo luận điểm 10 năm. Skill này KHÔNG có lăng kính Lý Lục.
- Chỉ chơi khi **VN-Index thuận** (Stage 2). Thị trường chung Stage 4 → đứng ngoài, giữ tiền mặt, dù cổ phiếu riêng lẻ đẹp.
- Nếu người dùng đã có vị thế (nêu giá mua): chuyển sang chế độ quản trị lệnh — đánh giá còn giữ hay thoát theo đúng bộ quy tắc bán ở trên.
