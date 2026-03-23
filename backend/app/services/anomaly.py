from collections import deque

from app.core.config import get_settings
from app.schemas.market import MarketAlert, NormalizedTicker


class AnomalyDetector:
    def __init__(self) -> None:
        self.cfg = get_settings()
        self.history: dict[str, deque[NormalizedTicker]] = {}

    def detect(self, tick: NormalizedTicker) -> list[MarketAlert]:
        alerts: list[MarketAlert] = []
        bucket = self.history.setdefault(tick.symbol, deque(maxlen=30))
        bucket.append(tick)
        if len(bucket) < 5:
            return alerts

        first, last = bucket[0], bucket[-1]
        pct_move = ((last.price - first.price) / first.price) * 100
        if abs(pct_move) >= self.cfg.anomaly_price_threshold_pct:
            alerts.append(MarketAlert(
                alert_type="price_move",
                symbol=tick.symbol,
                severity="critical",
                message=f"{tick.symbol} 在短周期内波动 {pct_move:.2f}%",
            ))

        avg_volume = sum(x.volume_24h for x in bucket) / len(bucket)
        if last.volume_24h > avg_volume * self.cfg.anomaly_volume_multiplier:
            alerts.append(MarketAlert(
                alert_type="volume_spike",
                symbol=tick.symbol,
                message=f"成交量异常放大：当前 {last.volume_24h:.2f}，均值 {avg_volume:.2f}",
            ))

        top_bid = max([level.price * level.size for level in tick.bids], default=0.0)
        top_ask = max([level.price * level.size for level in tick.asks], default=0.0)
        if max(top_bid, top_ask) >= self.cfg.whale_order_usd_threshold:
            alerts.append(MarketAlert(
                alert_type="whale_activity",
                symbol=tick.symbol,
                severity="critical",
                message=f"检测到大额挂单，规模约 ${max(top_bid, top_ask):,.0f}",
            ))
        return alerts
