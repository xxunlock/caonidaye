from abc import ABC, abstractmethod

from app.schemas.market import IndicatorSnapshot, NormalizedTicker
from app.schemas.strategy import TradeSignal


class StrategyPlugin(ABC):
    name: str

    @abstractmethod
    def generate(self, tick: NormalizedTicker, indicators: IndicatorSnapshot) -> TradeSignal:
        raise NotImplementedError
