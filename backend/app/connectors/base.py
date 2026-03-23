from abc import ABC, abstractmethod
from datetime import datetime, timezone

import httpx

from app.schemas.market import NormalizedTicker, OrderBookLevel


class ExchangeConnector(ABC):
    name: str

    def __init__(self, timeout: float = 8.0) -> None:
        self.client = httpx.AsyncClient(timeout=timeout)

    @abstractmethod
    async def fetch_ticker(self, symbol: str) -> NormalizedTicker:
        raise NotImplementedError

    def normalize_orderbook(self, bids: list[list[float]], asks: list[list[float]]) -> tuple[list[OrderBookLevel], list[OrderBookLevel]]:
        norm_bids = [OrderBookLevel(price=float(p), size=float(s)) for p, s in bids[:10]]
        norm_asks = [OrderBookLevel(price=float(p), size=float(s)) for p, s in asks[:10]]
        return norm_bids, norm_asks

    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    async def close(self) -> None:
        await self.client.aclose()
