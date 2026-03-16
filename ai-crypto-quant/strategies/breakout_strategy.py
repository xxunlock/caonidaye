from __future__ import annotations


def evaluate_breakout(price: float, recent_high: float, recent_low: float) -> float:
    if price > recent_high:
        return 1.0
    if price < recent_low:
        return -1.0
    return 0.0
