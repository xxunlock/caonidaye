from app.schemas.strategy import RiskAssessment, TradeSignal


class RiskEngine:
    def __init__(self, max_drawdown: float = 0.15, account_size_usd: float = 100_000.0) -> None:
        self.max_drawdown = max_drawdown
        self.account_size_usd = account_size_usd

    def assess(self, signal: TradeSignal, volatility_estimate: float = 0.02) -> RiskAssessment:
        base_risk = min(100, int(volatility_estimate * 2000))
        confidence_adj = int((1 - signal.confidence) * 40)
        risk_score = min(100, max(0, base_risk + confidence_adj))

        risk_per_trade = max(0.005, 0.02 - risk_score / 10000)
        position_size = self.account_size_usd * risk_per_trade

        return RiskAssessment(
            symbol=signal.symbol,
            risk_score=risk_score,
            position_size_usd=round(position_size, 2),
            max_drawdown_allowed=self.max_drawdown,
            notes=f"Dynamic sizing using confidence={signal.confidence:.2f}",
        )
