from __future__ import annotations

from functools import lru_cache
import asyncio
import os
import random

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from config.settings import Settings


class LLMService:
    def __init__(self, settings: Settings):
        self._settings = settings
        if settings.langsmith_enabled:
            os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
            os.environ.setdefault("LANGCHAIN_API_KEY", settings.langsmith_api_key)
            os.environ.setdefault("LANGCHAIN_PROJECT", settings.langsmith_project)
        self._client = ChatGroq(
            api_key=settings.groq_api_key or None,
            model=settings.groq_model,
            temperature=settings.groq_temperature,
        )

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
        attempt = 0
        # Retry on transient errors like rate limits with exponential backoff.
        while True:
            try:
                response = await self._client.ainvoke(messages)
                return response.content
            except Exception as exc:  # pragma: no cover - library exceptions vary
                attempt += 1
                if attempt > self._settings.llm_max_retries:
                    raise

                # Exponential backoff with jitter; handles 429s and transient failures.
                delay = min(
                    self._settings.llm_retry_max_delay,
                    self._settings.llm_retry_base_delay * (2 ** (attempt - 1)),
                )
                delay = delay * (0.8 + random.random() * 0.4)
                await asyncio.sleep(delay)


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService(Settings())
