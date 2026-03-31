from __future__ import annotations

import json

import re
from time import perf_counter

from core.graph.state import GraphState
from core.services.llm_service import get_llm_service
from config.constants import SOCIAL_JSON_PROMPT


async def run_social(state: GraphState) -> dict:
    start = perf_counter()
    request = state["request"]
    audience = request.audience or "general"
    prompt = SOCIAL_JSON_PROMPT.format(topic=request.topic, audience=audience)
    llm = get_llm_service()
    response = await llm.generate(
        "You write social media posts.",
        prompt,
    )
    cleaned = re.sub(r"^```(?:json)?\s*|```$", "", response.strip(), flags=re.IGNORECASE | re.MULTILINE)
    try:
        social = json.loads(cleaned)
    except json.JSONDecodeError:
        social = {"raw": response}
    duration_ms = (perf_counter() - start) * 1000.0
    return {"social": social, "timings": {"social_ms": duration_ms}}
