from collections import Counter
from typing import Iterable

import httpx
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.schemas.market import SentimentItem


class SentimentService:
    def __init__(self) -> None:
        self.cfg = get_settings()
        self.client = httpx.AsyncClient(timeout=10)
        self.openai = AsyncOpenAI(api_key=self.cfg.openai_api_key) if self.cfg.openai_api_key else None

    async def fetch_news(self) -> list[str]:
        # Optional integration point: replace endpoint with a provider like CryptoPanic.
        return [
            "比特币ETF连续第三天净流入",
            "以太坊二层活跃度回落，Gas费用趋稳",
        ]

    async def fetch_x_posts(self) -> list[str]:
        # Integrate X API or third-party indexers here.
        return [
            "$BTC 在 8 万上方表现强势，资金费率健康",
            "巨鲸资金正从 meme 币轮动到主流币",
        ]

    async def analyze_text(self, source: str, text: str) -> SentimentItem:
        lower = text.lower()
        score = 0.0
        for token in ("strong", "rise", "inflow", "bull", "breakout"):
            if token in lower:
                score += 0.2
        for token in ("dump", "hack", "bear", "risk", "selloff"):
            if token in lower:
                score -= 0.2

        label = "neutral"
        if score > 0.1:
            label = "bullish"
        elif score < -0.1:
            label = "bearish"

        keywords = [w.strip("$.,") for w in text.split() if w.startswith("$") or w.lower() in {"bitcoin", "ethereum", "solana"}]
        return SentimentItem(source=source, text=text, score=score, label=label, keywords=keywords)

    async def run(self) -> dict[str, object]:
        raw = [("news", x) for x in await self.fetch_news()] + [("twitter", x) for x in await self.fetch_x_posts()]
        items = [await self.analyze_text(src, txt) for src, txt in raw]

        keyword_counter = Counter(k for item in items for k in item.keywords)
        trending = [coin for coin, _ in keyword_counter.most_common(5)]
        avg_score = sum(i.score for i in items) / max(1, len(items))
        return {
            "items": items,
            "average_score": avg_score,
            "trending": trending,
        }

    async def close(self) -> None:
        await self.client.aclose()
