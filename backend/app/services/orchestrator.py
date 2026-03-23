import asyncio
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from app.indicators.engine import IndicatorEngine
from app.notifications.dispatcher import NotificationDispatcher
from app.risk.engine import RiskEngine
from app.services.anomaly import AnomalyDetector
from app.services.market_data import MarketDataService
from app.services.sentiment import SentimentService
from app.strategy.momentum import MomentumStrategy


class Orchestrator:
    def __init__(self, symbols: list[str]) -> None:
        self.symbols = symbols
        self.market = MarketDataService()
        self.indicators = IndicatorEngine()
        self.anomaly = AnomalyDetector()
        self.sentiment = SentimentService()
        self.strategy = MomentumStrategy()
        self.risk = RiskEngine()
        self.notify = NotificationDispatcher()
        self.state: dict[str, Any] = defaultdict(dict)

    async def tick(self) -> dict[str, Any]:
        sentiment_state = await self.sentiment.run()
        for symbol in self.symbols:
            ticks = await self.market.fetch_symbol(symbol)
            agg = self.market.aggregate(ticks)
            ind = self.indicators.update(symbol, agg.price, agg.volume_24h)
            sig = self.strategy.generate(agg, ind)
            risk = self.risk.assess(sig)
            alerts = self.anomaly.detect(agg)
            for alert in alerts:
                await self.notify.dispatch_alert(alert)

            self.state[symbol] = {
                "market": agg.model_dump(mode="json"),
                "exchange_ticks": [t.model_dump(mode="json") for t in ticks],
                "indicators": ind.model_dump(mode="json"),
                "signal": sig.model_dump(mode="json"),
                "risk": risk.model_dump(mode="json"),
                "alerts": [a.model_dump(mode="json") for a in alerts],
                "sentiment": {
                    "average_score": sentiment_state["average_score"],
                    "trending": sentiment_state["trending"],
                },
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        return dict(self.state)

    async def close(self) -> None:
        await asyncio.gather(self.market.close(), self.sentiment.close())
