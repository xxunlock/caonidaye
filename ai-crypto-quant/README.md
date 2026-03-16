# AI Crypto Quant

Production-grade modular crypto market monitoring and signal platform (analysis-only, **no auto trade execution**).

## Features

- Multi-exchange collection via CCXT (Binance, OKX, Bybit)
- 24/7 scheduler-driven data pipelines
- Market data, orderbook, funding, open-interest, liquidation, whale monitoring
- Technical indicators (RSI, MACD, EMA, Bollinger, VWAP, ATR, volume profile)
- AI engine with RandomForest + XGBoost blending
- Signal generation and risk gating
- Telegram alerting format
- FastAPI dashboard endpoints

## Structure

See directories under `ai-crypto-quant/`:

- `core`, `exchanges`, `collectors`, `indicators`, `features`, `ai_engine`, `strategies`, `risk`, `sentiment`, `signals`, `alerts`, `scheduler`, `dashboard`, `utils`

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ai-crypto-quant/main.py
```

API:

- `GET /signals`
- `GET /market`
- `GET /orderbook`
- `GET /liquidations`
- `GET /sentiment`
- `GET /whales`
