from __future__ import annotations


class VolatilityGuard:
    def __init__(self, max_volatility: float = 0.08):
        self.max_volatility = max_volatility

    def is_extreme(self, volatility_score: float) -> bool:
        return volatility_score >= self.max_volatility
