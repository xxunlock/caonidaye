import pandas as pd

from app.backtest.engine import BacktestEngine
from app.indicators.engine import IndicatorEngine


def test_indicator_engine_has_values_after_enough_points() -> None:
    engine = IndicatorEngine()
    out = None
    for i in range(50):
        out = engine.update("BTCUSDT", price=100 + i, volume=1000 + (i * 10))
    assert out is not None
    assert out.rsi is not None
    assert out.macd is not None


def test_backtest_engine_basic() -> None:
    data = pd.DataFrame({
        "close": [100, 102, 101, 105, 108, 107],
        "signal": [0, 1, 1, 0, -1, 0],
    })
    result = BacktestEngine().run(data)
    assert 0 <= result.win_rate <= 1
    assert result.max_drawdown >= 0
    assert len(result.equity_curve) == len(data)
