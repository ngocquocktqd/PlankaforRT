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
