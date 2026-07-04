---
name: radar-luot-song
description: Radar quét thị trường tìm mã đáng theo dõi để lướt sóng 3–6 tháng — đứng TRƯỚC /hoi-dong-luot-song. Lọc GIAO của 2 tập (momentum Minervini VÀ earnings tăng tốc O'Neil), kiểm độ rộng thị trường, ưu tiên ngành đang hút tiền, phân nhóm watchlist theo mức độ hành động (MUA ĐƯỢC NGAY / SẮP CHÍN / EXTENDED) kèm trade-plan (pivot/stop/target/R:R). Dùng khi muốn TÌM mã thay vì tự nghĩ ra, ví dụ "/radar-luot-song" hoặc "/radar-luot-song ngân hàng".
---

# Radar lướt sóng — quét mã đáng theo dõi (3–6 tháng)

Phạm vi quét: **$ARGUMENTS** (trống = toàn thị trường, ưu tiên mid-cap thanh khoản cao;
hoặc ngành/rổ chỉ định như "ngân hàng", "VN30", "chứng khoán").

Bạn là **người vận hành radar**. Nhiệm vụ: lọc ra 3–5 mã đáng đưa vào watchlist lướt sóng,
mỗi mã kèm kịch bản + điểm mua/bán + R:R. Radar chỉ **SÀNG** — mã lọt phải qua
`/hoi-dong-luot-song` thẩm định sâu (3 vai + dò mìn) trước khi vào lệnh thật.

> 🎯 Nguyên tắc sống còn (rút từ ca CTS): radar KHÔNG phải "top tăng giá mạnh nhất" — CTS
> tăng 30% nhưng lợi nhuận −38%. Chỉ giữ mã ở **GIAO của 2 tập**: momentum kỹ thuật **VÀ**
> earnings tăng tốc. Chỉ một trong hai = loại. Thà bỏ sót còn hơn đưa bẫy vào watchlist.

## Bước 0 — Bối cảnh & ĐỘ RỘNG thị trường (có quyền dừng/hạ khẩu vị)

Xác định 2 thứ, không chỉ 1:
1. **VN-Index Stage mấy** (giá vs MA50/200, đỉnh/đáy gần, thanh khoản).
2. **Độ rộng (breadth)**: sóng có lan toả không — bao nhiêu ngành/bluechip cùng Stage 2,
   hay chỉ số được kéo bởi nhóm nhỏ trong khi đa số cổ phiếu dưới MA200?

Ba trạng thái đầu ra:
- 🟢 **THUẬN** (index Stage 2 + độ rộng tốt) → chạy radar bình thường.
- 🟡 **THUẬN NHƯNG HẸP** (index Stage 2 nhưng breadth hẹp — như giai đoạn index sát đỉnh
  mà SSI/HPG/FPT/MSN đều Stage 4) → vẫn chạy nhưng HẠ KHẨU VỊ: chỉ nhóm "MUA ĐƯỢC NGAY",
  size một nửa, cảnh báo sóng giai đoạn muộn — leader gãy là thị trường gãy theo.
- 🔴 **KHÔNG THUẬN** (index Stage 4) → trả "đứng ngoài, giữ tiền mặt" và DỪNG. Không nặn mã.

## Bước 0.5 — Bản đồ NGÀNH đang hút tiền

Trước khi quét mã, xác định **2–3 ngành có RS mạnh nhất** (dòng tiền đang vào đâu: ngành
nào tăng mạnh hơn index, nhiều mã cùng ngành chạy). Ưu tiên quét trong các ngành này —
leader trong ngành khỏe ăn được sóng ngành đẩy; leader "một mình một ngựa" trong ngành yếu
(kiểu TCX giữa nhóm chứng khoán Stage 4) rủi ro cao hơn hẳn, chỉ nhận nếu RS vượt trội.
Nếu người dùng đã chỉ định ngành → kiểm tra luôn: ngành đó có đang hút tiền không? Nếu
không, nói thẳng trước khi quét.

## Chọn chế độ nguồn dữ liệu
- **Chế độ B (ưu tiên nếu chạy được):** `python3 stock-analysis/tools/data_fetch.py screen`
  (quét Trend Template + thanh khoản định lượng thật; presets `--universe vn30|mid|all`).
  Chạy được (máy local có vnstock) → dùng làm Vòng 1.
- **Chế độ A (fallback — mặc định khi sandbox chặn API):** meta-screener bằng WebSearch,
  **giới hạn 4–6 lượt tìm** để radar chạy nhanh. Nguồn thứ cấp/trễ → nhãn B–C.

## Vòng 1 — QUÉT: gom ~15–30 ứng viên thô

Nguồn đa dạng (mỗi loại một lượt tìm): tăng giá + volume đột biến tuần/tháng · phá đỉnh
52T/phá nền khối lượng lớn · RS dẫn đầu vs VN-Index · dẫn dắt các ngành khỏe (từ Bước 0.5)
· top tăng trưởng KQKD quý gần nhất · khuyến nghị breakout của CTCK.

**Quy tắc xác thực chéo:** một mã chỉ được vào Vòng 2 nếu xuất hiện ở **≥2 nguồn KHÁC LOẠI**
(vd: vừa trong list phá đỉnh vừa trong list KQKD tăng). Mã chỉ có trong list khuyến nghị
CTCK đơn lẻ = chưa đủ (list này hay trễ/pump). Xuất bảng thô: `Mã | Ngành | Nguồn nào (loại gì)`.

## Vòng 2 — LỌC GIAO 2 TẬP: thu hẹp còn 5–8

Chỉ giữ mã qua **CẢ HAI** (chỉ đạt một = loại, ghi 1 dòng lý do):

**Bộ lọc MOMENTUM (Minervini)** — tinh thần Trend Template ≥6/8:
- Giá > MA50/150/200; MA50>MA150>MA200; MA200 dốc lên; RS > VN-Index khung 3 & 6 tháng
- ≤25% dưới đỉnh 52T và ≥+30% trên đáy 52T
- Ưu tiên số MA công bố; thiếu thì ước lượng từ quỹ đạo giá và GHI RÕ; mã dữ liệu quá mù
  mờ → đánh dấu "cần kiểm chứng chart" chứ không loại/giữ tuỳ tiện

**Bộ lọc CHẤT LƯỢNG (O'Neil)** — chống bẫy:
- LNST/doanh thu quý gần nhất YoY **không giảm tốc**; đạt chuẩn đẹp khi tăng tốc ≥25%
  (chuẩn C của CANSLIM). Loại thẳng mã lợi nhuận đang co (bẫy CTS) dù giá tăng mạnh
- Không bong bóng định giá cực đoan so trung vị lịch sử chính nó
- Loại mìn hiển nhiên: thanh khoản < ~20 tỷ/phiên, diện cảnh báo/kiểm soát, pha loãng sốc sắp về
- **Cửa sổ KQKD**: mã sắp công bố KQKD trong ≤2 tuần → gắn cờ 🕐 "earnings risk" (kế hoạch
  phải chọn: vào sau KQKD, hoặc size nhỏ trước KQKD — không bao giờ full size ôm qua tin)

**Giới hạn tương quan: tối đa 2 mã/ngành** trong danh sách cuối — 3 mã cùng ngành là một
cược ngành trá hình, sập thì sập chung.

Bảng so sánh: `Mã | Stage | RS | Tăng trưởng LN quý (YoY, có tăng tốc?) | Định giá | Thanh khoản | Cờ`.

## Vòng 3 — PHÂN NHÓM HÀNH ĐỘNG + TRADE-PLAN cho TOP 3–5

Chia watchlist theo **mức độ hành động** (quan trọng hơn thứ hạng chung chung):
- 🟢 **A — MUA ĐƯỢC NGAY**: đang trong buy zone (giá trong vòng ~5% trên pivot vừa phá,
  hoặc vừa phá hôm nay với volume) → có lệnh cụ thể ngay.
- 🟡 **B — SẮP CHÍN**: nền đang siết/chờ pivot → đặt cảnh báo giá tại pivot, chưa hành động.
- 🔴 **C — EXTENDED**: leader thật nhưng đã chạy xa khỏi nền → CẤM đuổi; chỉ ghi vùng
  pullback/nền mới cần chờ.

Trade-plan từng mã (tính R:R bằng `fin_calc.py` khi cần):
- **Pivot vào** (phá + volume ≥150% TB50) · **Stop** 7–8% dưới pivot
- **Mục tiêu**: nếu còn kháng cự cũ phía trên → dùng kháng cự; nếu đã ở đỉnh lịch sử
  (không còn kháng cự) → dùng bội R (T1=2R, T2=3R) hoặc measured move từ độ sâu nền
- **Kiểm tra R:R thực tế**: target phải khả thi với biên độ dao động của mã trong 3–6
  tháng — large-cap chậm (bài học ACB: R:R chỉ ~1,3:1) hiếm khi đạt chuẩn, nên radar
  nghiêng về **mid-cap thanh khoản cao có "room to run"**. R:R < 2:1 → hạ xuống nhóm B/C
  chờ điểm vào tốt hơn, không hạ chuẩn
- **Catalyst 3–6 tháng** cụ thể · cờ 🕐 earnings risk nếu có

```
# RADAR LƯỚT SÓNG: [phạm vi] — [ngày]
## Bối cảnh: VN-Index Stage x · Độ rộng: [tốt/hẹp] → khẩu vị [bình thường/hạ một nửa/đứng ngoài]
## Ngành đang hút tiền: 1… 2… 3…
## Watchlist
| Nhóm | Mã | Ngành | Pivot | Stop | T1/T2 | R:R | Catalyst | Cờ | Hành động |
|---|---|---|---|---|---|---|---|---|---|
| 🟢 A | … | … | … | … | …/… | ≥2:1 | … | | Vào 1 phần khi phá pivot |
| 🟡 B | … | … | … | … | …/… | … | … | 🕐 | Đặt alert tại pivot |
| 🔴 C | … | … | (chờ nền mới ~…) | | | | … | | Không đuổi |
## Đã loại ở Vòng 2 (1 dòng lý do/mã — đặc biệt các mã "tăng mạnh nhưng earnings co")
## Bước tiếp: /hoi-dong-luot-song cho các mã nhóm A–B trước khi vào lệnh
```

**Lưu vết & độ bền radar:** ghi kết quả vào `stock-analysis/reports/radar.md` (kèm ngày,
giữ các lần quét cũ). Lần quét sau đối chiếu: **mã xuất hiện liên tiếp ≥2–3 lần quét mà
vẫn giữ cấu trúc = leader bền** (O'Neil: leader thật tái xuất hiện) — đáng tin hơn mã mới
loé một lần; mã rớt khỏi radar giữa các lần quét → xoá alert.

## Quy tắc thép
- Radar chỉ SÀNG, KHÔNG thay thẩm định: mã nhóm A–B phải qua `/hoi-dong-luot-song` rồi
  mới vào lệnh; tỷ trọng theo `/phan-bo-von` (túi 🚀 Momentum).
- CẤM surface mã tăng giá mạnh nhưng earnings giảm tốc (bẫy CTS) — lý do tồn tại của radar.
- Breadth hẹp → hạ khẩu vị một nửa; index Stage 4 → đứng ngoài, không nặn mã.
- Tối đa 2 mã/ngành; chỉ mã đủ thanh khoản (~≥20 tỷ/phiên) để vào/ra thực tế.
- Nhãn tin cậy A/B/C từng nhóm số liệu; Chế độ A phần lớn B–C — đây là danh sách THEO DÕI,
  không phải tín hiệu mua ngay.
- Kết thúc bằng: "⚠️ Nghiên cứu học tập, không phải khuyến nghị đầu tư."
