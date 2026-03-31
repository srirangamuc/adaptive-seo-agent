from __future__ import annotations

import json
import re
from time import perf_counter

from config.constants import SEO_SOCIAL_JSON_PROMPT
from core.graph.state import GraphState
from core.services.llm_service import get_llm_service


async def run_seo_social(state: GraphState) -> dict:
    start = perf_counter()
    request = state["request"]
    audience = request.audience or "general"
    prompt = SEO_SOCIAL_JSON_PROMPT.format(topic=request.topic, audience=audience)
    llm = get_llm_service()
    response = await llm.generate(
        "You create SEO metadata and social posts in strict JSON.",
        prompt,
    )
    cleaned = re.sub(r"^```(?:json)?\s*|```$", "", response.strip(), flags=re.IGNORECASE | re.MULTILINE)
    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    payload = match.group(0) if match else cleaned
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        parsed = {}

    seo = parsed.get("seo") if isinstance(parsed, dict) else None
    social = parsed.get("social") if isinstance(parsed, dict) else None

    duration_ms = (perf_counter() - start) * 1000.0
    return {
        "seo": seo if isinstance(seo, dict) else {"raw": response},
        "social": social if isinstance(social, dict) else {"raw": response},
        "timings": {"seo_social_ms": duration_ms},
    }
