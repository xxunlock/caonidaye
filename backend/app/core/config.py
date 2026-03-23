from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Crypto Quant Assistant"
    env: str = "dev"
    debug: bool = True
    api_prefix: str = "/api/v1"

    openai_api_key: str | None = None
    llm_provider: str = "openai"  # openai | qwen | deepseek
    local_llm_url: str | None = None

    symbols: str = "BTCUSDT,ETHUSDT,SOLUSDT"
    timeframe: str = "1m"
    anomaly_price_threshold_pct: float = 2.5
    anomaly_volume_multiplier: float = 2.0
    whale_order_usd_threshold: float = 500000.0

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    email_host: str | None = None
    email_port: int = 587
    email_user: str | None = None
    email_password: str | None = None
    email_to: str | None = None

    websocket_broadcast_interval_sec: int = 2


@lru_cache
def get_settings() -> Settings:
    return Settings()
