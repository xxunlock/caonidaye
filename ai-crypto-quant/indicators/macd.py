from __future__ import annotations

import pandas as pd
from ta.trend import MACD


def compute_macd(close: pd.Series) -> pd.DataFrame:
    m = MACD(close=close)
    return pd.DataFrame({
        "macd": m.macd(),
        "macd_signal": m.macd_signal(),
        "macd_diff": m.macd_diff(),
    })
