from __future__ import annotations

from time import perf_counter

from core.graph.state import GraphState
from core.validators.relevance import is_relevant
from config.constants import MAX_RETRIES


async def validate_anchor(state: GraphState) -> dict:
    start = perf_counter()
    anchor = state.get("anchor_content") or ""
    topic = state["request"].topic
    relevance_ok = is_relevant(topic, anchor)
    duration_ms = (perf_counter() - start) * 1000.0
    return {"relevance_ok": relevance_ok, "timings": {"validate_anchor_ms": duration_ms}}


def route_after_validation(state: GraphState) -> str:
    if state["relevance_ok"]:
        return "continue"

    if state["retries"] >= MAX_RETRIES:
        return "continue"

    state["retries"] += 1
    return "retry"
