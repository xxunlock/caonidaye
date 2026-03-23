from app.connectors.base import ExchangeConnector
from app.schemas.market import NormalizedTicker


class BybitConnector(ExchangeConnector):
    name = "bybit"

    async def fetch_ticker(self, symbol: str) -> NormalizedTicker:
        ticker = await self.client.get(f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={symbol}")
        depth = await self.client.get(f"https://api.bybit.com/v5/market/orderbook?category=linear&symbol={symbol}&limit=20")
        funding = await self.client.get(f"https://api.bybit.com/v5/market/funding/history?category=linear&symbol={symbol}&limit=1")

        t = ticker.json()["result"]["list"][0]
        d = depth.json()["result"]
        f_list = funding.json().get("result", {}).get("list", [])
        last_funding = float(f_list[0]["fundingRate"]) if f_list else 0.0
        bids, asks = self.normalize_orderbook(d.get("b", []), d.get("a", []))

        return NormalizedTicker(
            exchange=self.name,
            symbol=symbol,
            timestamp=self.now(),
            price=float(t["lastPrice"]),
            volume_24h=float(t.get("turnover24h", 0.0)),
            funding_rate=last_funding,
            bids=bids,
            asks=asks,
        )
