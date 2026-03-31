from __future__ import annotations

from time import perf_counter

from core.graph.state import GraphState
from core.services.llm_service import get_llm_service
from config.constants import BLOG_PROMPT


async def run_blog(state: GraphState) -> dict:
    start = perf_counter()
    request = state["request"]
    audience = request.audience or "general"
    constraints = request.constraints or "none"
    spec = state.get("content_spec", {})
    def _stringify_list(values: list) -> str:
        return ", ".join(str(item) for item in values)

    prompt = BLOG_PROMPT.format(
        topic=request.topic,
        audience=audience,
        constraints=constraints,
        outline=_stringify_list(spec.get("outline", [])),
        tone=str(spec.get("tone", "neutral")),
        keywords=_stringify_list(spec.get("keywords", [])),
        entities=_stringify_list(spec.get("entities", [])),
        source_excerpt=state.get("doc_excerpt", ""),
    )
    llm = get_llm_service()
    anchor_content = await llm.generate(
        "You write high-quality marketing content.",
        prompt,
    )
    duration_ms = (perf_counter() - start) * 1000.0
    return {"anchor_content": anchor_content, "timings": {"blog_ms": duration_ms}}
