from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GenerateResponse(BaseModel):
    request_id: str = Field(..., min_length=8, max_length=64)
    status: str
    content: dict[str, Any]
