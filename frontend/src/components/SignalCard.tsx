import { SymbolState } from '@/lib/types'

export default function SignalCard({ symbol, state }: { symbol: string; state: SymbolState }) {
  return (
    <div style={{ border: '1px solid #333', borderRadius: 8, padding: 12, marginBottom: 12 }}>
      <h3>{symbol}</h3>
      <p>价格：{state.market.price.toFixed(2)}</p>
      <p>信号：<b>{state.signal.action}</b>（{(state.signal.confidence * 100).toFixed(0)}%）</p>
      <p>入场区间：{state.signal.entry_min.toFixed(2)} - {state.signal.entry_max.toFixed(2)}</p>
      <p>止损 / 止盈：{state.signal.stop_loss.toFixed(2)} / {state.signal.take_profit.toFixed(2)}</p>
      <p>RSI：{state.indicators.rsi?.toFixed(2) ?? '暂无'} | MACD：{state.indicators.macd?.toFixed(4) ?? '暂无'}</p>
      <p>风险分：{state.risk.risk_score} | 建议仓位：${state.risk.position_size_usd}</p>
      <p>热词趋势：{state.sentiment.trending.join(', ') || '暂无'}</p>
    </div>
  )
}
