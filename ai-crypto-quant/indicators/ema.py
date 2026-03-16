from __future__ import annotations

import pandas as pd
from ta.trend import EMAIndicator


def compute_ema(close: pd.Series, window: int = 20) -> pd.Series:
    return EMAIndicator(close=close, window=window).ema_indicator()
