from __future__ import annotations

import json

import re
from time import perf_counter

from config.constants import NEWSLETTER_JSON_PROMPT
from core.graph.state import GraphState
from core.services.llm_service import get_llm_service


async def run_newsletter(state: GraphState) -> dict:
    start = perf_counter()
    request = state["request"]
    audience = request.audience or "general"
    anchor = state.get("anchor_content") or ""
    prompt = NEWSLETTER_JSON_PROMPT.format(
        topic=request.topic,
        audience=audience,
        anchor=anchor,
    )
    llm = get_llm_service()
    response = await llm.generate(
        "You write concise newsletter summaries.",
        prompt,
    )
    cleaned = re.sub(r"^```(?:json)?\s*|```$", "", response.strip(), flags=re.IGNORECASE | re.MULTILINE)
    try:
        newsletter = json.loads(cleaned)
    except json.JSONDecodeError:
        newsletter = {"raw": response}
    duration_ms = (perf_counter() - start) * 1000.0
    return {"newsletter": newsletter, "timings": {"newsletter_ms": duration_ms}}
