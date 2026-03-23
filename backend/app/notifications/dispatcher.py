import asyncio
import smtplib
from email.mime.text import MIMEText

import httpx

from app.core.config import get_settings
from app.schemas.market import MarketAlert


class NotificationDispatcher:
    def __init__(self) -> None:
        self.cfg = get_settings()

    async def send_telegram(self, message: str) -> None:
        if not (self.cfg.telegram_bot_token and self.cfg.telegram_chat_id):
            return
        url = f"https://api.telegram.org/bot{self.cfg.telegram_bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=8) as client:
            await client.post(url, json={"chat_id": self.cfg.telegram_chat_id, "text": message})

    async def send_email(self, subject: str, message: str) -> None:
        if not all([self.cfg.email_host, self.cfg.email_user, self.cfg.email_password, self.cfg.email_to]):
            return

        def _send() -> None:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = self.cfg.email_user
            msg["To"] = self.cfg.email_to
            with smtplib.SMTP(self.cfg.email_host, self.cfg.email_port) as server:
                server.starttls()
                server.login(self.cfg.email_user, self.cfg.email_password)
                server.sendmail(self.cfg.email_user, [self.cfg.email_to], msg.as_string())

        await asyncio.to_thread(_send)

    async def send_web_push(self, payload: dict[str, str]) -> None:
        # Stub: integrate with OneSignal/Firebase/etc.
        _ = payload

    async def dispatch_alert(self, alert: MarketAlert) -> None:
        text = f"[{alert.severity}] {alert.symbol} - {alert.message}"
        await asyncio.gather(
            self.send_telegram(text),
            self.send_email(f"市场告警：{alert.alert_type}", text),
            self.send_web_push({"title": alert.alert_type, "body": text}),
        )
