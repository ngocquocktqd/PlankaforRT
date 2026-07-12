# 🥇 Gold Trading Toolkit — phân tích & lướt sóng VÀNG trên Claude Code

Bộ công cụ nghiên cứu và giao dịch **vàng (XAU/USD + vàng VN)** chạy trên **Claude Code**,
theo triết lý **dò CHẾ ĐỘ trước, đọc driver sau**: trọng số các yếu tố vĩ mô KHÔNG cố định
mà đổi theo thời kỳ — ai đang là "người mua biên" mới là câu hỏi trung tâm.

> 📜 Bài học nền: tương quan vàng × lãi suất thực (TIPS 10Y) = **84%** giai đoạn 2005–2021
> nhưng **sụp còn 3–7%** từ 2022 khi NHTW mua >1.000 tấn/năm trở thành người mua biên. Áp
> một quy luật cứng ("không cãi real yield") xuyên suốt là sai — phải dò chế độ mỗi lần.

## 🛠️ Cài đặt
```bash
# 1. Cài Claude Code
npm install -g @anthropic-ai/claude-code
# 2. Cài skill vào Claude Code
./scripts/install.sh
```

## 🚀 Sử dụng
```
/hoi-dong-vang                 # Hội đồng đầy đủ: 4 agent driver + dò chế độ → bias + kế hoạch khung
/hoi-dong-vang nhanh           # Chỉ cập nhật driver + mức giá
/luot-song-vang                # Lướt sóng nhanh: kế thừa chế độ → lệnh 2 chiều + R:R + trailing
/luot-song-vang đã mua 4165    # Quản trị vị thế đang có (hoặc "đã short 4300")
```

## 🧠 Kiến trúc 2 lớp
- **`/hoi-dong-vang`** (nặng, ~tuần/sau sự kiện lớn) — 4 agent chạy song song theo *cơ chế
  truyền dẫn* (khung GRAM của World Gold Council):
  1. **Chi-phí-cơ-hội** — real yield TIPS 10Y, FedWatch, CPI/NFP, DXY (mỏ neo chế độ cũ)
  2. **Dòng-tiền-cấu-trúc** — NHTW mua ròng, phi-đô-la-hoá, premium SGE, ETF Đông vs Tây
     (người mua biên chế độ mới — *không có trong mô hình cũ*)
  3. **Sợ-hãi & Nợ** — địa chính trị (áp *quy luật bốc hơi*: thoáng qua vs cấu trúc), thâm
     hụt/nợ Mỹ, độc lập Fed
  4. **Kỹ-thuật & Positioning** — Stage, 4 mẫu setup, COT/RSI làm lớp phủ ngược chiều
  → **Bước 0.5 dò chế độ** (CŨ / MỚI / LAI) quyết định *trọng số* các agent, không cào bằng.
- **`/luot-song-vang`** (nhanh) — kế thừa chế độ + bias từ `reports/vang.md`, chỉ làm tươi
  kỹ thuật → kế hoạch giao dịch cụ thể: điểm vào/ra 2 chiều, stop theo cấu trúc + ATR,
  R:R ≥2:1, **hệ số size theo độ thuận chế độ** (thuận = chuẩn, cãi = ½ + chỉ T1, cửa sổ
  sự kiện ≤48h = 0).

## 📁 Cấu trúc
```
gold-analysis/
├── skills/
│   ├── hoi-dong-vang/       # Hội đồng 4 agent + dò chế độ
│   └── luot-song-vang/      # Lướt sóng nhanh: lệnh + quản trị vị thế
├── reports/
│   └── vang.md              # Nhật ký CHẾ ĐỘ + nhật ký lệnh (theo dõi đổi chế độ giữa các lần chạy)
└── scripts/install.sh
```

## 🔒 Nguyên tắc thép
1. **Dò chế độ trước, đọc driver sau** — trọng số là đầu ra của bước dò, không mặc định.
2. **Câu hỏi trung tâm: ai là người mua biên?** — mọi báo cáo phải trả lời, kèm bằng chứng
   dòng tiền (WGC/ETF/SGE/COT).
3. **Sự kiện ≤48h (CPI/FOMC/NFP) = cấm vào lệnh mới** — vàng gap vài chục USD qua tin.
4. **Stop theo cấu trúc + ATR**, không số tròn; R:R ≥2:1 cho lệnh thuận bias.
5. **Vàng VN**: luôn ghi premium SJC/nhẫn so quy đổi — premium phình ăn hết lãi thế giới.
6. **Ghi CHẾ ĐỘ mỗi lần chạy vào `reports/vang.md`** — đổi chế độ là tín hiệu lớn hơn số lẻ.

## ⚠️ Miễn trừ trách nhiệm
Phục vụ **nghiên cứu và học tập**. Không phải khuyến nghị đầu tư. Vàng và phái sinh vàng có
rủi ro cao; bạn tự chịu trách nhiệm với quyết định của mình.
