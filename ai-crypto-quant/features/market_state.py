from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarketState:
    trend: str
    volatility: float
    momentum: float


def classify_market_state(rsi: float, macd_diff: float, atr_ratio: float) -> MarketState:
    trend = "bull" if rsi > 55 and macd_diff > 0 else "bear" if rsi < 45 and macd_diff < 0 else "sideways"
    volatility = float(atr_ratio)
    momentum = float(macd_diff)
    return MarketState(trend=trend, volatility=volatility, momentum=momentum)
