from __future__ import annotations


def evaluate_trend(rsi: float, ema_fast: float, ema_slow: float) -> float:
    score = 0.0
    if ema_fast > ema_slow:
        score += 0.5
    if rsi > 55:
        score += 0.5
    return score
