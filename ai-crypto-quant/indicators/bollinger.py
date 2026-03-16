from __future__ import annotations

import pandas as pd
from ta.volatility import BollingerBands


def compute_bollinger(close: pd.Series, window: int = 20) -> pd.DataFrame:
    b = BollingerBands(close=close, window=window)
    return pd.DataFrame({
        "bb_high": b.bollinger_hband(),
        "bb_mid": b.bollinger_mavg(),
        "bb_low": b.bollinger_lband(),
    })
