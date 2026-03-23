from app.connectors.base import ExchangeConnector
from app.schemas.market import NormalizedTicker


def _okx_inst(symbol: str) -> str:
    return symbol.replace("USDT", "-USDT-SWAP")


class OKXConnector(ExchangeConnector):
    name = "okx"

    async def fetch_ticker(self, symbol: str) -> NormalizedTicker:
        inst = _okx_inst(symbol)
        ticker = await self.client.get(f"https://www.okx.com/api/v5/market/ticker?instId={inst}")
        depth = await self.client.get(f"https://www.okx.com/api/v5/market/books?instId={inst}&sz=20")
        funding = await self.client.get(f"https://www.okx.com/api/v5/public/funding-rate?instId={inst}")

        t = ticker.json()["data"][0]
        d = depth.json()["data"][0]
        f = funding.json()["data"][0]
        bids, asks = self.normalize_orderbook(d.get("bids", []), d.get("asks", []))

        return NormalizedTicker(
            exchange=self.name,
            symbol=symbol,
            timestamp=self.now(),
            price=float(t["last"]),
            volume_24h=float(t.get("volCcy24h", 0.0)),
            funding_rate=float(f.get("fundingRate", 0.0)),
            bids=bids,
            asks=asks,
        )
