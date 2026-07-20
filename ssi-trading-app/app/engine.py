"""Engine luận điểm — tính VỊ THẾ và P&L THEO TỪNG LUẬN ĐIỂM (Decimal, giá vốn bình quân).

Đây là giá trị cốt lõi: không chỉ P&L tổng, mà lãi/lỗ gắn với TỪNG luận điểm — để biết
luận điểm nào thực sự kiếm tiền, luận điểm nào chỉ đúng trên giấy.
"""
from __future__ import annotations

from decimal import Decimal

from .models import Level, LevelKind, Side, Thesis, Trade

Q = Decimal("0.01")


def _d(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def position_and_pnl(trades: list[Trade], last_price: Decimal | None) -> dict:
    """Giá vốn bình quân. Bán → chốt lãi thực (realized); phần còn lại → lãi tạm (unrealized).

    Trả về: net_qty, avg_cost, realized_pnl, unrealized_pnl, total_pnl, invested, fees.
    """
    net_qty = 0
    avg_cost = Decimal("0")     # giá vốn bình quân của phần đang nắm
    realized = Decimal("0")
    fees = Decimal("0")

    for t in sorted(trades, key=lambda x: (x.executed_at, x.id or 0)):
        price = _d(t.price)
        fee = _d(t.fee)
        fees += fee
        if t.side == Side.BUY:
            # cập nhật giá vốn bình quân (gồm phí phân bổ vào giá vốn)
            new_cost_base = avg_cost * net_qty + price * t.quantity + fee
            net_qty += t.quantity
            avg_cost = (new_cost_base / net_qty) if net_qty else Decimal("0")
        else:  # SELL
            qty = min(t.quantity, net_qty)  # không cho bán khống trong sổ paper
            realized += (price - avg_cost) * qty - fee
            net_qty -= qty
            if net_qty == 0:
                avg_cost = Decimal("0")

    invested = (avg_cost * net_qty).quantize(Q)
    unrealized = Decimal("0")
    if net_qty > 0 and last_price is not None:
        unrealized = (_d(last_price) - avg_cost) * net_qty

    total = realized + unrealized
    ret_pct = (total / invested * 100) if invested > 0 else Decimal("0")

    return {
        "net_qty": net_qty,
        "avg_cost": avg_cost.quantize(Q),
        "invested": invested,
        "realized_pnl": realized.quantize(Q),
        "unrealized_pnl": unrealized.quantize(Q),
        "total_pnl": total.quantize(Q),
        "return_pct": ret_pct.quantize(Q),
        "fees": fees.quantize(Q),
        "last_price": (_d(last_price).quantize(Q) if last_price is not None else None),
    }


def check_levels(levels: list[Level], last_price: Decimal | None) -> list[dict]:
    """Đối chiếu giá hiện tại với các mốc → cờ cảnh báo (đã chạm entry/stop/target/vùng mua)."""
    if last_price is None:
        return []
    p = _d(last_price)
    out: list[dict] = []
    for lv in levels:
        price = _d(lv.price)
        hit = False
        msg = ""
        if lv.kind in (LevelKind.STOP,):
            hit = p <= price
            msg = "⛔ Chạm/thủng STOP" if hit else ""
        elif lv.kind in (LevelKind.ENTRY,):
            hit = p >= price
            msg = "🟢 Đã phá điểm vào" if hit else ""
        elif lv.kind in (LevelKind.TARGET,):
            hit = p >= price
            msg = "🎯 Đạt mục tiêu" if hit else ""
        elif lv.kind in (LevelKind.ACCUMULATE, LevelKind.BUY_HOI):
            hit = p <= price
            msg = "📥 Vào vùng mua" if hit else ""
        if hit:
            out.append({"level_id": lv.id, "kind": lv.kind.value,
                        "price": str(price), "note": lv.note, "msg": msg})
    return out


def performance_stats(rows: list[tuple[Thesis, Decimal | None]]) -> dict:
    """Thống kê hiệu suất toàn sổ. rows = [(thesis, last_price)].

    - Tổng: realized/unrealized/fees/vốn đang nằm/số lệnh.
    - Win rate: tính trên các luận điểm ĐÃ CÓ lãi/lỗ chốt (realized ≠ 0) —
      trung thực với dữ liệu ít, không tô vẽ.
    - Theo mode (value/momentum/cw) và bảng xếp hạng từng luận điểm.
    """
    z = Decimal("0")
    tot = {"realized": z, "unrealized": z, "fees": z, "invested": z, "n_trades": 0}
    by_mode: dict[str, dict] = {}
    per_thesis: list[dict] = []
    wins = losses = 0

    for th, price in rows:
        pnl = position_and_pnl(list(th.trades), price)
        tot["realized"] += pnl["realized_pnl"]
        tot["unrealized"] += pnl["unrealized_pnl"]
        tot["fees"] += pnl["fees"]
        tot["invested"] += pnl["invested"]
        tot["n_trades"] += len(th.trades)

        m = by_mode.setdefault(th.mode.value,
                               {"realized": z, "unrealized": z, "n": 0})
        m["realized"] += pnl["realized_pnl"]
        m["unrealized"] += pnl["unrealized_pnl"]
        m["n"] += 1

        if pnl["realized_pnl"] > 0:
            wins += 1
        elif pnl["realized_pnl"] < 0:
            losses += 1

        if th.trades:
            per_thesis.append({
                "thesis_id": th.id, "symbol": th.symbol, "mode": th.mode.value,
                "state": th.state.value,
                "realized": str(pnl["realized_pnl"]),
                "unrealized": str(pnl["unrealized_pnl"]),
                "total": str(pnl["total_pnl"]),
                "return_pct": str(pnl["return_pct"]),
                "n_trades": len(th.trades),
            })

    per_thesis.sort(key=lambda r: Decimal(r["total"]), reverse=True)
    decided = wins + losses
    return {
        "totals": {k: (str(v) if isinstance(v, Decimal) else v) for k, v in tot.items()},
        "total_pnl": str(tot["realized"] + tot["unrealized"]),
        "win_rate": (f"{wins}/{decided}" if decided else None),
        "win_rate_pct": (str((Decimal(wins) / decided * 100).quantize(Q)) if decided else None),
        "by_mode": {k: {kk: (str(vv) if isinstance(vv, Decimal) else vv)
                        for kk, vv in v.items()} for k, v in by_mode.items()},
        "per_thesis": per_thesis,
    }


def rr_metrics(levels: list[Level], pnl: dict, last_price: Decimal | None) -> dict | None:
    """R:R kế hoạch (entry/stop/target từ Levels) + R hiện tại của vị thế đang mở.

    - plan_rr = (target − entry) / (entry − stop) — chỉ khi có đủ 3 mốc hợp lệ.
    - current_r = (giá − giá vốn) / (giá vốn − stop) — vị thế đang lời/lỗ bao nhiêu "R"
      so với rủi ro đã chấp nhận. Thiếu mốc nào → bỏ trống, không đoán.
    """
    entry = next((_d(lv.price) for lv in levels if lv.kind == LevelKind.ENTRY), None)
    stop = next((_d(lv.price) for lv in levels if lv.kind == LevelKind.STOP), None)
    targets = sorted(_d(lv.price) for lv in levels if lv.kind == LevelKind.TARGET)

    out: dict = {}
    if entry and stop and targets and entry > stop:
        risk = entry - stop
        out["plan_rr"] = str(((targets[0] - entry) / risk).quantize(Decimal("0.1")))
        if len(targets) > 1:
            out["plan_rr_t2"] = str(((targets[-1] - entry) / risk).quantize(Decimal("0.1")))

    if pnl["net_qty"] > 0 and stop and last_price is not None:
        avg = pnl["avg_cost"]
        if avg > stop:
            out["current_r"] = str(
                ((_d(last_price) - avg) / (avg - stop)).quantize(Decimal("0.01")))
            out["risk_per_share"] = str((avg - stop).quantize(Q))

    return out or None


def thesis_snapshot(thesis: Thesis, last_price: Decimal | None) -> dict:
    """Gói toàn bộ trạng thái 1 luận điểm cho API/dashboard."""
    pnl = position_and_pnl(list(thesis.trades), last_price)
    alerts = check_levels(list(thesis.levels), last_price)
    pillars = [
        {"id": p.id, "text": p.text, "status": p.status.value,
         "is_invalidation": p.is_invalidation, "order": p.order}
        for p in sorted(thesis.pillars, key=lambda x: (x.is_invalidation, x.order))
    ]
    return {
        "id": thesis.id,
        "symbol": thesis.symbol,
        "title": thesis.title,
        "mode": thesis.mode.value,
        "state": thesis.state.value,
        "conviction": thesis.conviction,
        "summary": thesis.summary,
        "pnl": {k: (str(v) if isinstance(v, Decimal) else v) for k, v in pnl.items()},
        "rr": rr_metrics(list(thesis.levels), pnl, last_price),
        "alerts": alerts,
        "pillars": pillars,
        "levels": [
            {"kind": lv.kind.value, "price": str(lv.price), "note": lv.note}
            for lv in thesis.levels
        ],
        "n_trades": len(thesis.trades),
    }


# ---------- Van an toàn SIZE (luật /phan-bo-von) ----------

# Trần tỷ trọng 1 mã theo hạng luận điểm (A ≤15%, B ≤8%, C ≤3% NAV)
CONVICTION_CAP = {"A": Decimal("0.15"), "B": Decimal("0.08"), "C": Decimal("0.03")}


def size_check(nav: Decimal, risk_pct: Decimal, conviction: str,
               qty: int, price: Decimal, pnl: dict,
               stop: Decimal | None) -> dict:
    """Kiểm lệnh MUA trước khi nhận. Trả {ok, violations[], hints{}}.

    Luật 1 — RỦI RO/LỆNH: (giá − stop) × SL mua ≤ nav × risk_pct.
      Không có mốc STOP → không tính được rủi ro → cảnh báo riêng (luận điểm giá trị
      có thể không đặt stop giá, nhưng phải biết mình đang bỏ luật này).
    Luật 2 — TRẦN MÃ THEO HẠNG: giá trị vị thế SAU lệnh ≤ nav × cap(hạng).
    """
    violations: list[str] = []
    hints: dict = {}
    price = _d(price)
    nav = _d(nav)

    # Luật 2 — trần tỷ trọng
    cap = CONVICTION_CAP.get(conviction.upper(), CONVICTION_CAP["C"])
    pos_after = pnl["avg_cost"] * pnl["net_qty"] + price * qty
    cap_value = nav * cap
    hints["cap_pct"] = str((cap * 100).quantize(Decimal("1")))
    hints["max_qty_by_cap"] = int((cap_value - pnl["avg_cost"] * pnl["net_qty"]) / price) \
        if price > 0 else 0
    if pos_after > cap_value:
        violations.append(
            f"Vượt trần hạng {conviction.upper()} ({hints['cap_pct']}% NAV): vị thế sau lệnh "
            f"{pos_after.quantize(Q)} > {cap_value.quantize(Q)} — tối đa còn mua được "
            f"~{max(hints['max_qty_by_cap'], 0)} cp")

    # Luật 1 — rủi ro theo stop
    if stop is not None and price > stop:
        risk = (price - stop) * qty
        budget = nav * risk_pct
        hints["risk_per_share"] = str((price - stop).quantize(Q))
        hints["max_qty_by_risk"] = int(budget / (price - stop))
        if risk > budget:
            violations.append(
                f"Rủi ro lệnh {risk.quantize(Q)} > ngân sách {budget.quantize(Q)} "
                f"({(risk_pct*100).quantize(Decimal('0.1'))}% NAV) — với stop này tối đa "
                f"~{hints['max_qty_by_risk']} cp")
    elif stop is None:
        hints["no_stop"] = ("Luận điểm chưa có mốc STOP — không tính được rủi ro/lệnh. "
                            "Chỉ trần tỷ trọng đang bảo vệ bạn.")

    return {"ok": not violations, "violations": violations, "hints": hints}


# ---------- Equity curve + drawdown + benchmark ----------

def equity_series(snapshots: list, nav: Decimal) -> dict:
    """Chuỗi equity theo ngày + max drawdown + benchmark VN-Index chuẩn hoá.

    drawdown_t = equity_t / max(equity_0..t) − 1. Benchmark chuẩn hoá về NAV gốc
    tại ngày đầu để hai đường so được với nhau ("nếu chỉ mua index thì sao?").
    """
    snaps = sorted(snapshots, key=lambda s: s.date)
    if not snaps:
        return {"series": [], "max_drawdown_pct": "0", "vs_index_pct": None}

    peak = _d(snaps[0].equity)
    max_dd = Decimal("0")
    base_idx = next((_d(s.vnindex) for s in snaps if s.vnindex), None)
    series = []
    for s in snaps:
        eq = _d(s.equity)
        peak = max(peak, eq)
        dd = (eq / peak - 1) * 100 if peak > 0 else Decimal("0")
        max_dd = min(max_dd, dd)
        bench = None
        if base_idx and s.vnindex:
            bench = (_d(snaps[0].equity) * _d(s.vnindex) / base_idx).quantize(Q)
        series.append({"date": s.date, "equity": str(eq.quantize(Q)),
                       "benchmark": (str(bench) if bench is not None else None),
                       "drawdown_pct": str(dd.quantize(Decimal("0.01")))})

    vs_index = None
    if base_idx and snaps[-1].vnindex:
        port_ret = _d(snaps[-1].equity) / _d(snaps[0].equity) - 1
        idx_ret = _d(snaps[-1].vnindex) / base_idx - 1
        vs_index = str(((port_ret - idx_ret) * 100).quantize(Decimal("0.01")))

    return {"series": series,
            "max_drawdown_pct": str(max_dd.quantize(Decimal("0.01"))),
            "vs_index_pct": vs_index}
