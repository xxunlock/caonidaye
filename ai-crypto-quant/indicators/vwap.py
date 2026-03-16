from __future__ import annotations

import pandas as pd
from ta.volume import VolumeWeightedAveragePrice


def compute_vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int = 14) -> pd.Series:
    return VolumeWeightedAveragePrice(high=high, low=low, close=close, volume=volume, window=window).volume_weighted_average_price()
