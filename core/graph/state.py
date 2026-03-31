from __future__ import annotations

from typing import Any, Optional, TypedDict, Annotated
import operator

from api.schemas.request import GenerateRequest


class GraphState(TypedDict):
    request: GenerateRequest
    source_doc: Optional[str]
    doc_chunks: list[str]
    doc_excerpt: str
    content_spec: dict[str, Any]
    anchor_content: Optional[str]
    seo: dict[str, Any]
    social: dict[str, Any]
    newsletter: dict[str, Any]
    metadata: dict[str, Any]
    timings: Annotated[dict[str, float], operator.or_]
    retries: int
    relevance_ok: bool
    derivatives_ok: bool
    failure_reasons: dict[str, str]
    node_retries: dict[str, int]
