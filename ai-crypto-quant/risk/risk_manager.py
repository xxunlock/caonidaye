from __future__ import annotations

from dataclasses import dataclass

from risk.drawdown_protection import DrawdownProtection
from risk.volatility_guard import VolatilityGuard


@dataclass
class RiskDecision:
    allowed: bool
    risk_level: str
    reason: str


class RiskManager:
    def __init__(self):
        self.vol_guard = VolatilityGuard()
        self.dd_guard = DrawdownProtection()

    def evaluate(self, volatility_score: float, drawdown: float) -> RiskDecision:
        if self.vol_guard.is_extreme(volatility_score):
            return RiskDecision(False, "extreme", "volatility guard blocked")
        if not self.dd_guard.allow(drawdown):
            return RiskDecision(False, "high", "drawdown protection blocked")
        level = "low" if volatility_score < 0.03 else "medium"
        return RiskDecision(True, level, "risk acceptable")
