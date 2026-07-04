# 📈 Stock Analysis Toolkit — "AI Berkshire" phiên bản Việt

Bộ công cụ nghiên cứu đầu tư giá trị chạy trên **Claude Code**, lấy cảm hứng từ
[xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire): kết hợp phương pháp luận
của 4 bậc thầy đầu tư với phân tích đối kháng đa-agent và công cụ tính toán tài chính
chính xác tuyệt đối (không dùng float, chỉ dùng `Decimal`).

Hỗ trợ **cổ phiếu Việt Nam** (HOSE/HNX/UPCoM qua `vnstock`) và **cổ phiếu quốc tế**
(qua `yfinance`).

## 🧠 Triết lý: 4 lăng kính xung đột

Mỗi phân tích được soi qua 4 góc nhìn **cố tình mâu thuẫn nhau** — "các thiên thần
xung đột bắt được lỗi" — để tránh tư duy bầy đàn:

| Lăng kính | Bậc thầy | Câu hỏi cốt lõi |
|---|---|---|
| 🏭 Mô hình kinh doanh | Đoàn Vĩnh Bình (段永平) | Doanh nghiệp này có tạo ra giá trị thật không? Lợi thế có bền không? |
| 💰 Định giá & con hào | Warren Buffett | Dòng tiền chủ sở hữu là bao nhiêu? Biên an toàn ở đâu? |
| 🔄 Tư duy ngược & thiên kiến | Charlie Munger | Kịch bản nào khiến khoản đầu tư này chết? Tôi đang tự lừa mình ở điểm nào? |
| 🌊 Xu thế văn minh | Lý Lục (李录) | 10 năm nữa công ty này còn đứng đúng dòng chảy lớn không? |

## 🛠️ Cài đặt

```bash
# 1. Cài Claude Code (nếu chưa có)
npm install -g @anthropic-ai/claude-code

# 2. Cài skill vào Claude Code
./stock-analysis/scripts/install.sh

# 3. (Tuỳ chọn) Cài thư viện dữ liệu
pip install -r stock-analysis/requirements.txt
```

## 🚀 Sử dụng

Mở Claude Code và gõ trực tiếp:

```
/phan-tich-dau-tu FPT              # Phân tích sâu một công ty (4 lăng kính)
/hoi-dong-dau-tu HPG               # 5 agent đối kháng — ĐẦU TƯ giá trị (giữ nhiều năm)
/radar-luot-song                   # Radar QUÉT thị trường tìm mã lướt sóng (giao momentum × earnings)
/hoi-dong-luot-song FPT            # 3 agent nhẹ — LƯỚT SÓNG momentum (giữ 3–6 tháng)
/phan-tich-ky-thuat FPT            # Kỹ thuật Minervini/SEPA — trả lời THỜI ĐIỂM mua
/doc-bao-cao-tai-chinh VNM         # Đọc sâu BCTC / báo cáo thường niên
/loc-co-phieu ngành bán lẻ         # Phễu lọc ngành 30 → 10 → 3
/checklist-dau-tu MWG, FPT, PNJ    # Checklist 6 cổng kiểu Buffett
/theo-doi-luan-diem VCB            # Theo dõi luận điểm sau khi đã mua
/phan-bo-von 500 triệu, khẩu vị vừa # Thiết kế 3 túi vốn + liều lượng giải ngân
```

**Ba chế độ, không trộn lẫn:** framework phân biệt rõ *Đầu tư giá trị* (mua dưới nội tại,
giữ nhiều năm), *GARP* (tăng trưởng ở giá hợp lý, giữ 1–2 năm) và *Trader momentum*
(theo pivot Minervini, stop 7–8%). Giải ngân theo **3 tầng giá** (fair value 25–30% →
tích luỹ 60–70% → mua hời 100%) thay vì quyết định nhị phân mua/không mua.

**Hai luồng làm việc:**
- 🏛️ *Đầu tư giá trị*: `/loc-co-phieu` (tìm ngành) → `/hoi-dong-dau-tu` (thẩm định 5 lăng kính)
  → `/phan-bo-von` (giải ngân 3 tầng) → `/theo-doi-luan-diem` (giám sát nhiều năm).
- 🚀 *Lướt sóng momentum*: `/radar-luot-song` (quét tìm mã) → `/hoi-dong-luot-song` (thẩm định
  3 vai + dò mìn) → `/phan-bo-von` túi Momentum (position size, stop 7–8%, giữ 3–6 tháng).

## 📁 Cấu trúc

```
stock-analysis/
├── skills/                    # Các skill Claude Code (slash command)
│   ├── phan-tich-dau-tu/      #   Phân tích sâu 1 công ty qua 4 lăng kính
│   ├── hoi-dong-dau-tu/       #   5 agent — ĐẦU TƯ giá trị (2 khối + ma trận)
│   ├── radar-luot-song/       #   Radar quét mã lướt sóng (giao momentum × earnings tăng tốc)
│   ├── hoi-dong-luot-song/    #   3 agent nhẹ — LƯỚT SÓNG momentum 3–6 tháng (kế hoạch giao dịch)
│   ├── phan-tich-ky-thuat/    #   Minervini/SEPA: Trend Template, Stage, VCP, pivot
│   ├── doc-bao-cao-tai-chinh/ #   Đọc sâu BCTC, soi chất lượng lợi nhuận
│   ├── loc-co-phieu/          #   Phễu lọc ngành 30 → 10 → 3
│   ├── checklist-dau-tu/      #   6 cổng kiểm tra kiểu Buffett
│   ├── theo-doi-luan-diem/    #   Giám sát luận điểm đầu tư sau giải ngân
│   └── phan-bo-von/           #   3 túi vốn (Beta/Giá trị/GARP-Momentum) + position sizing
├── tools/                     # Công cụ Python (độ chính xác Decimal)
│   ├── fin_calc.py            #   DCF, owner earnings, biên an toàn, CAGR, ROIC…
│   ├── data_fetch.py          #   Lấy giá & BCTC (vnstock / yfinance), đối chiếu chéo
│   └── benford.py             #   Kiểm tra Định luật Benford — phát hiện số liệu bất thường
├── scripts/install.sh         # Cài skill vào ~/.claude/skills
└── requirements.txt
```

## 🔒 Nguyên tắc dữ liệu (bắt buộc trong mọi skill)

1. **Không float** — mọi phép tính tiền tệ dùng `decimal.Decimal` (`tools/fin_calc.py`).
2. **Xác minh chéo** — số liệu trọng yếu cần tối thiểu 2 nguồn độc lập; kết quả gắn
   nhãn độ tin cậy **A/B/C**.
3. **Tự kiểm tra** — ví dụ: `giá × số CP lưu hành` phải khớp vốn hoá công bố.
4. **Benford check** — chạy `tools/benford.py` trên chuỗi số liệu BCTC nhiều năm để
   phát hiện dấu hiệu "xào nấu" số liệu.
5. **Kết luận nhị phân** — mọi báo cáo phải chốt MUA/KHÔNG MUA kèm vùng giá cụ thể,
   cấm kiểu "một mặt… mặt khác…".

## ⚠️ Miễn trừ trách nhiệm

Công cụ này phục vụ **nghiên cứu và học tập**. Không phải khuyến nghị đầu tư.
Bạn tự chịu trách nhiệm với quyết định của mình.
