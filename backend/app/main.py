import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.services.orchestrator import Orchestrator
from app.services.runtime import RuntimeState
from app.services.ws_manager import WSManager, start_broadcast_loop

setup_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(router, prefix=settings.api_prefix)
manager = WSManager()
orchestrator = Orchestrator(symbols=[s.strip() for s in settings.symbols.split(",")])


async def produce() -> dict:
    RuntimeState.state = await orchestrator.tick()
    return RuntimeState.state


@app.on_event("startup")
async def startup_event() -> None:
    app.state.broadcast_task = asyncio.create_task(
        start_broadcast_loop(settings.websocket_broadcast_interval_sec, produce, manager)
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:
    app.state.broadcast_task.cancel()
    await orchestrator.close()


@app.websocket("/ws/market")
async def ws_market(ws: WebSocket) -> None:
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(ws)
