from __future__ import annotations


def evaluate_scalping(imbalance: float, spread_bps: float) -> float:
    if spread_bps < 3 and imbalance > 0.2:
        return 1.0
    if spread_bps < 3 and imbalance < -0.2:
        return -1.0
    return 0.0
