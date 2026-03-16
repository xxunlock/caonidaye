"""Main startup for AI crypto quant monitoring and signal generation platform."""
from __future__ import annotations

import asyncio
import threading
import time
from pathlib import Path

import numpy as np
import pandas as pd
import uvicorn

from ai_engine.dataset_builder import DatasetBuilder
from ai_engine.model_trainer import ModelTrainer, TrainedModels
from ai_engine.predictor import Predictor
from alerts.notifier import AlertMessage, Notifier
from collectors.funding_collector import FundingCollector
from collectors.liquidation_collector import LiquidationCollector
from collectors.orderbook_collector import OrderbookCollector
from collectors.price_collector import PriceCollector
from collectors.whale_collector import WhaleCollector
from core.database import DB, MarketSnapshot, TradingSignal
from core.logger import setup_logger
from core.settings import Settings
from dashboard.api_server import DashboardAPI
from exchanges.exchange_manager import ExchangeManager
from features.feature_builder import FeatureBuilder
from features.volatility_model import VolatilityModel
from risk.risk_manager import RiskManager
from scheduler.job_scheduler import JobScheduler
from sentiment.sentiment_model import SentimentModel
from signals.signal_evaluator import SignalEvaluator
from signals.signal_generator import SignalGenerator


class Application:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.settings = Settings.from_yaml(config_path)
        self.logger = setup_logger(level=self.settings.get("app.log_level", "INFO"))
        self.db = DB(self.settings.get("database.url", "sqlite:///./ai_crypto_quant.db"))
        self.db.init()

        enabled_exchanges = self.settings.get("exchanges.enabled", ["binance"])
        self.symbols = self.settings.get("exchanges.symbols", ["BTC/USDT"])
        self.timeframes = self.settings.get("exchanges.timeframes", ["1m", "5m", "15m", "1h"])
        self.ohlcv_limit = int(self.settings.get("exchanges.ohlcv_limit", 200))

        self.exchange_manager = ExchangeManager(enabled_exchanges)
        self.price_collector = PriceCollector(self.exchange_manager)
        self.orderbook_collector = OrderbookCollector(self.exchange_manager)
        self.funding_collector = FundingCollector(self.exchange_manager)
        self.liquidation_collector = LiquidationCollector()
        self.whale_collector = WhaleCollector(
            btc_threshold=float(self.settings.get("thresholds.whale_btc", 500)),
            eth_threshold=float(self.settings.get("thresholds.whale_eth", 5000)),
        )
        self.feature_builder = FeatureBuilder()
        self.dataset_builder = DatasetBuilder()
        self.model_trainer = ModelTrainer()
        self.models: TrainedModels | None = None
        self.predictor: Predictor | None = None
        self.sentiment = SentimentModel()
        self.signal_generator = SignalGenerator(
            SignalEvaluator(
                long_threshold=float(self.settings.get("thresholds.long_prob", 0.65)),
                short_threshold=float(self.settings.get("thresholds.short_prob", 0.65)),
            )
        )
        self.risk_manager = RiskManager()
        self.volatility_model = VolatilityModel()
        self.notifier = Notifier(telegram_enabled=False)

        self.state: dict = {
            "signals": [],
            "market": {},
            "orderbook": {},
            "liquidations": {},
            "sentiment": {},
            "whales": {},
        }

        self.scheduler = JobScheduler()

    def _build_ohlcv_df(self, symbol: str) -> pd.DataFrame:
        # Select first exchange feed as canonical for modeling.
        ohlcv_data = self.exchange_manager.fetch_ohlcv_all(symbol, timeframe="1m", limit=self.ohlcv_limit)
        if not ohlcv_data:
            raise RuntimeError("No OHLCV data collected")
        first = next(iter(ohlcv_data.values()))
        df = pd.DataFrame(first, columns=["ts", "open", "high", "low", "close", "volume"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms")
        return df

    def collect_price_job(self) -> None:
        self.logger.info("Running price collector")
        for symbol in self.symbols:
            rows = self.price_collector.collect(symbol)
            funding = self.funding_collector.collect(symbol)
            funding_map = {r.exchange: r.funding_rate for r in funding}
            oi_data = self.exchange_manager.fetch_open_interest_all(symbol)
            with self.db.session() as sess:
                for row in rows:
                    snap = MarketSnapshot(
                        exchange=row.exchange,
                        symbol=row.symbol,
                        price=row.price,
                        volume=row.volume,
                        funding_rate=funding_map.get(row.exchange, 0.0),
                        open_interest=float((oi_data.get(row.exchange) or {}).get("openInterestValue") or 0.0),
                    )
                    sess.add(snap)
                sess.commit()
            self.state["market"][symbol] = [r.__dict__ for r in rows]

    def indicators_job(self) -> None:
        self.logger.info("Running indicator + anomaly engine")
        for symbol in self.symbols:
            df = self._build_ohlcv_df(symbol)
            feat = self.feature_builder.build(df)
            latest = feat.iloc[-1].to_dict()

            # anomaly detection
            price_change_5m = float(latest.get("ret_5") or 0.0)
            volume_spike = float(latest.get("volume_spike") or 0.0)
            anomalies = {
                "price_change_gt_3pct": abs(price_change_5m) > 0.03,
                "volume_spike": volume_spike > 2.5,
            }
            self.state["market"][f"{symbol}_indicators"] = latest
            self.state["market"][f"{symbol}_anomalies"] = anomalies

            # orderbook analysis
            ob = self.orderbook_collector.collect(symbol)
            self.state["orderbook"][symbol] = [x.__dict__ for x in ob]

            # liquidation & whales
            liq = self.liquidation_collector.collect(symbol)
            self.state["liquidations"][symbol] = liq.__dict__
            whales = self.whale_collector.detect(symbol)
            self.state["whales"][symbol] = [w.__dict__ for w in whales]

            # sentiment
            sentiment_score = self.sentiment.aggregate(symbol)
            self.state["sentiment"][symbol] = {"score": sentiment_score}

    def prediction_job(self) -> None:
        self.logger.info("Running AI prediction")
        for symbol in self.symbols:
            df = self._build_ohlcv_df(symbol)
            feat = self.feature_builder.build(df)
            feat["funding_rate"] = 0.0
            feat["open_interest"] = 0.0
            feat["sentiment_score"] = self.state["sentiment"].get(symbol, {}).get("score", 0.0)

            x, y = self.dataset_builder.build(feat)
            if len(x) < 30:
                self.logger.warning("Insufficient training data for %s", symbol)
                continue

            self.models = self.model_trainer.train(x, y)
            self.predictor = Predictor(self.models)
            row = x.iloc[-1].to_numpy(dtype=float).reshape(1, -1)
            pred = self.predictor.predict(np.array(row))
            self.state["market"][f"{symbol}_prediction"] = pred.__dict__

    def signal_job(self) -> None:
        self.logger.info("Running signal engine")
        for symbol in self.symbols:
            market_rows = self.state["market"].get(symbol, [])
            if not market_rows:
                continue
            price = float(market_rows[0].get("price", 0.0))
            pred = self.state["market"].get(f"{symbol}_prediction", {})
            long_p = float(pred.get("long_probability", 0.5))
            short_p = float(pred.get("short_probability", 0.5))

            # risk gate
            try:
                df = self._build_ohlcv_df(symbol)
                vol_score = self.volatility_model.score(df)
            except Exception:
                vol_score = 0.0
            decision = self.risk_manager.evaluate(volatility_score=vol_score, drawdown=0.05)
            if not decision.allowed:
                self.logger.warning("Signal blocked for %s: %s", symbol, decision.reason)
                continue

            signal = self.signal_generator.generate(symbol, price, long_p, short_p)
            self.state["signals"].append(signal.__dict__)

            with self.db.session() as sess:
                sess.add(
                    TradingSignal(
                        symbol=signal.symbol,
                        signal=signal.signal,
                        confidence=signal.confidence,
                        entry_low=signal.entry_low,
                        entry_high=signal.entry_high,
                        stop_loss=signal.stop_loss,
                        take_profit=signal.take_profit,
                        reason=signal.reason,
                    )
                )
                sess.commit()

            msg = AlertMessage(
                symbol=signal.symbol.replace("/", ""),
                signal=signal.signal,
                confidence=signal.confidence,
                entry_low=signal.entry_low,
                entry_high=signal.entry_high,
                stop_loss=signal.stop_loss,
                take_profit=signal.take_profit,
            )
            asyncio.run(self.notifier.notify(msg))

    def setup_jobs(self) -> None:
        self.scheduler.add_interval_job(
            self.collect_price_job,
            seconds=int(self.settings.get("scheduler.price_seconds", 10)),
            id="price_collector",
        )
        self.scheduler.add_interval_job(
            self.indicators_job,
            minutes=int(self.settings.get("scheduler.indicator_minutes", 1)),
            id="indicators",
        )
        self.scheduler.add_interval_job(
            self.prediction_job,
            minutes=int(self.settings.get("scheduler.prediction_minutes", 5)),
            id="prediction",
        )
        self.scheduler.add_interval_job(
            self.signal_job,
            minutes=int(self.settings.get("scheduler.signal_minutes", 10)),
            id="signal",
        )

    def start(self) -> None:
        self.setup_jobs()
        self.scheduler.start()
        self.logger.info("Scheduler started")

        api = DashboardAPI(self.state)

        def run_api():
            uvicorn.run(api.app, host="0.0.0.0", port=8000, log_level="info")

        thread = threading.Thread(target=run_api, daemon=True)
        thread.start()
        self.logger.info("API server started on 0.0.0.0:8000")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.scheduler.shutdown()
            self.logger.info("Application stopped")


if __name__ == "__main__":
    cfg = Path(__file__).parent / "config" / "config.yaml"
    app = Application(str(cfg))
    app.start()
