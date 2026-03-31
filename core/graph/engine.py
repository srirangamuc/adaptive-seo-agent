from __future__ import annotations

import uuid
from functools import lru_cache

from langgraph.graph import END, StateGraph

from api.schemas.request import GenerateRequest
from api.schemas.response import GenerateResponse
from config.settings import Settings
from core.graph.nodes.blog_node import run_blog
from core.graph.nodes.ingest_node import run_ingest
from core.graph.nodes.newsletter_node import run_newsletter
from core.graph.nodes.planning_node import run_planning
from core.graph.nodes.retry_node import route_after_validation, validate_anchor
from core.graph.nodes.seo_social_node import run_seo_social
from core.graph.nodes.validation_node import route_after_derivatives, validate_derivatives
from core.graph.state import GraphState


@lru_cache
def get_graph(fast_mode: bool):
    graph = StateGraph(GraphState)

    graph.add_node("ingest_node", run_ingest)
    graph.add_node("blog_node", run_blog)
    graph.add_node("seo_social_node", run_seo_social)
    graph.add_node("newsletter_node", run_newsletter)

    if not fast_mode:
        graph.add_node("planning_node", run_planning)
        graph.add_node("validate_node", validate_anchor)
        graph.add_node("validate_derivatives", validate_derivatives)

    if fast_mode:
        graph.set_entry_point("ingest_node")
        graph.add_edge("ingest_node", "blog_node")
        graph.add_edge("blog_node", "seo_social_node")
        graph.add_edge("blog_node", "newsletter_node")
        graph.add_edge("seo_social_node", END)
        graph.add_edge("newsletter_node", END)
    else:
        graph.set_entry_point("ingest_node")
        graph.add_edge("ingest_node", "planning_node")
        graph.add_edge("planning_node", "blog_node")
        graph.add_edge("blog_node", "validate_node")
        graph.add_conditional_edges(
            "validate_node",
            route_after_validation,
            {
                "retry": "blog_node",
                "continue": "seo_social_node",
            },
        )
        graph.add_edge("seo_social_node", "validate_derivatives")
        graph.add_edge("newsletter_node", "validate_derivatives")
        graph.add_conditional_edges(
            "validate_derivatives",
            route_after_derivatives,
            {
                "retry_seo": "seo_social_node",
                "retry_social": "seo_social_node",
                "retry_newsletter": "newsletter_node",
                "complete": END,
            },
        )

        graph.add_edge("validate_node", "seo_social_node")
        graph.add_edge("validate_node", "newsletter_node")

    return graph.compile()


async def run_graph(payload: GenerateRequest) -> GenerateResponse:
    settings = Settings()
    fast_mode = payload.fast_mode if payload.fast_mode is not None else settings.fast_mode
    initial_state: GraphState = {
        "request": payload,
        "source_doc": None,
        "doc_chunks": [],
        "doc_excerpt": "",
        "content_spec": {},
        "anchor_content": None,
        "seo": {},
        "social": {},
        "newsletter": {},
        "metadata": {},
        "timings": {},
        "retries": 0,
        "relevance_ok": True if fast_mode else False,
        "derivatives_ok": True if fast_mode else False,
        "failure_reasons": {},
        "node_retries": {},
    }

    result = await get_graph(fast_mode).ainvoke(initial_state)

    return GenerateResponse(
        request_id=uuid.uuid4().hex,
        status="ok",
        content={
            "anchor": result.get("anchor_content"),
            "seo": result.get("seo", {}),
            "social": result.get("social", {}),
            "newsletter": result.get("newsletter", {}),
            "metadata": result.get("metadata", {}),
            "timings": result.get("timings", {}),
            "fast_mode": fast_mode,
            "retries": result.get("retries", 0),
            "relevance_ok": result.get("relevance_ok", False),
            "derivatives_ok": result.get("derivatives_ok", False),
            "failure_reasons": result.get("failure_reasons", {}),
            "node_retries": result.get("node_retries", {}),
        },
    )
