import asyncio
from collections.abc import Awaitable, Callable

from fastapi import WebSocket


class WSManager:
    def __init__(self) -> None:
        self.connections: set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.connections.add(ws)

    async def disconnect(self, ws: WebSocket) -> None:
        self.connections.discard(ws)

    async def broadcast(self, payload: dict) -> None:
        stale: list[WebSocket] = []
        for ws in self.connections:
            try:
                await ws.send_json(payload)
            except Exception:
                stale.append(ws)
        for ws in stale:
            self.connections.discard(ws)


async def start_broadcast_loop(interval: int, producer: Callable[[], Awaitable[dict]], manager: WSManager) -> None:
    while True:
        payload = await producer()
        await manager.broadcast(payload)
        await asyncio.sleep(interval)
