from __future__ import annotations

from config.constants import MIN_RELEVANCE_SCORE
from core.services.embedding_service import get_embedding_service


def similarity_score(text_a: str, text_b: str) -> float:
    service = get_embedding_service()
    return service.similarity(text_a, text_b)


def is_relevant(topic: str, content: str) -> bool:
    return similarity_score(topic, content) >= MIN_RELEVANCE_SCORE
