from __future__ import annotations

import pandas as pd


def compute_volume_profile(df: pd.DataFrame, bins: int = 20) -> pd.DataFrame:
    price_bins = pd.cut(df["close"], bins=bins)
    grouped = df.groupby(price_bins, observed=False)["volume"].sum().reset_index(name="volume_sum")
    grouped["price_range"] = grouped["close"].astype(str)
    return grouped[["price_range", "volume_sum"]]
