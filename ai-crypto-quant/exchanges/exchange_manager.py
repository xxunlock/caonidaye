"""Unified exchange manager for multi-exchange collection."""
from __future__ import annotations

import time
from dataclasses import dataclass

from exchanges.binance_client import BinanceClient
from exchanges.bybit_client import BybitClient
from exchanges.okx_client import OkxClient


@dataclass
class ExchangeLatency:
    exchange: str
    endpoint: str
    latency_ms: float


class ExchangeManager:
    def __init__(self, enabled: list[str]):
        mapping = {
            "binance": BinanceClient,
            "okx": OkxClient,
            "bybit": BybitClient,
        }
        self.clients = {name: mapping[name]() for name in enabled if name in mapping}
        self.latency: list[ExchangeLatency] = []

    def _with_latency(self, exchange: str, endpoint: str, fn):
        st = time.perf_counter()
        result = fn()
        elapsed = (time.perf_counter() - st) * 1000
        self.latency.append(ExchangeLatency(exchange, endpoint, elapsed))
        return result

    def fetch_ticker_all(self, symbol: str) -> dict[str, dict]:
        return {
            name: self._with_latency(name, "ticker", lambda c=client: c.fetch_ticker(symbol))
            for name, client in self.clients.items()
        }

    def fetch_ohlcv_all(self, symbol: str, timeframe: str, limit: int = 200) -> dict[str, list]:
        return {
            name: self._with_latency(
                name,
                f"ohlcv:{timeframe}",
                lambda c=client: c.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit),
            )
            for name, client in self.clients.items()
        }

    def fetch_orderbook_all(self, symbol: str, limit: int = 100) -> dict[str, dict]:
        return {
            name: self._with_latency(name, "orderbook", lambda c=client: c.fetch_order_book(symbol, limit=limit))
            for name, client in self.clients.items()
        }

    def fetch_funding_all(self, symbol: str) -> dict[str, dict]:
        return {
            name: self._with_latency(name, "funding", lambda c=client: c.fetch_funding_rate(symbol))
            for name, client in self.clients.items()
        }

    def fetch_open_interest_all(self, symbol: str) -> dict[str, dict]:
        return {
            name: self._with_latency(name, "open_interest", lambda c=client: c.fetch_open_interest(symbol))
            for name, client in self.clients.items()
        }
