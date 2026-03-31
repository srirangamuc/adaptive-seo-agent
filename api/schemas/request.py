from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=200)
    audience: Optional[str] = Field(default=None, max_length=200)
    channels: list[str] = Field(default_factory=list)
    constraints: Optional[str] = Field(default=None, max_length=500)
    fast_mode: bool = Field(default=False)
    source_text: Optional[str] = Field(default=None, max_length=20000)
    source_url: Optional[str] = Field(default=None, max_length=2000)
    source_type: Optional[str] = Field(default=None, max_length=20)
