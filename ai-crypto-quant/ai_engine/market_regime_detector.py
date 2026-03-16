from __future__ import annotations

import pandas as pd


class MarketRegimeDetector:
    def detect(self, df: pd.DataFrame) -> str:
        if len(df) < 50:
            return "unknown"
        ma_fast = df["close"].rolling(20).mean().iloc[-1]
        ma_slow = df["close"].rolling(50).mean().iloc[-1]
        vol = df["close"].pct_change().rolling(20).std().iloc[-1]

        if ma_fast > ma_slow and vol < 0.04:
            return "trending_up"
        if ma_fast < ma_slow and vol < 0.04:
            return "trending_down"
        if vol >= 0.04:
            return "high_volatility"
        return "range"
