from __future__ import annotations

from config.constants import MIN_CONSISTENCY_SCORE
from core.services.embedding_service import get_embedding_service


def similarity_score(text_a: str, text_b: str) -> float:
    service = get_embedding_service()
    return service.similarity(text_a, text_b)


def is_consistent(anchor: str, sub_content: str) -> bool:
    return similarity_score(anchor, sub_content) >= MIN_CONSISTENCY_SCORE
