from __future__ import annotations


class DrawdownProtection:
    def __init__(self, max_drawdown: float = 0.2):
        self.max_drawdown = max_drawdown

    def allow(self, drawdown: float) -> bool:
        return drawdown < self.max_drawdown
