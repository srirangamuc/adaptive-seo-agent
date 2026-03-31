from __future__ import annotations

from functools import lru_cache
import os

import numpy as np
from sentence_transformers import SentenceTransformer

from config.settings import Settings


class EmbeddingService:
    def __init__(self, settings: Settings):
        os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "0")
        try:
            self._model = SentenceTransformer(settings.embedding_model)
        except OSError as exc:
            raise RuntimeError(
                "Failed to load embedding model. Ensure the model name is correct, "
                "internet access is available, or set a local model path."
            ) from exc
        self._cache: dict[str, np.ndarray] = {}

    def embed_text(self, text: str) -> np.ndarray:
        cached = self._cache.get(text)
        if cached is not None:
            return cached

        vector = self._model.encode(text, normalize_embeddings=False)
        arr = np.array(vector, dtype=float)
        self._cache[text] = arr
        return arr

    def similarity(self, text_a: str, text_b: str) -> float:
        if not text_a.strip() or not text_b.strip():
            return 0.0

        vec_a = self.embed_text(text_a)
        vec_b = self.embed_text(text_b)

        denom = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
        if denom == 0.0:
            return 0.0

        return float(np.dot(vec_a, vec_b) / denom)


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(Settings())
