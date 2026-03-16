from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestClassifier

try:
    from xgboost import XGBClassifier
except Exception:  # noqa: BLE001
    XGBClassifier = None


@dataclass
class TrainedModels:
    rf: RandomForestClassifier
    xgb: object | None


class ModelTrainer:
    def train(self, x, y) -> TrainedModels:
        rf = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )
        rf.fit(x, y)

        xgb = None
        if XGBClassifier is not None:
            xgb = XGBClassifier(
                n_estimators=200,
                max_depth=5,
                learning_rate=0.05,
                subsample=0.9,
                colsample_bytree=0.8,
                eval_metric="logloss",
            )
            xgb.fit(x.values, y.values)

        return TrainedModels(rf=rf, xgb=xgb)

    @staticmethod
    def blend_predict(models: TrainedModels, features_row: np.ndarray) -> tuple[float, float]:
        rf_prob = models.rf.predict_proba(features_row)[0, 1]
        probs = [rf_prob]
        if models.xgb is not None:
            xgb_prob = float(models.xgb.predict_proba(features_row)[0, 1])
            probs.append(xgb_prob)
        long_prob = float(sum(probs) / len(probs))
        short_prob = 1 - long_prob
        return long_prob, short_prob
