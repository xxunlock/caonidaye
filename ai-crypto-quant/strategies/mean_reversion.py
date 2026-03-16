from __future__ import annotations


def evaluate_mean_reversion(price: float, bb_low: float, bb_high: float) -> float:
    if price < bb_low:
        return 1.0
    if price > bb_high:
        return -1.0
    return 0.0
