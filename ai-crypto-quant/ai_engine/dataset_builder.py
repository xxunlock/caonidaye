from __future__ import annotations

import pandas as pd


class DatasetBuilder:
    feature_cols = [
        "ret_1",
        "ret_5",
        "rsi",
        "macd",
        "macd_diff",
        "atr",
        "funding_rate",
        "open_interest",
        "volume_spike",
        "sentiment_score",
    ]

    def build(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        data = df.copy()
        data["target"] = (data["close"].shift(-3) > data["close"]).astype(int)
        data = data.dropna(subset=self.feature_cols + ["target"])
        x = data[self.feature_cols]
        y = data["target"]
        return x, y
