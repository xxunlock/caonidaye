from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TradeSignal(BaseModel):
    symbol: str
    action: Literal["LONG", "SHORT", "HOLD"]
    entry_min: float
    entry_max: float
    stop_loss: float
    take_profit: float
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class RiskAssessment(BaseModel):
    symbol: str
    risk_score: int = Field(ge=0, le=100)
    position_size_usd: float
    max_drawdown_allowed: float
    notes: str
