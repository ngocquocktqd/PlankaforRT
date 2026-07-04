#!/usr/bin/env python3
"""Lấy dữ liệu giá & báo cáo tài chính cho cổ phiếu VN (vnstock) và quốc tế (yfinance).

Dùng:
    python3 data_fetch.py price FPT                # giá + vốn hoá, tự nhận diện thị trường
    python3 data_fetch.py price AAPL --market us
    python3 data_fetch.py financials FPT           # BCTC 5 năm (KQKD, CĐKT, LCTT)
    python3 data_fetch.py history VNM --years 5    # lịch sử giá
    python3 data_fetch.py screen                    # radar: quét VN30+MID theo Trend Template
    python3 data_fetch.py screen --universe mid     # chỉ rổ mid-cap (preset: vn30|mid|all)
    python3 data_fetch.py screen --universe FPT,HPG,MWG --min-from-low 0.30 --min-value 20

Quy ước nhận diện: mã 3 ký tự chữ hoa → mặc định thị trường VN; còn lại → quốc tế.
Ghi đè bằng --market vn|us.

Cài thư viện:  pip install -r stock-analysis/requirements.txt
Kết quả in ra kèm nguồn + thời điểm lấy để phục vụ xác minh chéo. Đây là MỘT nguồn;
số liệu trọng yếu vẫn cần đối chiếu nguồn thứ hai (web chính thống) theo quy tắc A/B/C.
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta


def detect_market(symbol: str, override: str | None) -> str:
    if override:
        return override
    return "vn" if len(symbol) == 3 and symbol.isalpha() and symbol.isupper() else "us"


def need(module: str, pip_name: str):
    try:
        return __import__(module)
    except ImportError:
        sys.exit(f"LỖI: thiếu thư viện '{pip_name}'. Cài bằng: pip install {pip_name}")


def stamp(source: str) -> None:
    print(f"\n[Nguồn: {source} | Lấy lúc: {datetime.now().isoformat(timespec='seconds')}]"
          f"\n[Nhắc: đây là 1 nguồn — số liệu trọng yếu cần nguồn thứ 2 để đạt nhãn A]")


# ---------- VN (vnstock) ----------

def vn_client(symbol: str):
    vnstock = need("vnstock", "vnstock")
    return vnstock.Vnstock().stock(symbol=symbol, source="VCI")


def vn_price(symbol: str) -> None:
    stock = vn_client(symbol)
    quote = stock.quote.history(start=str(date.today() - timedelta(days=14)),
                                end=str(date.today()), interval="1D")
    last = quote.iloc[-1]
    print(f"{symbol} — giá đóng cửa gần nhất ({last['time']}): {last['close']}")
    print(f"Khối lượng: {last['volume']}")
    try:
        overview = stock.company.overview()
        print(overview.T.to_string())
    except Exception as e:  # noqa: BLE001 - API phụ, không chặn kết quả giá
        print(f"(Không lấy được thông tin tổng quan công ty: {e})")
    stamp("vnstock/VCI")


def vn_financials(symbol: str) -> None:
    stock = vn_client(symbol)
    for name, df in [
        ("KẾT QUẢ KINH DOANH", stock.finance.income_statement(period="year")),
        ("CÂN ĐỐI KẾ TOÁN", stock.finance.balance_sheet(period="year")),
        ("LƯU CHUYỂN TIỀN TỆ", stock.finance.cash_flow(period="year")),
    ]:
        print(f"\n===== {name} (theo năm) =====")
        print(df.head(6).T.to_string())
    stamp("vnstock/VCI")


def vn_history(symbol: str, years: int) -> None:
    stock = vn_client(symbol)
    df = stock.quote.history(start=str(date.today() - timedelta(days=365 * years)),
                             end=str(date.today()), interval="1D")
    print(df.to_csv(index=False))
    stamp("vnstock/VCI")


# ---------- Quốc tế (yfinance) ----------

def us_price(symbol: str) -> None:
    yf = need("yfinance", "yfinance")
    t = yf.Ticker(symbol)
    info = t.info
    fields = ["currentPrice", "marketCap", "sharesOutstanding", "trailingPE",
              "forwardPE", "dividendYield", "totalCash", "totalDebt",
              "freeCashflow", "returnOnEquity", "profitMargins"]
    print(json.dumps({k: info.get(k) for k in fields}, indent=2, default=str))
    price, shares, mcap = info.get("currentPrice"), info.get("sharesOutstanding"), info.get("marketCap")
    if price and shares and mcap:
        diff = abs(price * shares - mcap) / mcap
        print(f"Kiểm tra chéo: giá×CP so với vốn hoá lệch {diff:.2%} "
              f"{'✅' if diff <= 0.03 else '🚩 >3%, điều tra thêm'}")
    stamp("yfinance")


def us_financials(symbol: str) -> None:
    yf = need("yfinance", "yfinance")
    t = yf.Ticker(symbol)
    for name, df in [("KẾT QUẢ KINH DOANH", t.income_stmt),
                     ("CÂN ĐỐI KẾ TOÁN", t.balance_sheet),
                     ("LƯU CHUYỂN TIỀN TỆ", t.cash_flow)]:
        print(f"\n===== {name} (theo năm) =====")
        print(df.to_string())
    stamp("yfinance")


def us_history(symbol: str, years: int) -> None:
    yf = need("yfinance", "yfinance")
    df = yf.Ticker(symbol).history(period=f"{years}y", interval="1d")
    print(df.to_csv())
    stamp("yfinance")


# Rổ mặc định cho lệnh screen. Radar lướt sóng nghiêng mid-cap (bài học ACB:
# large-cap chạy chậm, R:R mỏng) nên preset "all" = VN30 + MID.
VN30 = ("ACB BCM BID BVH CTG FPT GAS GVR HDB HPG MBB MSN MWG PLX POW SAB "
        "SHB SSB SSI STB TCB TPB VCB VHM VIB VIC VJC VNM VPB VRE").split()
MID = ("VND VCI HCM VIX MBS FTS BSI CTS DGC DPM DCM DGW FRT PNJ VHC ANV HAH "
       "GMD VSC PVD PC1 REE GEX VGC KBC IDC SZC NLG KDH DXG HDG DBC HSG NKG "
       "VTP CTR EVF").split()
UNIVERSE_PRESETS = {"vn30": VN30, "mid": MID, "all": VN30 + MID}


def vn_screen(universe: list[str], min_from_low: float, min_value: float) -> None:
    """Radar Chế độ B — quét Trend Template rút gọn cho một rổ mã VN (cần vnstock).

    Với mỗi mã: lấy ~1 năm giá, tính MA50/150/200, kiểm các tiêu chí Minervini
    (giá > các MA, MA xếp thứ tự, MA200 dốc lên, cách đỉnh 52T ≤25%, trên đáy 52T
    ≥ min_from_low), đo RS đơn giản (hiệu suất 6 tháng) và GTGD bình quân 20 phiên
    (tỷ VND — lọc thanh khoản min_value). In các mã ĐẠT cho Vòng 1 của radar.
    Sandbox chặn vnstock (403) nên hàm này chỉ chạy khi có mạng vnstock (vd máy local).
    """
    import statistics

    passed = []
    print(f"{'Mã':>6} {'Giá':>10} {'MA50':>10} {'MA200':>10} "
          f"{'%đáy':>7} {'%đỉnh':>7} {'6th':>7} {'GTGD':>8}  Kết quả")
    for sym in universe:
        try:
            stock = vn_client(sym)
            df = stock.quote.history(start=str(date.today() - timedelta(days=400)),
                                     end=str(date.today()), interval="1D")
            closes = [float(x) for x in df["close"].tolist()]
            vols = [float(x) for x in df["volume"].tolist()]
            if len(closes) < 200:
                print(f"{sym:>6}  (thiếu dữ liệu, bỏ qua)")
                continue
            price = closes[-1]
            ma50 = statistics.fmean(closes[-50:])
            ma150 = statistics.fmean(closes[-150:])
            ma200 = statistics.fmean(closes[-200:])
            hi52, lo52 = max(closes[-250:]), min(closes[-250:])
            from_low = (price - lo52) / lo52
            from_high = (price - hi52) / hi52
            ret6m = (price - closes[-120]) / closes[-120] if len(closes) >= 120 else 0.0
            # GTGD bình quân 20 phiên, đơn vị tỷ VND (giá vnstock tính bằng VND)
            avg_value = statistics.fmean(c * v for c, v in
                                         zip(closes[-20:], vols[-20:])) / 1e9
            liquid = avg_value >= min_value
            ok = (price > ma50 > ma150 > ma200 and ma200 > statistics.fmean(closes[-220:-20])
                  and from_high >= -0.25 and from_low >= min_from_low and liquid)
            note = "✅ ĐẠT momentum" if ok else ("— (kém thanh khoản)" if not liquid else "—")
            print(f"{sym:>6} {price:>10.0f} {ma50:>10.0f} {ma200:>10.0f} "
                  f"{from_low:>6.0%} {from_high:>6.0%} {ret6m:>6.0%} {avg_value:>7.0f}t  {note}")
            if ok:
                passed.append((sym, ret6m))
        except Exception as e:  # noqa: BLE001 - một mã lỗi không được chặn cả rổ
            print(f"{sym:>6}  (lỗi: {e})")

    print("\n=== ĐẠT bộ lọc momentum + thanh khoản (xếp theo RS 6 tháng) ===")
    for sym, r in sorted(passed, key=lambda x: x[1], reverse=True):
        print(f"  {sym}  (6th {r:+.0%})")
    print("\n[Bước tiếp] Với mỗi mã ĐẠT: kiểm tăng trưởng LN quý gần nhất bằng "
          "`data_fetch.py financials <mã>` (loại mã earnings giảm tốc — bẫy CTS), "
          "rồi dựng trade-plan. Đây mới là Vòng 1 của radar — chưa lọc chất lượng.")
    stamp("vnstock/VCI")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["price", "financials", "history", "screen"])
    p.add_argument("symbol", nargs="?", help="Mã CP (không cần cho lệnh screen)")
    p.add_argument("--market", choices=["vn", "us"], help="Ghi đè nhận diện thị trường")
    p.add_argument("--years", type=int, default=5)
    p.add_argument("--universe", help="screen: preset vn30|mid|all hoặc danh sách mã "
                                      "phân tách bằng dấu phẩy (mặc định: all)")
    p.add_argument("--min-from-low", type=float, default=0.30,
                   help="screen: ngưỡng %% tối thiểu trên đáy 52T (mặc định 0.30)")
    p.add_argument("--min-value", type=float, default=20.0,
                   help="screen: GTGD bình quân 20 phiên tối thiểu, tỷ VND (mặc định 20)")
    a = p.parse_args()

    if a.cmd == "screen":
        key = (a.universe or "all").strip().lower()
        universe = UNIVERSE_PRESETS.get(key) or \
            [s.strip().upper() for s in a.universe.split(",")]
        vn_screen(universe, a.min_from_low, a.min_value)
        return

    if not a.symbol:
        p.error("cần 'symbol' cho lệnh price/financials/history")
    symbol = a.symbol.upper()
    market = detect_market(symbol, a.market)
    fn = {("vn", "price"): vn_price, ("vn", "financials"): vn_financials,
          ("vn", "history"): lambda s: vn_history(s, a.years),
          ("us", "price"): us_price, ("us", "financials"): us_financials,
          ("us", "history"): lambda s: us_history(s, a.years)}[(market, a.cmd)]
    fn(symbol)


if __name__ == "__main__":
    main()
