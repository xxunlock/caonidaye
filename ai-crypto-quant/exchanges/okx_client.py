from __future__ import annotations

import ccxt


class OkxClient:
    def __init__(self):
        self.client = ccxt.okx({"enableRateLimit": True})

    def fetch_ticker(self, symbol: str) -> dict:
        return self.client.fetch_ticker(symbol)

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1m", limit: int = 200):
        return self.client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    def fetch_order_book(self, symbol: str, limit: int = 100):
        return self.client.fetch_order_book(symbol, limit=limit)

    def fetch_funding_rate(self, symbol: str) -> dict:
        return self.client.fetch_funding_rate(symbol)

    def fetch_open_interest(self, symbol: str) -> dict:
        return self.client.fetch_open_interest(symbol)
