from __future__ import annotations

from fastapi import FastAPI


class DashboardAPI:
    def __init__(self, state: dict):
        self.state = state
        self.app = FastAPI(title="AI Crypto Quant Dashboard", version="1.0.0")
        self._register_routes()

    def _register_routes(self) -> None:
        @self.app.get("/signals")
        def signals():
            return self.state.get("signals", [])

        @self.app.get("/market")
        def market():
            return self.state.get("market", {})

        @self.app.get("/orderbook")
        def orderbook():
            return self.state.get("orderbook", {})

        @self.app.get("/liquidations")
        def liquidations():
            return self.state.get("liquidations", {})

        @self.app.get("/sentiment")
        def sentiment():
            return self.state.get("sentiment", {})

        @self.app.get("/whales")
        def whales():
            return self.state.get("whales", {})
