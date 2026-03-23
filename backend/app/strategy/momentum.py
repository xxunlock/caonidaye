from app.schemas.market import IndicatorSnapshot, NormalizedTicker
from app.schemas.strategy import TradeSignal
from app.strategy.base import StrategyPlugin


class MomentumStrategy(StrategyPlugin):
    name = "momentum_v1"

    def generate(self, tick: NormalizedTicker, indicators: IndicatorSnapshot) -> TradeSignal:
        action = "HOLD"
        confidence = 0.5
        reason = "暂无明确交易形态"

        if indicators.rsi and indicators.macd and indicators.macd_signal:
            if indicators.rsi < 35 and indicators.macd > indicators.macd_signal:
                action, confidence, reason = "LONG", 0.75, "RSI超卖 + MACD金叉"
            elif indicators.rsi > 70 and indicators.macd < indicators.macd_signal:
                action, confidence, reason = "SHORT", 0.75, "RSI超买 + MACD死叉"

        px = tick.price
        return TradeSignal(
            symbol=tick.symbol,
            action=action,
            entry_min=px * 0.998,
            entry_max=px * 1.002,
            stop_loss=px * (0.99 if action == "LONG" else 1.01),
            take_profit=px * (1.02 if action == "LONG" else 0.98),
            confidence=confidence,
            reason=reason,
        )
