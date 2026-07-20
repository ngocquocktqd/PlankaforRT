"""CLI backtest chân cơ học. Chạy từ thư mục ssi-trading-app.

  # 1. Tải data (máy local, cần credential SSI_* trong env — sandbox bị chặn):
  python -m scripts.backtest fetch --symbols FPT,HPG,MWG,SSI,VNINDEX \
      --from 2019-01-01 --to 2026-07-20 --csv-dir data/ohlc

  # 2. Chạy backtest trên CSV:
  python -m scripts.backtest run --csv-dir data/ohlc [--start-equity 500000000]

VNINDEX.csv (nếu có trong csv-dir) tự động thành bộ lọc thị trường + benchmark.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backtest.data import fetch_via_sdk, load_dir  # noqa: E402
from backtest.engine import Params, run_backtest  # noqa: E402

VN30_DEFAULT = ("ACB BID CTG FPT GAS HPG MBB MSN MWG PLX SAB SSI STB TCB VCB "
                "VHM VIB VIC VJC VNM VPB VRE PVD PVS DGC DBC VND HCM VNINDEX").split()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="tải OHLC qua ssi-sdk → CSV")
    f.add_argument("--symbols", default="vn30",
                   help="'vn30' hoặc danh sách mã phẩy (thêm VNINDEX để có bộ lọc)")
    f.add_argument("--from", dest="from_date", required=True)
    f.add_argument("--to", dest="to_date", default="2026-12-31")
    f.add_argument("--csv-dir", default="data/ohlc")

    r = sub.add_parser("run", help="chạy backtest trên thư mục CSV")
    r.add_argument("--csv-dir", default="data/ohlc")
    r.add_argument("--start-equity", default="500000000")
    r.add_argument("--json-out", help="ghi kết quả đầy đủ (kèm từng lệnh) ra file JSON")

    a = ap.parse_args()

    if a.cmd == "fetch":
        syms = (VN30_DEFAULT if a.symbols.strip().lower() == "vn30"
                else [s.strip().upper() for s in a.symbols.split(",")])
        fetch_via_sdk(syms, a.from_date, a.to_date, Path(a.csv_dir))
        return

    csv_dir = Path(a.csv_dir)
    if not csv_dir.exists():
        sys.exit(f"Không thấy {csv_dir} — chạy 'fetch' trước (máy local) hoặc tự đặt CSV vào.")
    data = load_dir(csv_dir)
    index_bars = data.pop("VNINDEX", None)
    if not data:
        sys.exit("Không có mã nào đủ dữ liệu (≥260 phiên).")
    print(f"▶ {len(data)} mã, index: {'CÓ' if index_bars else 'KHÔNG (bộ lọc thị trường TẮT)'}")

    result = run_backtest(data, index_bars,
                          start_equity=Decimal(a.start_equity))

    print("\n===== KẾT QUẢ (chân cơ học) =====")
    for k in ("n_trades", "win_rate_pct", "avg_r", "profit_factor",
              "total_return_pct", "cagr_pct", "max_drawdown_pct",
              "buyhold_index_pct", "final_equity", "exit_reasons", "n_forced_eod"):
        print(f"  {k:20}: {result[k]}")
    print("\n⚠️ GIỚI HẠN (đọc bắt buộc):")
    for c in result["caveats"]:
        print(f"  - {c}")

    if a.json_out:
        Path(a.json_out).write_text(
            json.dumps(result, ensure_ascii=False, indent=1, default=str),
            encoding="utf-8")
        print(f"\n✓ Chi tiết từng lệnh → {a.json_out}")


if __name__ == "__main__":
    main()
