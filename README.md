# 加密量化助手（7x24 市场监控 + AI 分析）

这是一个面向生产的加密货币监控与交易辅助系统模板，覆盖多交易所聚合、技术指标、情绪分析、异常检测、策略信号、风险控制与实时看板。

## 核心能力

- **多交易所聚合**：Binance、OKX、Bybit（价格、深度、成交量、资金费率）
- **统一数据模型**：标准化行情结构，便于策略与风控复用
- **技术指标引擎**：RSI、MACD、EMA(12/26)、布林带、成交量异常
- **AI 情绪模块**：X/新闻数据入口、情绪判断、关键词提取、热币识别
- **异常市场检测**：短时剧烈波动、放量、大额挂单（鲸鱼行为）
- **策略引擎**：输出 LONG / SHORT / HOLD，含入场区间、止损止盈、置信度
- **风控引擎**：风险评分（0-100）、动态仓位、最大回撤约束
- **通知系统**：Telegram、邮件、Web Push 扩展位
- **实时看板**：Next.js + WebSocket
- **回测引擎**：收益曲线、胜率、最大回撤

## 项目结构

```text
backend/
  app/
    api/                 # REST 接口
    backtest/            # 回测
    connectors/          # 交易所连接器
    core/                # 配置与日志
    indicators/          # 指标计算
    notifications/       # 通知分发
    risk/                # 风控
    schemas/             # 统一数据模型
    services/            # 编排、情绪、异常、ws
    strategy/            # 策略插件
  tests/
frontend/
  src/app/
  src/components/
  src/lib/
scripts/start.sh
```

## 快速启动

### 1) 准备环境

- 安装 Docker 与 Docker Compose

### 2) 一键启动

```bash
cp .env.example .env
./scripts/start.sh
```

启动后：

- 后端：`http://localhost:8000`
- 前端：`http://localhost:3000`
- 健康检查：`GET /api/v1/health`
- 行情快照：`GET /api/v1/snapshot`
- 实时推送：`ws://localhost:8000/ws/market`

## 本地开发

### 后端

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## .env 配置说明

请复制 `.env.example` 为 `.env` 后填写：

- `OPENAI_API_KEY`：OpenAI 模型密钥
- `LLM_PROVIDER=openai|qwen|deepseek`：模型供应商
- `LOCAL_LLM_URL`：本地模型服务地址
- Telegram、邮件告警相关账号与密钥

## 扩展指南

### 新增交易所
1. 在 `backend/app/connectors/` 下新增连接器
2. 实现 `ExchangeConnector.fetch_ticker`
3. 注册到 `MarketDataService.connectors`

### 新增策略
1. 在 `backend/app/strategy/` 下实现 `StrategyPlugin`
2. 在 `Orchestrator` 中切换策略实例
3. 使用 `BacktestEngine` 回测验证

### 新增指标
1. 扩展 `IndicatorEngine.update`
2. 在 `IndicatorSnapshot` 增加字段
3. 前端面板增加对应展示

## 说明

- 当前情绪数据接入为可替换模板，默认提供回退样例，便于本地直接跑通。
- 生产环境建议补充：数据库（如 PostgreSQL/ClickHouse）、消息队列、熔断重试、鉴权与限流。
