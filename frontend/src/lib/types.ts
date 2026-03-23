export interface Signal {
  action: 'LONG' | 'SHORT' | 'HOLD'
  confidence: number
  entry_min: number
  entry_max: number
  stop_loss: number
  take_profit: number
  reason: string
}

export interface SymbolState {
  market: {
    symbol: string
    price: number
    volume_24h: number
    funding_rate: number
  }
  indicators: {
    rsi?: number
    macd?: number
    ema_fast?: number
    ema_slow?: number
    volume_spike: boolean
  }
  signal: Signal
  risk: {
    risk_score: number
    position_size_usd: number
  }
  sentiment: {
    average_score: number
    trending: string[]
  }
}
