from __future__ import annotations

import pandas as pd
from ta.volatility import AverageTrueRange

from indicators.bollinger import compute_bollinger
from indicators.ema import compute_ema
from indicators.macd import compute_macd
from indicators.rsi import compute_rsi
from indicators.vwap import compute_vwap


class FeatureBuilder:
    def build(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["rsi"] = compute_rsi(out["close"])
        macd_df = compute_macd(out["close"])
        out = out.join(macd_df)
        out["ema20"] = compute_ema(out["close"], 20)
        out = out.join(compute_bollinger(out["close"], 20))
        out["vwap"] = compute_vwap(out["high"], out["low"], out["close"], out["volume"], 14)
        atr = AverageTrueRange(high=out["high"], low=out["low"], close=out["close"], window=14)
        out["atr"] = atr.average_true_range()
        out["ret_1"] = out["close"].pct_change(1)
        out["ret_5"] = out["close"].pct_change(5)
        out["volume_spike"] = out["volume"] / out["volume"].rolling(20).mean()
        return out
