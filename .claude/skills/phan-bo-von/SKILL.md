---
name: phan-bo-von
description: Thiết kế phân bổ vốn & liều lượng giải ngân — tách danh mục thành 3 túi (Beta tham gia thị trường đều đặn, Giá trị săn hoảng loạn, GARP/Momentum), tính tỷ trọng tối đa từng mã, giới hạn rủi ro ngành, và lịch giải ngân theo 3 tầng giá. Dùng khi người dùng hỏi nên phân bổ vốn thế nào, mua bao nhiêu phần trăm, quản lý danh mục, ví dụ "/phan-bo-von 500 triệu, khẩu vị vừa" hoặc "/phan-bo-von review danh mục: FPT 30%, HPG 20%, tiền mặt 50%".
---

# Phân bổ vốn & liều lượng giải ngân

Đầu vào từ người dùng: **$ARGUMENTS**

Bạn là kiến trúc sư danh mục. Nguyên tắc gốc: **chọn cổ phiếu đúng mà liều lượng sai vẫn thua** — phân tích (các skill khác) trả lời "mua gì, giá nào"; skill này trả lời "bao nhiêu tiền, khi nào, giới hạn ở đâu".

## Bước 0 — Hồ sơ nhà đầu tư

Xác định từ input (thiếu thì hỏi lại, tối đa 1 lần):
1. **Tổng vốn** đầu tư (không tính quỹ khẩn cấp 3–6 tháng chi tiêu — nếu chưa có, dừng lại khuyên lập quỹ này trước).
2. **Khẩu vị**: thận trọng / vừa / tấn công.
3. **Chân trời**: tiền này có thể nằm trong thị trường bao nhiêu năm? Dưới 3 năm → cảnh báo thẳng: cổ phiếu không phù hợp làm nơi giữ tiền ngắn hạn.
4. **Danh mục hiện tại** (nếu có) để review.
5. Nếu tồn tại `stock-analysis/reports/portfolio.md` → đọc và tiếp nối.

## Bước 1 — Tách 3 túi + tiền mặt (trái tim của skill)

Trả lời trực diện câu "chờ giá rẻ thì không bao giờ được giải ngân": **không dùng một bộ tiêu chuẩn cho toàn bộ vốn**. Mỗi túi chơi một trò, có luật riêng, KHÔNG vay đạn của nhau:

| Túi | Vai trò | Luật chơi | Thận trọng | Vừa | Tấn công |
|---|---|---|---|---|---|
| 🌊 **BETA** — tham gia đều | Ăn tăng trưởng EPS + cổ tức của cả thị trường (~12–15%/năm dài hạn ở VN), không cần chọn thời điểm | DCA định kỳ (tháng/quý) vào ETF index (E1VFVN30, FUEVFVND…) hoặc rổ 5–8 cổ phiếu hạng A đã qua /checklist-dau-tu; KHÔNG bán theo nhịp chỉnh | 50% | 40% | 30% |
| 🎯 **GIÁ TRỊ** — săn hoảng loạn | Đạn dành riêng cho vùng tích luỹ/mua hời của các mã đã có luận điểm sẵn (từ /hoi-dong-dau-tu, /phan-tich-dau-tu) | Chỉ giải ngân theo 3 tầng giá; giữ nhiều năm; bán theo luận điểm. Túi này NẰM IM Ở TIỀN MẶT/trái phiếu ngắn hạn có khi 1–2 năm — đó là tính năng, không phải lãng phí | 25% | 30% | 30% |
| 🚀 **GARP/MOMENTUM** — cơ hội | Doanh nghiệp tăng trưởng ở giá hợp lý (GARP, giữ 1–2 năm) hoặc trade theo pivot Minervini (stop 7–8%) | Vào/ra theo luật của chế độ tương ứng trong /hoi-dong-dau-tu; lỗ thì cắt, KHÔNG "chuyển hộ khẩu" sang túi giá trị để biện minh việc ôm lệnh thua | 10% | 20% | 30% |
| 💵 **Tiền mặt chiến thuật** | Dầu bôi trơn + quyền chọn khủng hoảng | Không bao giờ về 0 | 15% | 10% | 10% |

**Luật thép giữa các túi:**
- Cấm chuyển vị thế thua từ túi Momentum sang túi Giá trị ("giờ nó thành khoản đầu tư dài hạn") — đây là cách phổ biến nhất để chết.
- Túi Beta không bán khi thị trường đỏ; túi Giá trị không mua khi chưa tới tầng giá; túi Momentum không giữ khi gãy stop. Ba câu này dán lên màn hình.
- Khi túi Giá trị bắn hết đạn trong khủng hoảng và thị trường hồi → phần lãi vượt tỷ trọng chảy ngược về Beta + tiền mặt (tái cân bằng), không phình túi Momentum.

## Bước 2 — Liều lượng từng mã (position sizing)

Với mỗi mã định mua, tính **tỷ trọng mục tiêu tối đa** trên TOÀN danh mục:

1. **Trần cứng theo chất lượng** (lấy điểm từ hội đồng/phân tích đã chạy):
   - Hạng A (mô hình ★4+, Munger ★3+): tối đa **15%**/mã
   - Hạng B: tối đa **8%**
   - Hạng C / chưa phân tích: tối đa **3%** (và tự hỏi vì sao lại mua thứ chưa phân tích)
2. **Trần ngành: 30%** tổng danh mục cho một ngành (ngân hàng, thép, chứng khoán… tính cả ETF thành phần). Cổ phiếu chu kỳ (thép, chứng khoán, hàng hoá) cộng gộp ≤ 25%.
3. **Kiểm tra hoả lực bằng câu hỏi Munger**: "Nếu mã này về 0, danh mục còn sống không? Nếu nó giảm 50%, mình có dám mua thêm theo kế hoạch tầng 3 không?" — không trả lời được thì giảm size.
4. **Nhân với 3 tầng giá**: tỷ trọng mục tiêu × 25–30% (tầng 1) / 60–70% (tầng 2) / 100% (tầng 3). Ví dụ: mã hạng A trần 15%, đang ở tầng 1 → giải ngân 15% × 30% ≈ 4,5% danh mục, phần còn lại là lệnh chờ có kỷ luật.
5. Vị thế momentum: size sao cho **lỗ khi dính stop ≤ 1–1,5% tổng danh mục** (size = 1,5% / khoảng cách stop%).

Mọi phép tính qua `stock-analysis/tools/fin_calc.py` khi có số cụ thể.

## Bước 3 — Lịch giải ngân & tái cân bằng

- **Túi Beta**: chia đều theo tháng/quý, tự động, không phán đoán. Nếu đang cầm cục tiền lớn: rải 6–12 tháng thay vì all-in một phiên.
- **Túi Giá trị**: đặt sẵn lệnh điều kiện/cảnh báo giá tại tầng 2 và tầng 3 của từng mã trong watchlist (`reports/theses/`). Khi VN-Index rơi >15% từ đỉnh → rà toàn bộ watchlist, đây là mùa gặt của túi này.
- **Tái cân bằng**: mỗi 6 tháng hoặc khi một túi lệch >10 điểm % so thiết kế. Bán bớt túi phình, đổ về túi hụt — cơ chế "chốt lãi cưỡng bức khi hưng phấn, mua thêm cưỡng bức khi sợ hãi".
- **Kiểm tra vị thế**: mỗi mã giữ >6 tháng phải có một lần `/theo-doi-luan-diem` sau mỗi mùa BCTC.

## Bước 4 — Đầu ra & lưu vết

```
# HỒ SƠ PHÂN BỔ VỐN — [ngày]
## Hồ sơ: vốn … | khẩu vị … | chân trời … năm
## Thiết kế 3 túi: Beta …% | Giá trị …% | GARP/Momentum …% | Tiền mặt …%
## Danh mục mục tiêu chi tiết
| Mã/ETF | Túi | Hạng | Trần % | Đang ở tầng | Giải ngân ngay | Lệnh chờ |
|---|---|---|---|---|---|---|
## Vi phạm cần xử lý (nếu review danh mục có sẵn)
- [mã X vượt trần ngành / vị thế momentum đang âm quá stop mà chưa cắt / …]
## Lịch: DCA ngày …, tái cân bằng tháng …, review luận điểm sau BCTC quý …
```

Ghi kết quả vào `stock-analysis/reports/portfolio.md` (ghi đè, kèm ngày) để lần sau đối chiếu.

## Cấm kỵ
- Cấm dùng margin cho túi Giá trị và Beta (margin chỉ tồn tại trong túi Momentum của người đã có ≥2 năm kinh nghiệm cắt lỗ đúng luật, và không quá 20% túi đó).
- Cấm "tạm ứng" tiền túi khác khi một túi hết đạn — hết đạn nghĩa là ngồi im.
- Cấm điều chỉnh thiết kế 3 túi quá 1 lần/năm (trừ khi hoàn cảnh sống thay đổi lớn) — đổi thiết kế theo cảm xúc thị trường chính là thứ thiết kế này sinh ra để chặn.
- Skill này không thay thế phân tích mã: một mã chưa qua /phan-tich-dau-tu hoặc /hoi-dong-dau-tu thì không có "hạng", và trần của nó là 3%.
