'use client'

import { useEffect, useState } from 'react'
import SignalCard from '@/components/SignalCard'
import { SymbolState } from '@/lib/types'

export default function HomePage() {
  const [state, setState] = useState<Record<string, SymbolState>>({})

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/market')
    ws.onopen = () => ws.send('subscribe')
    ws.onmessage = (event) => {
      setState(JSON.parse(event.data))
    }
    return () => ws.close()
  }, [])

  return (
    <main style={{ maxWidth: 960, margin: '0 auto', padding: 16 }}>
      <h1>加密货币 24/7 市场监控台</h1>
      <p>多交易所实时监控，结合 AI 信号与风险控制。</p>
      {Object.entries(state).map(([symbol, item]) => (
        <SignalCard key={symbol} symbol={symbol} state={item} />
      ))}
    </main>
  )
}
