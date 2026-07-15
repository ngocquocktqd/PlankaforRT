"""Realtime: đẩy giá + cảnh báo mốc luận điểm qua WebSocket.

Kiến trúc GĐ1 (chạy được cả MOCK lẫn LIVE, không phụ thuộc credential):
- Vòng lặp nền tick mỗi TICK_SECONDS: lấy giá mọi mã đang có luận điểm
  (MOCK: giá sóng sin; LIVE: ssi-sdk REST last price) → broadcast {type:"quote"}.
- So giá với Level của từng luận điểm (engine.check_levels) → mốc nào VỪA chạm
  thì broadcast {type:"alert"} — có khoá chống spam: mỗi mốc chỉ báo lại sau khi
  giá rời xa ≥ RE_ARM_PCT.

Nâng cấp LIVE streaming thật (ssi-sdk AsyncStream subscribe_symbol_quote) chừa
sẵn chỗ ở _try_sdk_stream() — best-effort, lỗi thì rơi về polling, không chặn app.
"""
from __future__ import annotations

import asyncio
import contextlib
from decimal import Decimal

from fastapi import WebSocket
from sqlmodel import Session, select

from .db import engine as db_engine
from .engine import check_levels
from .market import market
from .models import Level, Thesis, ThesisState

TICK_SECONDS = 2.0
RE_ARM_PCT = Decimal("0.015")  # giá rời mốc ≥1,5% mới cho báo lại


class Broadcaster:
    def __init__(self) -> None:
        self.clients: set[WebSocket] = set()
        self._armed: dict[int, bool] = {}   # level_id → sẵn sàng bắn alert?
        self._task: asyncio.Task | None = None

    # ---- quản lý client ----
    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.clients.add(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self.clients.discard(ws)

    async def _send_all(self, msg: dict) -> None:
        dead = []
        for ws in self.clients:
            try:
                await ws.send_json(msg)
            except Exception:  # noqa: BLE001 - client rớt thì gỡ, không chặn vòng lặp
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

    # ---- vòng lặp tick ----
    def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    async def _loop(self) -> None:
        while True:
            try:
                if self.clients:  # không ai xem thì không tick (tiết kiệm)
                    await self._tick()
            except Exception:  # noqa: BLE001 - một tick lỗi không được giết vòng lặp
                pass
            await asyncio.sleep(TICK_SECONDS)

    async def _tick(self) -> None:
        # đọc DB trong thread để không chặn event loop
        def _load() -> list[tuple[int, str, list[Level]]]:
            with Session(db_engine) as s:
                theses = s.exec(
                    select(Thesis).where(Thesis.state != ThesisState.CLOSED)
                ).all()
                return [
                    (t.id, t.symbol,
                     s.exec(select(Level).where(Level.thesis_id == t.id)).all())
                    for t in theses
                ]

        rows = await asyncio.to_thread(_load)
        symbols = sorted({sym for _, sym, _ in rows})
        prices: dict[str, Decimal] = {}
        for sym in symbols:
            prices[sym] = await asyncio.to_thread(market.last_price, sym)

        if prices:
            await self._send_all({
                "type": "quote",
                "source": "live" if market.live else "mock",
                "prices": {s: str(p) for s, p in prices.items()},
            })

        # cảnh báo mốc — dùng chung logic engine.check_levels
        for thesis_id, sym, levels in rows:
            price = prices.get(sym)
            if price is None:
                continue
            hit_map = {h["level_id"]: h for h in check_levels(levels, price)}
            for lv in levels:
                armed = self._armed.get(lv.id, True)
                if lv.id in hit_map and armed:
                    self._armed[lv.id] = False  # khoá tới khi giá rời xa
                    h = hit_map[lv.id]
                    await self._send_all({
                        "type": "alert", "thesis_id": thesis_id, "symbol": sym,
                        "level_id": lv.id, "kind": lv.kind.value,
                        "level_price": str(lv.price), "price": str(price),
                        "note": lv.note, "msg": h["msg"],
                    })
                elif lv.id not in hit_map and not armed:
                    # re-arm khi giá rời mốc đủ xa
                    if lv.price and abs(price - lv.price) / lv.price >= RE_ARM_PCT:
                        self._armed[lv.id] = True


broadcaster = Broadcaster()
