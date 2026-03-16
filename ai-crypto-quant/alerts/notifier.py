from __future__ import annotations

from dataclasses import dataclass

from alerts.telegram_bot import TelegramAlertBot


@dataclass
class AlertMessage:
    symbol: str
    signal: str
    confidence: float
    entry_low: float
    entry_high: float
    stop_loss: float
    take_profit: float

    def render(self) -> str:
        return (
            f"COIN: {self.symbol}\n\n"
            f"Signal: {self.signal}\n\n"
            f"Confidence: {int(self.confidence * 100)}%\n\n"
            f"Entry:\n{self.entry_low:.2f} - {self.entry_high:.2f}\n\n"
            f"Stop loss:\n{self.stop_loss:.2f}\n\n"
            f"Take profit:\n{self.take_profit:.2f}\n"
        )


class Notifier:
    def __init__(self, telegram_enabled: bool = False, bot: TelegramAlertBot | None = None):
        self.telegram_enabled = telegram_enabled
        self.bot = bot

    async def notify(self, msg: AlertMessage) -> None:
        if self.telegram_enabled and self.bot:
            await self.bot.send(msg.render())
