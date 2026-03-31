from __future__ import annotations

import json
from time import perf_counter

from config.constants import PLANNING_PROMPT
from core.graph.state import GraphState
from core.services.llm_service import get_llm_service


async def run_planning(state: GraphState) -> dict:
    start = perf_counter()
    request = state["request"]
    audience = request.audience or "general"
    constraints = request.constraints or "none"

    prompt = PLANNING_PROMPT.format(
        topic=request.topic,
        audience=audience,
        constraints=constraints,
        source_excerpt=state.get("doc_excerpt", ""),
    )

    llm = get_llm_service()
    response = await llm.generate(
        "You are a planning assistant that returns strict JSON.",
        prompt,
    )

    try:
        spec = json.loads(response)
    except json.JSONDecodeError:
        spec = {
            "outline": [],
            "tone": "neutral",
            "entities": [],
            "keywords": [],
        }

    duration_ms = (perf_counter() - start) * 1000.0
    return {"content_spec": spec, "timings": {"planning_ms": duration_ms}}
