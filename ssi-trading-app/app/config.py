"""Cấu hình app — quyết định chế độ LIVE (có credential SSI) hay MOCK (không có).

Không bao giờ hard-code credential. Nạp từ biến môi trường / .env.
Trading (đặt lệnh thật) mặc định TẮT — phải bật rõ ràng bằng SSI_TRADING_ENABLED=1.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass
class Settings:
    client_id: str = field(default_factory=lambda: os.getenv("SSI_CLIENT_ID", ""))
    api_key: str = field(default_factory=lambda: os.getenv("SSI_API_KEY", ""))
    api_secret: str = field(default_factory=lambda: os.getenv("SSI_API_SECRET", ""))
    private_key: str = field(default_factory=lambda: os.getenv("SSI_PRIVATE_KEY", ""))
    account_no: str = field(default_factory=lambda: os.getenv("SSI_ACCOUNT_NO", ""))
    db_url: str = field(
        default_factory=lambda: os.getenv("DB_URL", f"sqlite:///{BASE_DIR/'data.db'}")
    )
    # An toàn: đặt lệnh THẬT chỉ khi bật cờ này VÀ có đủ credential.
    trading_enabled: bool = field(
        default_factory=lambda: os.getenv("SSI_TRADING_ENABLED", "0") == "1"
    )

    @property
    def has_credentials(self) -> bool:
        return bool(self.client_id and self.api_key and self.api_secret)

    @property
    def mode(self) -> str:
        return "live" if self.has_credentials else "mock"

    @property
    def can_place_live_orders(self) -> bool:
        # Cần: có credential + có private_key (để ký RS256) + account + cờ bật.
        return bool(
            self.has_credentials
            and self.private_key
            and self.account_no
            and self.trading_enabled
        )


settings = Settings()
