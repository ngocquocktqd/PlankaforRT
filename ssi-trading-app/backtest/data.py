"""Dữ liệu OHLC cho backtest — CSV là nguồn chuẩn, ssi-sdk là máy tải.

Format CSV mỗi mã một file `<SYMBOL>.csv`: date,open,high,low,close,volume
(date = YYYY-MM-DD, tăng dần). VNINDEX.csv (nếu có) dùng làm bộ lọc thị trường
+ benchmark.

Tải qua ssi-sdk chỉ chạy được ở máy có mạng + credential (sandbox chặn):
    python -m scripts.backtest fetch --symbols VN30 --from 2019-01-01
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class Bar:
    date: str          # YYYY-MM-DD
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


def load_csv(path: Path) -> list[Bar]:
    bars: list[Bar] = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            bars.append(Bar(
                date=row["date"].strip(),
                open=Decimal(row["open"]), high=Decimal(row["high"]),
                low=Decimal(row["low"]), close=Decimal(row["close"]),
                volume=int(float(row["volume"] or 0)),
            ))
    bars.sort(key=lambda b: b.date)
    return bars


def load_dir(csv_dir: Path) -> dict[str, list[Bar]]:
    """Nạp mọi <SYMBOL>.csv trong thư mục. Trả {symbol: bars}."""
    out: dict[str, list[Bar]] = {}
    for p in sorted(csv_dir.glob("*.csv")):
        sym = p.stem.upper()
        try:
            bars = load_csv(p)
        except (KeyError, ValueError) as e:
            print(f"  ⚠️ bỏ qua {p.name}: {e}")
            continue
        if len(bars) >= 260:  # cần ~1 năm+ để tính MA200/52W
            out[sym] = bars
        else:
            print(f"  ⚠️ bỏ qua {sym}: chỉ {len(bars)} phiên (<260)")
    return out


def save_csv(path: Path, bars: list[Bar]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for b in bars:
            w.writerow([b.date, b.open, b.high, b.low, b.close, b.volume])


def fetch_via_sdk(symbols: list[str], from_date: str, to_date: str,
                  csv_dir: Path) -> None:
    """Tải OHLC ngày qua ssi-sdk (phân trang) rồi lưu CSV. Cần credential SSI_*.

    from_date/to_date: YYYY-MM-DD (đổi sang YYYY/MM/DD cho SDK).
    """
    from ssi_sdk import Auth, Config, Data  # type: ignore

    import os
    cfg = Config(
        client_id=os.getenv("SSI_CLIENT_ID", ""),
        api_key=os.getenv("SSI_API_KEY", ""),
        api_secret=os.getenv("SSI_API_SECRET", ""),
    )
    auth = Auth(cfg)
    data = Data(auth)
    f, t = from_date.replace("-", "/"), to_date.replace("-", "/")

    for sym in symbols:
        bars: list[Bar] = []
        page = 1
        while True:
            chunk = data.market_data.get_ohlc_1day_historical(
                sym, from_date=f, to_date=t, page=page, size=1000)
            if not chunk:
                break
            for c in chunk:
                # trading_date của SDK có thể là DD/MM/YYYY → chuẩn hoá ISO
                d = c.trading_date
                if "/" in d:
                    p3 = d.split("/")
                    d = f"{p3[2]}-{p3[1]}-{p3[0]}" if len(p3[0]) <= 2 else d.replace("/", "-")
                bars.append(Bar(date=d,
                                open=Decimal(str(c.open_price)),
                                high=Decimal(str(c.high_price)),
                                low=Decimal(str(c.low_price)),
                                close=Decimal(str(c.close_price)),
                                volume=int(c.volume)))
            if len(chunk) < 1000:
                break
            page += 1
        bars.sort(key=lambda b: b.date)
        save_csv(csv_dir / f"{sym}.csv", bars)
        print(f"  ✓ {sym}: {len(bars)} phiên → {csv_dir / (sym + '.csv')}")
