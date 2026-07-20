"""Backtest CHÂN CƠ HỌC của framework lướt sóng — trung thực về giới hạn.

Test được (máy móc hoá 1:1 từ radar + hội đồng lướt sóng):
  - Trend Template rút gọn (giá > MA50/150/200, MA xếp thứ tự, MA200 dốc lên,
    ≥+30% đáy 52T, ≤25% dưới đỉnh 52T)
  - Breakout pivot: close vượt đỉnh nền N phiên + volume ≥ 1,5× TB50
  - Bộ lọc THỊ TRƯỜNG (Bước 0): chỉ vào lệnh khi index > MA200 index
  - Stop cứng 7%, hoà vốn sau +1R, trailing MA20 khi ≥+1R, gãy MA50 → thoát,
    time-stop 120 phiên (~6 tháng)
  - Sizing: rủi ro 1% equity/lệnh, trần vị thế 15% equity, tối đa 5 vị thế
  - Phí + trượt giá 2 chiều; vào lệnh Ở PHIÊN SAU tín hiệu (không look-ahead)

KHÔNG test được (nói thẳng, in vào mọi báo cáo):
  - Chân O'Neil (earnings tăng tốc) — không có lịch sử BCTC máy đọc được
  - Phán đoán hội đồng (dò mìn, catalyst) — backtest LLM = nhiễm hindsight
  - Survivorship bias: universe là danh sách HÔM NAY (mã đã huỷ niêm yết vắng mặt)
→ Kết quả là CẬN TRÊN LẠC QUAN của riêng chân kỹ thuật, không phải của cả framework.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from statistics import fmean

from .data import Bar

D = Decimal
Q = D("0.01")


@dataclass
class Params:
    stop_pct: Decimal = D("0.07")          # stop cứng 7% dưới giá vào
    fee_pct: Decimal = D("0.0015")         # phí 0,15%/chiều
    slippage_pct: Decimal = D("0.001")     # trượt giá 0,1%/chiều
    risk_pct: Decimal = D("0.01")          # rủi ro 1% equity/lệnh
    max_pos_pct: Decimal = D("0.15")       # trần 15% equity/vị thế
    max_positions: int = 5
    base_lookback: int = 50                # đỉnh nền = max(high 50 phiên trước)
    vol_mult: Decimal = D("1.5")           # volume breakout ≥1,5× TB50
    time_stop_bars: int = 120              # ~6 tháng
    min_from_low: Decimal = D("0.30")
    max_from_high: Decimal = D("0.25")
    trail_ma: int = 20
    breakeven_r: Decimal = D("1")          # +1R → dời stop hoà vốn


@dataclass
class Trade:
    symbol: str
    entry_date: str
    entry: Decimal
    stop0: Decimal                 # stop ban đầu (định nghĩa 1R)
    qty: int
    exit_date: str = ""
    exit: Decimal = D("0")
    reason: str = ""
    r_multiple: Decimal = D("0")
    pnl: Decimal = D("0")


@dataclass
class _Series:
    """Chuỗi chỉ báo tiền tính cho một mã (tính 1 lần, tra O(1) theo index)."""
    bars: list[Bar]
    ma20: list[Decimal | None] = field(default_factory=list)
    ma50: list[Decimal | None] = field(default_factory=list)
    ma150: list[Decimal | None] = field(default_factory=list)
    ma200: list[Decimal | None] = field(default_factory=list)
    vol50: list[Decimal | None] = field(default_factory=list)
    hi52: list[Decimal | None] = field(default_factory=list)
    lo52: list[Decimal | None] = field(default_factory=list)
    base_hi: list[Decimal | None] = field(default_factory=list)


def _sma(vals: list[Decimal], n: int, i: int) -> Decimal | None:
    if i + 1 < n:
        return None
    return D(str(fmean(float(v) for v in vals[i + 1 - n: i + 1])))


def _precompute(bars: list[Bar], p: Params) -> _Series:
    s = _Series(bars=bars)
    closes = [b.close for b in bars]
    vols = [D(b.volume) for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    for i in range(len(bars)):
        s.ma20.append(_sma(closes, p.trail_ma, i))
        s.ma50.append(_sma(closes, 50, i))
        s.ma150.append(_sma(closes, 150, i))
        s.ma200.append(_sma(closes, 200, i))
        s.vol50.append(_sma(vols, 50, i))
        lo, hi = i + 1 - 250, i + 1
        s.hi52.append(max(highs[max(lo, 0):hi]) if i >= 200 else None)
        s.lo52.append(min(lows[max(lo, 0):hi]) if i >= 200 else None)
        b0 = i - p.base_lookback
        s.base_hi.append(max(highs[max(b0, 0):i]) if i >= p.base_lookback else None)
    return s


def _signal(s: _Series, i: int, p: Params) -> bool:
    """Tín hiệu MUA tại close phiên i (vào lệnh phiên i+1). Trend Template + breakout."""
    b = s.bars[i]
    ma50, ma150, ma200 = s.ma50[i], s.ma150[i], s.ma200[i]
    if None in (ma50, ma150, ma200, s.hi52[i], s.lo52[i], s.base_hi[i], s.vol50[i]):
        return False
    if i < 220 or s.ma200[i - 20] is None:
        return False
    c = b.close
    tt = (c > ma50 > ma150 > ma200
          and ma200 > s.ma200[i - 20]                      # MA200 dốc lên
          and c >= s.lo52[i] * (1 + p.min_from_low)        # ≥ +30% đáy 52T
          and c >= s.hi52[i] * (1 - p.max_from_high))      # ≤ 25% dưới đỉnh
    if not tt:
        return False
    breakout = (c > s.base_hi[i]
                and D(b.volume) >= s.vol50[i] * p.vol_mult)
    return breakout


def run_backtest(data: dict[str, list[Bar]], index_bars: list[Bar] | None,
                 params: Params | None = None,
                 start_equity: Decimal = D("500000000")) -> dict:
    p = params or Params()
    series = {sym: _precompute(bars, p) for sym, bars in data.items()}

    # Bộ lọc thị trường: index > MA200 index (thiếu data index → luôn cho vào, có cảnh báo)
    idx_ok: dict[str, bool] = {}
    if index_bars:
        idx_closes = [b.close for b in index_bars]
        for i, b in enumerate(index_bars):
            ma = _sma(idx_closes, 200, i)
            idx_ok[b.date] = (ma is not None and b.close > ma)

    # Trục thời gian hợp nhất + map ngày → index của từng mã
    all_dates = sorted({b.date for bars in data.values() for b in bars})
    pos_of = {sym: {b.date: i for i, b in enumerate(s.bars)} for sym, s in series.items()}

    equity = start_equity
    cash = start_equity
    open_pos: dict[str, Trade] = {}
    entry_bar_i: dict[str, int] = {}
    peak_after_entry: dict[str, Decimal] = {}
    pending: list[str] = []           # tín hiệu hôm qua → vào hôm nay
    trades: list[Trade] = []
    eq_curve: list[tuple[str, Decimal]] = []

    def exec_buy(sym: str, date: str) -> None:
        nonlocal cash
        s = series[sym]
        i = pos_of[sym].get(date)
        if i is None or sym in open_pos or len(open_pos) >= p.max_positions:
            return
        entry = s.bars[i].open * (1 + p.slippage_pct)
        stop0 = entry * (1 - p.stop_pct)
        risk_ps = entry - stop0
        qty = int(min(equity * p.risk_pct / risk_ps,
                      equity * p.max_pos_pct / entry) / 100) * 100
        if qty <= 0 or entry * qty > cash:
            return
        fee = entry * qty * p.fee_pct
        cash -= entry * qty + fee
        open_pos[sym] = Trade(symbol=sym, entry_date=date, entry=entry,
                              stop0=stop0, qty=qty)
        entry_bar_i[sym] = i
        peak_after_entry[sym] = entry

    def exec_sell(sym: str, date: str, price: Decimal, reason: str) -> None:
        nonlocal cash
        t = open_pos.pop(sym)
        px = price * (1 - p.slippage_pct)
        fee = px * t.qty * p.fee_pct
        cash += px * t.qty - fee
        t.exit_date, t.exit, t.reason = date, px, reason
        risk = (t.entry - t.stop0) * t.qty
        t.pnl = ((px - t.entry) * t.qty - fee
                 - t.entry * t.qty * p.fee_pct).quantize(Q)
        t.r_multiple = (t.pnl / risk).quantize(D("0.01")) if risk else D("0")
        trades.append(t)
        entry_bar_i.pop(sym, None)
        peak_after_entry.pop(sym, None)

    warn_no_index = index_bars is None

    for date in all_dates:
        # 1. vào lệnh chờ từ tín hiệu hôm trước (lọc thị trường tại ngày vào)
        market_open = idx_ok.get(date, True)
        if market_open:
            for sym in pending:
                exec_buy(sym, date)
        pending = []

        # 2. quản trị vị thế đang mở
        for sym in list(open_pos):
            i = pos_of[sym].get(date)
            if i is None:
                continue
            s, t = series[sym], open_pos[sym]
            b = s.bars[i]
            risk_ps = t.entry - t.stop0
            peak_after_entry[sym] = max(peak_after_entry[sym], b.high)
            stop = t.stop0
            if peak_after_entry[sym] >= t.entry + p.breakeven_r * risk_ps:
                stop = max(stop, t.entry)                       # hoà vốn sau +1R
            # thứ tự trong phiên: gap/stop trước, rồi tín hiệu đóng cửa
            if b.open <= stop:
                exec_sell(sym, date, b.open, "gap_stop"); continue
            if b.low <= stop:
                exec_sell(sym, date, stop, "stop"); continue
            gain_r = (b.close - t.entry) / risk_ps if risk_ps else D("0")
            if gain_r >= 1 and s.ma20[i] is not None and b.close < s.ma20[i]:
                exec_sell(sym, date, b.close, "trail_ma20"); continue
            if s.ma50[i] is not None and b.close < s.ma50[i]:
                exec_sell(sym, date, b.close, "break_ma50"); continue
            if i - entry_bar_i[sym] >= p.time_stop_bars:
                exec_sell(sym, date, b.close, "time_stop"); continue

        # 3. quét tín hiệu mới tại close (vào phiên sau)
        for sym, s in series.items():
            if sym in open_pos:
                continue
            i = pos_of[sym].get(date)
            if i is not None and _signal(s, i, p):
                pending.append(sym)
        # ưu tiên RS 6 tháng mạnh nhất nếu nhiều tín hiệu cùng ngày
        if len(pending) > 1:
            def rs6(sym: str) -> float:
                i = pos_of[sym][date]
                j = max(i - 120, 0)
                return float(series[sym].bars[i].close / series[sym].bars[j].close)
            pending.sort(key=rs6, reverse=True)

        # 4. mark-to-market
        mtm = cash
        for sym, t in open_pos.items():
            i = pos_of[sym].get(date)
            px = series[sym].bars[i].close if i is not None else t.entry
            mtm += px * t.qty
        equity = mtm
        eq_curve.append((date, equity))

    # đóng vị thế treo cuối kỳ (đánh dấu rõ, không tính là kết quả luật)
    if all_dates:
        for sym in list(open_pos):
            i = pos_of[sym].get(all_dates[-1])
            last_bar = series[sym].bars[i if i is not None else -1]
            exec_sell(sym, last_bar.date, last_bar.close, "eod_forced")

    return _report(trades, eq_curve, start_equity, index_bars, warn_no_index)


def _report(trades: list[Trade], eq_curve: list, start_equity: Decimal,
            index_bars: list[Bar] | None, warn_no_index: bool) -> dict:
    closed = [t for t in trades if t.reason != "eod_forced"]
    wins = [t for t in closed if t.pnl > 0]
    losses = [t for t in closed if t.pnl <= 0]
    gross_win = sum((t.pnl for t in wins), D("0"))
    gross_loss = -sum((t.pnl for t in losses), D("0"))

    peak = start_equity
    max_dd = D("0")
    for _, eq in eq_curve:
        peak = max(peak, eq)
        max_dd = min(max_dd, (eq / peak - 1) * 100)

    final = eq_curve[-1][1] if eq_curve else start_equity
    years = max(len(eq_curve) / 250, D("0.01"))
    cagr = ((float(final / start_equity)) ** (1 / float(years)) - 1) * 100

    bench = None
    if index_bars and len(index_bars) >= 2:
        bench = float(index_bars[-1].close / index_bars[0].close - 1) * 100

    out = {
        "n_trades": len(closed),
        "n_forced_eod": len(trades) - len(closed),
        "win_rate_pct": (round(len(wins) / len(closed) * 100, 1) if closed else None),
        "avg_r": (str((sum((t.r_multiple for t in closed), D("0")) / len(closed))
                      .quantize(D("0.01"))) if closed else None),
        "profit_factor": (str((gross_win / gross_loss).quantize(D("0.01")))
                          if gross_loss > 0 else None),
        "total_return_pct": str(((final / start_equity - 1) * 100).quantize(Q)),
        "cagr_pct": round(cagr, 2),
        "max_drawdown_pct": str(max_dd.quantize(Q)),
        "buyhold_index_pct": (round(bench, 2) if bench is not None else None),
        "final_equity": str(final.quantize(Q)),
        "exit_reasons": {},
        "trades": [t.__dict__ | {k: str(v) for k, v in t.__dict__.items()
                                 if isinstance(v, Decimal)} for t in trades],
        "caveats": [
            "Chỉ test CHÂN KỸ THUẬT (Trend Template + breakout + stop) — KHÔNG có "
            "lọc earnings O'Neil và phán đoán hội đồng → kết quả là cận trên lạc quan "
            "của riêng chân này, không phải của cả framework.",
            "Survivorship bias: universe là danh sách hôm nay (mã huỷ niêm yết vắng mặt).",
            "Phí 0,15%/chiều + trượt 0,1% là giả định; mã kém thanh khoản trượt nhiều hơn.",
            "Dưới ~30 lệnh → không đủ mẫu, đừng kết luận.",
        ],
    }
    if warn_no_index:
        out["caveats"].insert(0, "THIẾU VNINDEX.csv → bộ lọc thị trường (Bước 0) bị TẮT "
                                 "— kết quả sẽ đẹp/xấu hơn thực tế tuỳ giai đoạn.")
    reasons: dict[str, int] = {}
    for t in trades:
        reasons[t.reason] = reasons.get(t.reason, 0) + 1
    out["exit_reasons"] = reasons
    return out
