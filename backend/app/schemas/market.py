from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class OrderBookLevel(BaseModel):
    price: float
    size: float


class NormalizedTicker(BaseModel):
    exchange: str
    symbol: str
    timestamp: datetime
    price: float
    volume_24h: float
    funding_rate: float | None = None
    bids: list[OrderBookLevel] = Field(default_factory=list)
    asks: list[OrderBookLevel] = Field(default_factory=list)


class IndicatorSnapshot(BaseModel):
    symbol: str
    rsi: float | None = None
    macd: float | None = None
    macd_signal: float | None = None
    ema_fast: float | None = None
    ema_slow: float | None = None
    bb_upper: float | None = None
    bb_mid: float | None = None
    bb_lower: float | None = None
    volume_spike: bool = False


class SentimentItem(BaseModel):
    source: Literal["twitter", "news"]
    text: str
    score: float
    label: Literal["bullish", "bearish", "neutral"]
    keywords: list[str] = Field(default_factory=list)


class MarketAlert(BaseModel):
    alert_type: str
    symbol: str
    message: str
    severity: Literal["info", "warning", "critical"] = "warning"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
