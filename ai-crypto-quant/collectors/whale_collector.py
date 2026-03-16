from __future__ import annotations

from dataclasses import dataclass
from random import choice, random


@dataclass
class WhaleTransfer:
    symbol: str
    amount: float
    side: str
    label: str


class WhaleCollector:
    def __init__(self, btc_threshold: float = 500, eth_threshold: float = 5000):
        self.btc_threshold = btc_threshold
        self.eth_threshold = eth_threshold

    def detect(self, symbol: str) -> list[WhaleTransfer]:
        base = symbol.split("/")[0]
        threshold = self.btc_threshold if base == "BTC" else self.eth_threshold if base == "ETH" else 10000
        amount = threshold * (1 + random())
        transfer = WhaleTransfer(
            symbol=symbol,
            amount=round(amount, 2),
            side=choice(["inflow", "outflow"]),
            label=choice(["exchange inflow", "exchange outflow"]),
        )
        return [transfer] if random() > 0.6 else []
