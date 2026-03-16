from __future__ import annotations

import numpy as np


def safe_pct_change(new: float, old: float) -> float:
    if old == 0:
        return 0.0
    return (new - old) / old


def zscore(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    arr = np.array(values, dtype=float)
    std = arr.std()
    if std == 0:
        return 0.0
    return float((arr[-1] - arr.mean()) / std)
