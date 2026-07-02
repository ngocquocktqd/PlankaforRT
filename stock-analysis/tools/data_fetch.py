#!/usr/bin/env python3
"""Lấy dữ liệu giá & báo cáo tài chính cho cổ phiếu VN (vnstock) và quốc tế (yfinance).

Dùng:
    python3 data_fetch.py price FPT                # giá + vốn hoá, tự nhận diện thị trường
    python3 data_fetch.py price AAPL --market us
    python3 data_fetch.py financials FPT           # BCTC 5 năm (KQKD, CĐKT, LCTT)
    python3 data_fetch.py history VNM --years 5    # lịch sử giá

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


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["price", "financials", "history"])
    p.add_argument("symbol")
    p.add_argument("--market", choices=["vn", "us"], help="Ghi đè nhận diện thị trường")
    p.add_argument("--years", type=int, default=5)
    a = p.parse_args()

    symbol = a.symbol.upper()
    market = detect_market(symbol, a.market)
    fn = {("vn", "price"): vn_price, ("vn", "financials"): vn_financials,
          ("vn", "history"): lambda s: vn_history(s, a.years),
          ("us", "price"): us_price, ("us", "financials"): us_financials,
          ("us", "history"): lambda s: us_history(s, a.years)}[(market, a.cmd)]
    fn(symbol)


if __name__ == "__main__":
    main()
