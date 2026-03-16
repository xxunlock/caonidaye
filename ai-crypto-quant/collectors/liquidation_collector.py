from __future__ import annotations

from dataclasses import dataclass
from random import random


@dataclass
class LiquidationRow:
    symbol: str
    long_liquidation: float
    short_liquidation: float


class LiquidationCollector:
    """Liquidation data collector.

    In production, bind to exchange liquidation streams (websocket/vendor).
    Here it produces deterministic-like synthetic values when API is unavailable.
    """

    def collect(self, symbol: str) -> LiquidationRow:
        return LiquidationRow(
            symbol=symbol,
            long_liquidation=round(10000 * random(), 2),
            short_liquidation=round(10000 * random(), 2),
        )
