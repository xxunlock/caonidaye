from collections import deque

import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import BollingerBands

from app.schemas.market import IndicatorSnapshot


class IndicatorEngine:
    """Keeps rolling windows and computes indicators per symbol."""

    def __init__(self, maxlen: int = 300) -> None:
        self.price_history: dict[str, deque[float]] = {}
        self.volume_history: dict[str, deque[float]] = {}
        self.maxlen = maxlen

    def update(self, symbol: str, price: float, volume: float) -> IndicatorSnapshot:
        prices = self.price_history.setdefault(symbol, deque(maxlen=self.maxlen))
        volumes = self.volume_history.setdefault(symbol, deque(maxlen=self.maxlen))
        prices.append(price)
        volumes.append(volume)

        if len(prices) < 35:
            return IndicatorSnapshot(symbol=symbol)

        s = pd.Series(prices, dtype=np.float64)
        v = pd.Series(volumes, dtype=np.float64)

        rsi = RSIIndicator(close=s, window=14).rsi().iloc[-1]
        macd_obj = MACD(close=s, window_fast=12, window_slow=26, window_sign=9)
        macd_val = macd_obj.macd().iloc[-1]
        macd_signal = macd_obj.macd_signal().iloc[-1]
        ema_fast = EMAIndicator(close=s, window=12).ema_indicator().iloc[-1]
        ema_slow = EMAIndicator(close=s, window=26).ema_indicator().iloc[-1]

        bb = BollingerBands(close=s, window=20, window_dev=2)
        bb_upper = bb.bollinger_hband().iloc[-1]
        bb_mid = bb.bollinger_mavg().iloc[-1]
        bb_lower = bb.bollinger_lband().iloc[-1]

        volume_avg = float(v.tail(20).mean())
        volume_spike = bool(v.iloc[-1] > (2.0 * volume_avg))

        return IndicatorSnapshot(
            symbol=symbol,
            rsi=float(rsi),
            macd=float(macd_val),
            macd_signal=float(macd_signal),
            ema_fast=float(ema_fast),
            ema_slow=float(ema_slow),
            bb_upper=float(bb_upper),
            bb_mid=float(bb_mid),
            bb_lower=float(bb_lower),
            volume_spike=volume_spike,
        )
