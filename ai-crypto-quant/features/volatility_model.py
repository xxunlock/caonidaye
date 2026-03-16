from __future__ import annotations

import pandas as pd


class VolatilityModel:
    def score(self, df: pd.DataFrame) -> float:
        if len(df) < 20:
            return 0.0
        returns = df["close"].pct_change().dropna()
        return float(returns.std() * (252 ** 0.5))
