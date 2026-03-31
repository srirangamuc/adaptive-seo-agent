from __future__ import annotations

from time import perf_counter

from core.graph.state import GraphState
from core.validators.consistency import similarity_score as consistency_score
from core.validators.relevance import similarity_score as relevance_score
from config.constants import MIN_CONSISTENCY_SCORE, MIN_RELEVANCE_SCORE
from config.constants import (
    MAX_NEWSLETTER_CHARS,
    MAX_SEO_DESC_CHARS,
    MAX_SEO_TITLE_CHARS,
    MAX_SOCIAL_LINKEDIN_CHARS,
    MAX_SOCIAL_TWITTER_CHARS,
)


def _length_ok(text: str, limit: int) -> bool:
    return len(text.strip()) <= limit


def _extract_raw(block: dict[str, str]) -> str:
    if not isinstance(block, dict):
        return ""

    if "raw" in block:
        return block.get("raw", "")

    return " ".join(str(value) for value in block.values())


async def validate_derivatives(state: GraphState) -> dict:
    start = perf_counter()
    anchor = state.get("anchor_content") or ""
    topic = state["request"].topic

    failures: dict[str, str] = {}

    seo_raw = _extract_raw(state.get("seo", {}))
    social_raw = _extract_raw(state.get("social", {}))
    newsletter_raw = _extract_raw(state.get("newsletter", {}))

    seo_relevance = relevance_score(topic, seo_raw)
    seo_consistency = consistency_score(anchor, seo_raw)
    if seo_relevance < MIN_RELEVANCE_SCORE or seo_consistency < MIN_CONSISTENCY_SCORE:
        failures["seo"] = "relevance_or_consistency"
    seo_block = state.get("seo", {})
    if isinstance(seo_block, dict) and "title" in seo_block and "description" in seo_block:
        if not _length_ok(str(seo_block.get("title", "")), MAX_SEO_TITLE_CHARS):
            failures["seo"] = "length"
        if not _length_ok(str(seo_block.get("description", "")), MAX_SEO_DESC_CHARS):
            failures["seo"] = "length"
    elif not _length_ok(seo_raw, MAX_SEO_TITLE_CHARS + MAX_SEO_DESC_CHARS + 20):
        failures["seo"] = "length"

    social_relevance = relevance_score(topic, social_raw)
    social_consistency = consistency_score(anchor, social_raw)
    if social_relevance < MIN_RELEVANCE_SCORE or social_consistency < MIN_CONSISTENCY_SCORE:
        failures["social"] = "relevance_or_consistency"
    social_block = state.get("social", {})
    if isinstance(social_block, dict) and "twitter" in social_block and "linkedin" in social_block:
        if not _length_ok(str(social_block.get("twitter", "")), MAX_SOCIAL_TWITTER_CHARS):
            failures["social"] = "length"
        if not _length_ok(str(social_block.get("linkedin", "")), MAX_SOCIAL_LINKEDIN_CHARS):
            failures["social"] = "length"
    elif not _length_ok(social_raw, MAX_SOCIAL_TWITTER_CHARS + MAX_SOCIAL_LINKEDIN_CHARS + 80):
        failures["social"] = "length"

    newsletter_relevance = relevance_score(topic, newsletter_raw)
    newsletter_consistency = consistency_score(anchor, newsletter_raw)
    if newsletter_relevance < MIN_RELEVANCE_SCORE or newsletter_consistency < MIN_CONSISTENCY_SCORE:
        failures["newsletter"] = "relevance_or_consistency"
    if not _length_ok(newsletter_raw, MAX_NEWSLETTER_CHARS):
        failures["newsletter"] = "length"

    metadata = dict(state.get("metadata", {}))
    metadata["scores"] = {
        "seo_relevance": seo_relevance,
        "seo_consistency": seo_consistency,
        "social_relevance": social_relevance,
        "social_consistency": social_consistency,
        "newsletter_relevance": newsletter_relevance,
        "newsletter_consistency": newsletter_consistency,
    }
    duration_ms = (perf_counter() - start) * 1000.0
    return {
        "failure_reasons": failures,
        "derivatives_ok": not failures,
        "metadata": metadata,
        "timings": {"validate_derivatives_ms": duration_ms},
    }


def route_after_derivatives(state: GraphState) -> str:
    failures = state.get("failure_reasons", {})
    retries = state.get("node_retries", {})

    if not failures:
        return "complete"

    for node_key in ("seo", "social", "newsletter"):
        if node_key in failures:
            current = retries.get(node_key, 0)
            if current >= 2:
                continue
            retries[node_key] = current + 1
            state["node_retries"] = retries
            return f"retry_{node_key}"

    return "complete"
