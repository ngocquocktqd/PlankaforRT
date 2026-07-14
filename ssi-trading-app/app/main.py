"""FastAPI app — API + phục vụ dashboard.

GĐ1 (hiện tại): Data (chỉ đọc) + paper trading + P&L theo luận điểm.
GĐ2 (sau): bật đặt lệnh THẬT qua ssi-sdk (đã chừa chỗ, mặc định TẮT vì an toàn).
"""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlmodel import Session, select

from .config import settings
from .db import get_session, init_db
from .engine import thesis_snapshot
from .market import market
from .models import (
    Level, LevelKind, Pillar, PillarStatus, Side, Thesis, ThesisMode,
    ThesisState, Trade, TradeMode,
)

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="SSI Thesis Trading", version="0.1.0")


@app.on_event("startup")
def _startup() -> None:
    init_db()


# ---------- Schemas vào ----------

class ThesisIn(BaseModel):
    symbol: str
    title: str
    mode: ThesisMode = ThesisMode.VALUE
    conviction: str = "B"
    summary: str = ""


class TradeIn(BaseModel):
    side: Side
    quantity: int
    price: Decimal
    fee: Decimal = Decimal("0")
    note: str = ""


class PillarPatch(BaseModel):
    status: PillarStatus


# ---------- Meta ----------

@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "mode": settings.mode,                       # mock | live
        "market_live": market.live,
        "trading_live_enabled": settings.can_place_live_orders,
        "account_no": settings.account_no or None,
    }


# ---------- Luận điểm ----------

@app.get("/api/theses")
def list_theses(session: Session = Depends(get_session)) -> list[dict]:
    theses = session.exec(select(Thesis)).all()
    out = []
    for th in theses:
        lp = market.last_price(th.symbol)
        out.append(thesis_snapshot(th, lp))
    # sắp: đang mở trước, rồi theo dõi, rồi đóng
    order = {ThesisState.OPEN: 0, ThesisState.WATCH: 1, ThesisState.CLOSED: 2}
    return sorted(out, key=lambda x: order.get(ThesisState(x["state"]), 9))


@app.post("/api/theses")
def create_thesis(body: ThesisIn, session: Session = Depends(get_session)) -> dict:
    th = Thesis(symbol=body.symbol.upper(), title=body.title, mode=body.mode,
                conviction=body.conviction, summary=body.summary)
    session.add(th)
    session.commit()
    session.refresh(th)
    return thesis_snapshot(th, market.last_price(th.symbol))


@app.get("/api/theses/{thesis_id}")
def get_thesis(thesis_id: int, session: Session = Depends(get_session)) -> dict:
    th = session.get(Thesis, thesis_id)
    if not th:
        raise HTTPException(404, "Không tìm thấy luận điểm")
    snap = thesis_snapshot(th, market.last_price(th.symbol))
    snap["trades"] = [
        {"id": t.id, "side": t.side.value, "quantity": t.quantity, "price": str(t.price),
         "fee": str(t.fee), "mode": t.mode.value, "note": t.note,
         "executed_at": t.executed_at.isoformat()}
        for t in sorted(th.trades, key=lambda x: x.executed_at)
    ]
    return snap


@app.patch("/api/theses/{thesis_id}/pillars/{pillar_id}")
def update_pillar(thesis_id: int, pillar_id: int, body: PillarPatch,
                  session: Session = Depends(get_session)) -> dict:
    p = session.get(Pillar, pillar_id)
    if not p or p.thesis_id != thesis_id:
        raise HTTPException(404, "Không tìm thấy trụ cột")
    p.status = body.status
    session.add(p)
    session.commit()
    return {"id": p.id, "status": p.status.value}


# ---------- Lệnh (paper; live để GĐ2) ----------

@app.post("/api/theses/{thesis_id}/trades")
def add_trade(thesis_id: int, body: TradeIn,
              session: Session = Depends(get_session)) -> dict:
    th = session.get(Thesis, thesis_id)
    if not th:
        raise HTTPException(404, "Không tìm thấy luận điểm")
    if body.quantity <= 0 or body.price <= 0:
        raise HTTPException(400, "Số lượng và giá phải > 0")

    # GĐ1: luôn paper. GĐ2 sẽ gọi ssi-sdk place_*_order khi can_place_live_orders.
    trade = Trade(thesis_id=thesis_id, symbol=th.symbol, side=body.side,
                  quantity=body.quantity, price=body.price, fee=body.fee,
                  mode=TradeMode.PAPER, note=body.note)
    session.add(trade)
    # mở luận điểm nếu đây là lệnh mua đầu tiên
    if th.state == ThesisState.WATCH and body.side == Side.BUY:
        th.state = ThesisState.OPEN
        session.add(th)
    session.commit()
    session.refresh(th)
    return thesis_snapshot(th, market.last_price(th.symbol))


# ---------- Giá ----------

@app.get("/api/quote/{symbol}")
def quote(symbol: str) -> dict:
    return market.quote(symbol)


# ---------- Frontend ----------

@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND / "index.html")


if (FRONTEND).exists():
    app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
