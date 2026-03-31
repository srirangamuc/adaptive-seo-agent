from __future__ import annotations

from time import perf_counter

from core.graph.state import GraphState
from core.services.doc_ingest import chunk_text, fetch_source_text


async def run_ingest(state: GraphState) -> dict:
    start = perf_counter()
    request = state["request"]

    source_text = (request.source_text or "").strip()
    source_url = (request.source_url or "").strip()
    source_type = (request.source_type or "").strip().lower() or None

    if not source_text and source_url:
        source_text = fetch_source_text(source_url, source_type)

    chunks = chunk_text(source_text)
    excerpt = "" if not chunks else chunks[0][:1500]

    duration_ms = (perf_counter() - start) * 1000.0
    return {
        "source_doc": source_text,
        "doc_chunks": chunks,
        "doc_excerpt": excerpt,
        "timings": {"ingest_ms": duration_ms},
    }
