"""Kết nối DB (SQLite mặc định) + session helper."""
from __future__ import annotations

from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from .config import settings

# check_same_thread=False để FastAPI (đa luồng) dùng chung engine SQLite an toàn.
engine = create_engine(
    settings.db_url,
    echo=False,
    connect_args={"check_same_thread": False} if settings.db_url.startswith("sqlite") else {},
)


def init_db() -> None:
    # import models để SQLModel biết bảng trước khi create_all
    from . import models  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
