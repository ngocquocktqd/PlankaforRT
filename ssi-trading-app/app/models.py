"""Mô hình dữ liệu (SQLModel) — trái tim của app là LIÊN KẾT lệnh ↔ luận điểm.

Tiền tệ dùng Decimal (nguyên tắc "no float" của toàn framework). Giá cổ phiếu VN là
đồng (số nguyên) nhưng phí/P&L có thể lẻ → giữ Decimal cho an toàn.

Lưu ý: KHÔNG dùng `from __future__ import annotations` ở file này — nó biến annotation
của Relationship thành chuỗi mà SQLAlchemy không resolve được.
"""
from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


# ---- Enum trạng thái (khớp triết lý framework) ----

class ThesisMode(str, Enum):
    VALUE = "value"        # đầu tư giá trị (hoi-dong-dau-tu)
    MOMENTUM = "momentum"  # lướt sóng (hoi-dong-luot-song)
    CW = "cw"              # chứng quyền


class ThesisState(str, Enum):
    WATCH = "watch"    # theo dõi, chưa vào lệnh
    OPEN = "open"      # đang có vị thế
    CLOSED = "closed"  # đã đóng


class PillarStatus(str, Enum):
    GREEN = "green"    # 🟢 nguyên vẹn
    YELLOW = "yellow"  # 🟡 suy yếu
    RED = "red"        # 🔴 gãy
    NONE = "none"      # ⚪ chưa có dữ liệu mới


class LevelKind(str, Enum):
    ENTRY = "entry"          # điểm vào / pivot
    STOP = "stop"            # cắt lỗ
    TARGET = "target"        # chốt lời
    ACCUMULATE = "accumulate"  # vùng tích luỹ (Tầng 2)
    BUY_HOI = "buy_hoi"      # vùng mua hời (Tầng 3)
    INVALIDATE = "invalidate"  # mốc vô hiệu hoá luận điểm


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class TradeMode(str, Enum):
    PAPER = "paper"
    LIVE = "live"


# ---- Bảng ----

class Thesis(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    title: str
    mode: ThesisMode = ThesisMode.VALUE
    state: ThesisState = ThesisState.WATCH
    conviction: str = "B"           # A/B/C từ hội đồng
    summary: str = ""               # kết luận 1-2 câu
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    pillars: list["Pillar"] = Relationship(back_populates="thesis")
    levels: list["Level"] = Relationship(back_populates="thesis")
    trades: list["Trade"] = Relationship(back_populates="thesis")


class Pillar(SQLModel, table=True):
    """Trụ cột luận điểm hoặc điều kiện vô hiệu hoá — cái được PHÁN XỬ mỗi lần review."""
    id: int | None = Field(default=None, primary_key=True)
    thesis_id: int = Field(foreign_key="thesis.id", index=True)
    text: str
    status: PillarStatus = PillarStatus.NONE
    is_invalidation: bool = False   # True = điều kiện vô hiệu hoá (kích hoạt = cảnh báo đỏ)
    order: int = 0
    thesis: Thesis | None = Relationship(back_populates="pillars")


class Level(SQLModel, table=True):
    """Mốc giá: entry/stop/target/tích luỹ/mua hời/vô hiệu — dùng để canh cảnh báo."""
    id: int | None = Field(default=None, primary_key=True)
    thesis_id: int = Field(foreign_key="thesis.id", index=True)
    kind: LevelKind
    price: Decimal = Field(max_digits=20, decimal_places=4)
    note: str = ""
    thesis: Thesis | None = Relationship(back_populates="levels")


class Trade(SQLModel, table=True):
    """Lệnh khớp — GẮN với một luận điểm. Đây là mối nối cốt lõi của app."""
    id: int | None = Field(default=None, primary_key=True)
    thesis_id: int = Field(foreign_key="thesis.id", index=True)
    symbol: str = Field(index=True)
    side: Side
    quantity: int
    price: Decimal = Field(max_digits=20, decimal_places=4)
    fee: Decimal = Field(default=Decimal("0"), max_digits=20, decimal_places=4)
    mode: TradeMode = TradeMode.PAPER
    order_ref: str = ""             # id lệnh từ SSI (khi live)
    note: str = ""
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    thesis: Thesis | None = Relationship(back_populates="trades")
