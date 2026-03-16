from __future__ import annotations

from dataclasses import dataclass

from exchanges.exchange_manager import ExchangeManager


@dataclass
class PriceRow:
    exchange: str
    symbol: str
    price: float
    volume: float


class PriceCollector:
    def __init__(self, manager: ExchangeManager):
        self.manager = manager

    def collect(self, symbol: str) -> list[PriceRow]:
        data = self.manager.fetch_ticker_all(symbol)
        rows: list[PriceRow] = []
        for ex, ticker in data.items():
            rows.append(
                PriceRow(
                    exchange=ex,
                    symbol=symbol,
                    price=float(ticker.get("last") or 0.0),
                    volume=float(ticker.get("baseVolume") or 0.0),
                )
            )
        return rows
