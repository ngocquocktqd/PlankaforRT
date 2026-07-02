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
/phan-tich-dau-tu FPT              # Phân tích sâu một công ty
/hoi-dong-dau-tu HPG               # 4 agent đối kháng phân tích song song
/doc-bao-cao-tai-chinh VNM         # Đọc sâu BCTC / báo cáo thường niên
/loc-co-phieu ngành bán lẻ         # Phễu lọc ngành 30 → 10 → 3
/checklist-dau-tu MWG, FPT, PNJ    # Checklist 6 cổng kiểu Buffett
/theo-doi-luan-diem VCB            # Theo dõi luận điểm sau khi đã mua
```

## 📁 Cấu trúc

```
stock-analysis/
├── skills/                    # Các skill Claude Code (slash command)
│   ├── phan-tich-dau-tu/      #   Phân tích sâu 1 công ty qua 4 lăng kính
│   ├── hoi-dong-dau-tu/       #   4 agent độc lập + Trưởng nhóm tổng hợp
│   ├── doc-bao-cao-tai-chinh/ #   Đọc sâu BCTC, soi chất lượng lợi nhuận
│   ├── loc-co-phieu/          #   Phễu lọc ngành 30 → 10 → 3
│   ├── checklist-dau-tu/      #   6 cổng kiểm tra kiểu Buffett
│   └── theo-doi-luan-diem/    #   Giám sát luận điểm đầu tư sau giải ngân
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
