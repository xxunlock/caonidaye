#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[提示] 已基于模板创建 .env，请按需填写密钥与通知配置。"
fi

docker compose up --build
