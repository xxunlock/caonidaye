from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ai_engine.model_trainer import ModelTrainer, TrainedModels


@dataclass
class Prediction:
    long_probability: float
    short_probability: float


class Predictor:
    def __init__(self, models: TrainedModels):
        self.models = models

    def predict(self, features_row: np.ndarray) -> Prediction:
        long_p, short_p = ModelTrainer.blend_predict(self.models, features_row)
        return Prediction(long_probability=long_p, short_probability=short_p)
