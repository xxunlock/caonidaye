from app.connectors.base import ExchangeConnector
from app.schemas.market import NormalizedTicker


class BinanceConnector(ExchangeConnector):
    name = "binance"

    async def fetch_ticker(self, symbol: str) -> NormalizedTicker:
        ticker = await self.client.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}")
        depth = await self.client.get(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=20")
        funding = await self.client.get(f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}")

        t, d, f = ticker.json(), depth.json(), funding.json()
        bids, asks = self.normalize_orderbook(d.get("bids", []), d.get("asks", []))
        return NormalizedTicker(
            exchange=self.name,
            symbol=symbol,
            timestamp=self.now(),
            price=float(t["lastPrice"]),
            volume_24h=float(t["quoteVolume"]),
            funding_rate=float(f.get("lastFundingRate", 0.0)),
            bids=bids,
            asks=asks,
        )
