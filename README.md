# 24小时虚拟货币盯盘工具

这是一个可长期运行（24/7）的轻量级盯盘程序，支持同时接入多个主流交易所 API，实时拉取币价并输出汇总结果。

## 功能

- 支持多交易所并发拉取行情：
  - Binance
  - Coinbase
  - OKX
  - Kraken
- 可配置监控交易对（如 `BTCUSDT`、`ETHUSDT`）
- 统一价格格式（自动将 `USDC`、`USD` 等映射为 `USDT` 以便横向对比）
- 输出每个交易对的：
  - 各交易所最新价格
  - 最低价 / 最高价
  - 简单价差百分比（可用于发现基础套利机会）
- 支持阈值告警（价差超过指定百分比会打印 `ALERT`）

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py --config config.example.json
```

## 配置说明

配置文件使用 JSON，示例见 `config.example.json`：

- `symbols`: 监控交易对列表（统一使用 `USDT` 结尾）
- `exchanges`: 要启用的交易所
- `interval_seconds`: 拉取间隔（秒）
- `alert_spread_percent`: 触发告警的价差阈值（%）

## 运行示例

```bash
python app.py --config config.example.json
```

输出示意：

```text
[2026-01-01 10:00:00] BTCUSDT -> BINANCE:43123.11 | COINBASE:43121.44 | OKX:43124.01 | KRAKEN:43120.98 | low=43120.98 high=43124.01 spread=0.0070%
```

## 注意事项

- 该项目仅用于行情监控与学习，不构成投资建议。
- 各交易所 API 可能存在限频策略，请根据实际情况调大轮询间隔。
- 生产环境建议配合 `systemd` / `supervisor` / Docker 做进程守护。
