from __future__ import annotations

import json

import re
from time import perf_counter

from core.graph.state import GraphState
from core.services.llm_service import get_llm_service
from config.constants import SEO_JSON_PROMPT


async def run_seo(state: GraphState) -> dict:
    start = perf_counter()
    topic = state["request"].topic
    prompt = SEO_JSON_PROMPT.format(topic=topic)
    llm = get_llm_service()
    response = await llm.generate(
        "You create SEO metadata.",
        prompt,
    )
    cleaned = re.sub(r"^```(?:json)?\s*|```$", "", response.strip(), flags=re.IGNORECASE | re.MULTILINE)
    try:
        seo = json.loads(cleaned)
    except json.JSONDecodeError:
        seo = {"raw": response}
    duration_ms = (perf_counter() - start) * 1000.0
    return {"seo": seo, "timings": {"seo_ms": duration_ms}}
