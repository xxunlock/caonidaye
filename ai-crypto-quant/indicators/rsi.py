from __future__ import annotations

import pandas as pd
from ta.momentum import RSIIndicator


def compute_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    return RSIIndicator(close=close, window=window).rsi()
