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
        "alerts": alerts,
        "pillars": pillars,
        "levels": [
            {"kind": lv.kind.value, "price": str(lv.price), "note": lv.note}
            for lv in thesis.levels
        ],
        "n_trades": len(thesis.trades),
    }
