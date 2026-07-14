"""Nạp dữ liệu mẫu = 2 luận điểm ĐÃ phân tích trong phiên (DBC, PVD) + 1 lệnh paper demo.

Chạy: python -m scripts.seed  (từ thư mục ssi-trading-app)
Đóng vòng lặp: luận điểm từ /hoi-dong-* → cắm vào app → theo dõi P&L thật.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlmodel import Session, select  # noqa: E402

from app.db import engine, init_db  # noqa: E402
from app.models import (  # noqa: E402
    Level, LevelKind, Pillar, PillarStatus, Side, Thesis, ThesisMode,
    ThesisState, Trade, TradeMode,
)


def seed() -> None:
    init_db()
    with Session(engine) as s:
        if s.exec(select(Thesis)).first():
            print("DB đã có dữ liệu — bỏ qua seed.")
            return

        # ---- DBC: giá trị chu kỳ, TRÁNH, chờ đáy chu kỳ ----
        dbc = Thesis(
            symbol="DBC", title="Dabaco — chờ đáy chu kỳ giá heo",
            mode=ThesisMode.VALUE, state=ThesisState.WATCH, conviction="B",
            summary="Cyclical đang định giá lợi nhuận ĐỈNH + Stage 4 + Munger phủ quyết → "
                    "ĐỨNG NGOÀI. Chỉ mua ở đáy chu kỳ ≤12k khi tin ASF/heo chết dày đặc.",
        )
        s.add(dbc); s.commit(); s.refresh(dbc)
        s.add_all([
            Pillar(thesis_id=dbc.id, order=1, status=PillarStatus.GREEN,
                   text="Đầu ngành khối nội + chuỗi 3F chi phí thấp"),
            Pillar(thesis_id=dbc.id, order=2, status=PillarStatus.GREEN,
                   text="Công nghiệp hoá protein thuận dòng 10-20 năm"),
            Pillar(thesis_id=dbc.id, order=3, status=PillarStatus.YELLOW,
                   text="Vắc-xin ASF — KHÔNG phải moat, đừng định giá vào"),
            Pillar(thesis_id=dbc.id, is_invalidation=True, order=1,
                   text="ASF quét trại DBC → lỗ đột biến (39,8% tài sản là đàn heo)"),
            Pillar(thesis_id=dbc.id, is_invalidation=True, order=2,
                   text="CFO âm kéo dài + nợ 5.400 tỷ → pha loãng thêm"),
        ])
        s.add_all([
            Level(thesis_id=dbc.id, kind=LevelKind.ACCUMULATE, price=Decimal("12000"),
                  note="Tích luỹ thăm dò (dưới midpoint nội tại 13.5k)"),
            Level(thesis_id=dbc.id, kind=LevelKind.BUY_HOI, price=Decimal("7000"),
                  note="Mua hời MOS 30% — đáy chu kỳ hoảng loạn"),
        ])

        # ---- PVD: lướt sóng, CHỜ đồ thị bắt kịp cơ bản đã lật ----
        pvd = Thesis(
            symbol="PVD", title="PV Drilling — chờ Stage 2, đừng đuổi pop dầu",
            mode=ThesisMode.MOMENTUM, state=ThesisState.WATCH, conviction="A",
            summary="O'Neil ★4 catalyst BỀN (backlog khoá, LNST Q1 +110%) nhưng Minervini "
                    "Stage 4. Cú tăng trần là pop dầu địa chính trị — CHỜ nền Stage 1→2.",
        )
        s.add(pvd); s.commit(); s.refresh(pvd)
        s.add_all([
            Pillar(thesis_id=pvd.id, order=1, status=PillarStatus.GREEN,
                   text="Catalyst BỀN: giàn IX + backlog kín 2026 + day-rate $90k khoá"),
            Pillar(thesis_id=pvd.id, order=2, status=PillarStatus.GREEN,
                   text="Leader gần độc quyền dịch vụ khoan VN; Dragon Capital mua thêm"),
            Pillar(thesis_id=pvd.id, order=3, status=PillarStatus.RED,
                   text="Kỹ thuật Stage 4 — chưa có nền/pivot, cấm đuổi nến trần"),
            Pillar(thesis_id=pvd.id, is_invalidation=True, order=1,
                   text="Iran hạ nhiệt → Brent xả → giá cổ xả theo (dù earnings khoá)"),
        ])
        s.add_all([
            Level(thesis_id=pvd.id, kind=LevelKind.ENTRY, price=Decimal("20500"),
                  note="Reclaim & giữ trên MA50 → điều kiện đầu để Stage 1→2"),
            Level(thesis_id=pvd.id, kind=LevelKind.STOP, price=Decimal("18000"),
                  note="Dưới vùng đáy gần — chỉ áp khi đã có nền & pivot thật"),
        ])

        # ---- 1 lệnh paper demo trên PVD để thấy P&L chạy ----
        s.add(Trade(thesis_id=pvd.id, symbol="PVD", side=Side.BUY, quantity=1000,
                    price=Decimal("19000"), fee=Decimal("28500"), mode=TradeMode.PAPER,
                    note="Lệnh PAPER demo (không phải khuyến nghị) — test P&L theo luận điểm"))
        pvd.state = ThesisState.OPEN
        s.add(pvd)
        s.commit()
        print("✓ Seeded: DBC (watch) + PVD (open, 1 paper trade).")


if __name__ == "__main__":
    seed()
