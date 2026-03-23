from dataclasses import dataclass

import pandas as pd


@dataclass
class BacktestResult:
    equity_curve: list[float]
    win_rate: float
    max_drawdown: float


class BacktestEngine:
    def run(self, data: pd.DataFrame) -> BacktestResult:
        """
        Expects data columns: close, signal where signal in {-1,0,1}.
        """
        cash = 1.0
        curve = [cash]
        wins = 0
        trades = 0

        for i in range(1, len(data)):
            ret = (data.iloc[i]["close"] - data.iloc[i - 1]["close"]) / data.iloc[i - 1]["close"]
            signal = data.iloc[i - 1]["signal"]
            pnl = ret * signal
            if signal != 0:
                trades += 1
                if pnl > 0:
                    wins += 1
            cash *= (1 + pnl)
            curve.append(cash)

        series = pd.Series(curve)
        drawdown = (series / series.cummax() - 1).min()
        return BacktestResult(
            equity_curve=[round(x, 6) for x in curve],
            win_rate=round(wins / trades, 4) if trades else 0.0,
            max_drawdown=round(abs(float(drawdown)), 4),
        )
