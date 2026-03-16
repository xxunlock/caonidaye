from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler


class JobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def add_interval_job(self, func, seconds: int | None = None, minutes: int | None = None, id: str | None = None):
        self.scheduler.add_job(func, "interval", seconds=seconds, minutes=minutes, id=id, replace_existing=True)

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown(wait=False)
