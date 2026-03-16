from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvaluatedSignal:
    signal: str
    confidence: float
    reason: str


class SignalEvaluator:
    def __init__(self, long_threshold: float = 0.65, short_threshold: float = 0.65):
        self.long_threshold = long_threshold
        self.short_threshold = short_threshold

    def evaluate(self, long_p: float, short_p: float) -> EvaluatedSignal:
        if long_p > self.long_threshold:
            return EvaluatedSignal("LONG", long_p, "long probability above threshold")
        if short_p > self.short_threshold:
            return EvaluatedSignal("SHORT", short_p, "short probability above threshold")
        return EvaluatedSignal("WAIT", max(long_p, short_p), "no edge")
