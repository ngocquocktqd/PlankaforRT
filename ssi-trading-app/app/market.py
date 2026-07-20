"""Nguồn giá — LIVE qua ssi-sdk khi có credential, MOCK khi không.

MOCK tạo giá tất định theo mã (hash) + bước đi ngẫu nhiên nhẹ theo thời gian, để dashboard
"sống" mà không cần credential. Đổi sang LIVE chỉ cần cắm biến môi trường SSI_*.
"""
from __future__ import annotations

import hashlib
import math
import time
from decimal import Decimal

from .config import settings

# Giá tham chiếu mồi cho MOCK (đồng) — vài mã đã phân tích trong phiên, số xấp xỉ thực.
_SEED_PRICES: dict[str, int] = {
    "VNINDEX": 1787,  # benchmark cho equity curve
    "DBC": 17850, "PVD": 19900, "SSI": 25850, "VHM": 151600, "CTG": 34250,
    "MWG": 78000, "FRT": 117000, "PVS": 38000, "BSR": 21000, "VNM": 61000,
    "FPT": 95000, "HPG": 26000, "VCB": 62000, "MBB": 24000, "VPB": 27800,
}


def _mock_price(symbol: str) -> Decimal:
    base = _SEED_PRICES.get(symbol.upper())
    if base is None:
        h = int(hashlib.sha256(symbol.upper().encode()).hexdigest(), 16)
        base = 10000 + h % 90000
    # dao động ±1.5% theo sóng sin chậm (chu kỳ ~2 phút) để nhìn có nhịp
    drift = math.sin(time.time() / 20 + (len(symbol) * 1.3)) * 0.015
    price = Decimal(base) * (Decimal(1) + Decimal(str(round(drift, 5))))
    # làm tròn về bước giá thô (10đ) cho giống bảng giá VN
    return (price / 10).quantize(Decimal(1)) * 10


class MarketData:
    """Wrapper giá. Lazy-init SDK; nếu lỗi/không cred → tự rơi về MOCK."""

    def __init__(self) -> None:
        self._data = None
        self._auth = None
        if settings.has_credentials:
            try:
                from ssi_sdk import Auth, Config, Data  # type: ignore

                cfg = Config(
                    client_id=settings.client_id,
                    api_key=settings.api_key,
                    api_secret=settings.api_secret,
                    private_key=settings.private_key,
                )
                self._auth = Auth(cfg)
                self._data = Data(self._auth)
            except Exception:  # noqa: BLE001 - không có mạng/sai cred → dùng mock
                self._data = None

    @property
    def live(self) -> bool:
        return self._data is not None

    def last_price(self, symbol: str) -> Decimal:
        if self._data is not None:
            try:
                bars = self._data.get_ohlc_1day(symbol.upper())
                if bars:
                    return Decimal(str(bars[-1].close_price))
            except Exception:  # noqa: BLE001 - lỗi live → fallback mock, không chặn app
                pass
        return _mock_price(symbol)

    def quote(self, symbol: str) -> dict:
        p = self.last_price(symbol)
        return {"symbol": symbol.upper(), "price": str(p), "source": "live" if self.live else "mock"}


market = MarketData()
