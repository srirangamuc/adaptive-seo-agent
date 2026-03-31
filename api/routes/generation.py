from __future__ import annotations

from fastapi import APIRouter, Request

from api.schemas.request import GenerateRequest
from api.schemas.response import GenerateResponse
from core.graph.engine import run_graph

router = APIRouter(tags=["generation"], prefix="/generate")


@router.post("")
async def generate(payload: GenerateRequest, request: Request) -> GenerateResponse:
    response = await run_graph(payload)
    response.content["request_id"] = getattr(request.state, "request_id", None)
    return response
