from __future__ import annotations

from dataclasses import dataclass

from exchanges.exchange_manager import ExchangeManager


@dataclass
class FundingRow:
    exchange: str
    symbol: str
    funding_rate: float


class FundingCollector:
    def __init__(self, manager: ExchangeManager):
        self.manager = manager

    def collect(self, symbol: str) -> list[FundingRow]:
        data = self.manager.fetch_funding_all(symbol)
        return [
            FundingRow(exchange=ex, symbol=symbol, funding_rate=float(row.get("fundingRate") or 0.0))
            for ex, row in data.items()
        ]
