from __future__ import annotations

from dataclasses import dataclass

from exchanges.exchange_manager import ExchangeManager


@dataclass
class OrderbookInsight:
    exchange: str
    symbol: str
    bid_ask_imbalance: float
    top_bid_wall: float
    top_ask_wall: float


class OrderbookCollector:
    def __init__(self, manager: ExchangeManager):
        self.manager = manager

    @staticmethod
    def _sum_size(levels: list[list[float]], n: int = 20) -> float:
        return float(sum(level[1] for level in levels[:n])) if levels else 0.0

    def collect(self, symbol: str) -> list[OrderbookInsight]:
        books = self.manager.fetch_orderbook_all(symbol)
        insights: list[OrderbookInsight] = []
        for ex, book in books.items():
            bids = book.get("bids") or []
            asks = book.get("asks") or []
            bid_sum = self._sum_size(bids)
            ask_sum = self._sum_size(asks)
            total = bid_sum + ask_sum
            imbalance = (bid_sum - ask_sum) / total if total else 0.0
            top_bid_wall = max((row[1] for row in bids[:50]), default=0.0)
            top_ask_wall = max((row[1] for row in asks[:50]), default=0.0)
            insights.append(OrderbookInsight(ex, symbol, imbalance, float(top_bid_wall), float(top_ask_wall)))
        return insights
