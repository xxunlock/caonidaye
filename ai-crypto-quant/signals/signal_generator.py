from __future__ import annotations

from dataclasses import dataclass

from signals.signal_evaluator import SignalEvaluator


@dataclass
class SignalOutput:
    symbol: str
    signal: str
    confidence: float
    entry_low: float
    entry_high: float
    stop_loss: float
    take_profit: float
    reason: str


class SignalGenerator:
    def __init__(self, evaluator: SignalEvaluator):
        self.evaluator = evaluator

    def generate(self, symbol: str, price: float, long_p: float, short_p: float) -> SignalOutput:
        ev = self.evaluator.evaluate(long_p, short_p)
        entry_low = price * 0.999
        entry_high = price * 1.001

        if ev.signal == "LONG":
            stop_loss = price * 0.98
            take_profit = price * 1.05
        elif ev.signal == "SHORT":
            stop_loss = price * 1.02
            take_profit = price * 0.95
        else:
            stop_loss = price * 0.99
            take_profit = price * 1.01

        return SignalOutput(
            symbol=symbol,
            signal=ev.signal,
            confidence=ev.confidence,
            entry_low=entry_low,
            entry_high=entry_high,
            stop_loss=stop_loss,
            take_profit=take_profit,
            reason=ev.reason,
        )
