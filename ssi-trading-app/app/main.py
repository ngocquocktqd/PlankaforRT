"""FastAPI app — API + phục vụ dashboard.

GĐ1 (hiện tại): Data (chỉ đọc) + paper trading + P&L theo luận điểm.
GĐ2 (sau): bật đặt lệnh THẬT qua ssi-sdk (đã chừa chỗ, mặc định TẮT vì an toàn).
"""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlmodel import Session, select

from .config import settings
from .db import get_session, init_db
from .engine import thesis_snapshot
from .importer import import_into_db, parse_thesis_markdown, scan_theses_dir
from .market import market
from .stream import broadcaster
from .models import (
    Level, LevelKind, Pillar, PillarStatus, Side, Thesis, ThesisMode,
    ThesisState, Trade, TradeMode,
)

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="SSI Thesis Trading", version="0.1.0")


@app.on_event("startup")
def _startup() -> None:
    init_db()
    broadcaster.start()


@app.on_event("shutdown")
async def _shutdown() -> None:
    await broadcaster.stop()


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


# ---------- Import luận điểm từ framework markdown ----------

class ImportIn(BaseModel):
    markdown: str
    symbol_hint: str = ""
    dry_run: bool = True   # mặc định chỉ PREVIEW — ghi DB phải chủ động tắt


@app.post("/api/import/markdown")
def import_markdown(body: ImportIn, session: Session = Depends(get_session)) -> dict:
    """Parse 1 file luận điểm markdown (format /theo-doi-luan-diem).

    dry_run=True (mặc định): trả preview những gì sẽ ghi, KHÔNG đụng DB.
    dry_run=False: ghi thật (từ chối nếu mã đã có luận điểm đang mở).
    """
    parsed = parse_thesis_markdown(body.markdown, body.symbol_hint)
    preview = {
        "symbol": parsed.symbol, "title": parsed.title, "mode": parsed.mode,
        "conviction": parsed.conviction, "summary": parsed.summary,
        "pillars": parsed.pillars,
        "levels": [{**lv, "price": str(lv["price"])} for lv in parsed.levels],
        "warnings": parsed.warnings,
    }
    if body.dry_run:
        return {"dry_run": True, "preview": preview}
    result = import_into_db(parsed, session)
    if "error" in result:
        raise HTTPException(status_code=409, detail=result["error"])
    return {"dry_run": False, "imported": result, "preview": preview}


@app.get("/api/import/scan")
def import_scan() -> dict:
    """Liệt kê file luận điểm tìm thấy trong stock-analysis/reports/theses/."""
    files = scan_theses_dir()
    return {"files": [{"name": f.name, "path": str(f),
                       "symbol_hint": f.stem.upper()} for f in files]}


@app.post("/api/import/file/{name}")
def import_file(name: str, dry_run: bool = True,
                session: Session = Depends(get_session)) -> dict:
    """Import 1 file theo tên từ thư mục theses (vd DBC.md)."""
    match = next((f for f in scan_theses_dir() if f.name == name), None)
    if match is None:
        raise HTTPException(status_code=404, detail=f"Không thấy {name} trong theses/")
    body = ImportIn(markdown=match.read_text(encoding="utf-8"),
                    symbol_hint=match.stem, dry_run=dry_run)
    return import_markdown(body, session)


# ---------- Giá ----------

@app.get("/api/quote/{symbol}")
def quote(symbol: str) -> dict:
    return market.quote(symbol)


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    """Đẩy realtime: {type:'quote', prices:{sym:price}} mỗi ~2s + {type:'alert', ...}
    khi giá chạm mốc luận điểm (chống spam: re-arm sau khi giá rời mốc ≥1,5%)."""
    await broadcaster.connect(ws)
    try:
        while True:
            await ws.receive_text()  # giữ kết nối; client không cần gửi gì
    except WebSocketDisconnect:
        broadcaster.disconnect(ws)


# ---------- Frontend ----------

@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND / "index.html")


if (FRONTEND).exists():
    app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
