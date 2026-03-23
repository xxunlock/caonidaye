import asyncio
from statistics import mean

from app.connectors.binance import BinanceConnector
from app.connectors.bybit import BybitConnector
from app.connectors.okx import OKXConnector
from app.schemas.market import NormalizedTicker


class MarketDataService:
    def __init__(self) -> None:
        self.connectors = [BinanceConnector(), OKXConnector(), BybitConnector()]

    async def fetch_symbol(self, symbol: str) -> list[NormalizedTicker]:
        tasks = [connector.fetch_ticker(symbol) for connector in self.connectors]
        return await asyncio.gather(*tasks, return_exceptions=False)

    @staticmethod
    def aggregate(ticks: list[NormalizedTicker]) -> NormalizedTicker:
        anchor = ticks[0]
        return NormalizedTicker(
            exchange="aggregated",
            symbol=anchor.symbol,
            timestamp=anchor.timestamp,
            price=mean([t.price for t in ticks]),
            volume_24h=mean([t.volume_24h for t in ticks]),
            funding_rate=mean([t.funding_rate or 0.0 for t in ticks]),
            bids=anchor.bids,
            asks=anchor.asks,
        )

    async def close(self) -> None:
        await asyncio.gather(*(c.close() for c in self.connectors))
