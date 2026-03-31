from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"], prefix="/health")


@router.get("/live")
async def live() -> dict:
    return {"status": "live"}


@router.get("/ready")
async def ready() -> dict:
    return {"status": "ready"}
