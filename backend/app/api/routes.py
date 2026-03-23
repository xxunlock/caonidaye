from fastapi import APIRouter

from app.services.runtime import RuntimeState

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/snapshot")
async def snapshot() -> dict:
    return RuntimeState.state
