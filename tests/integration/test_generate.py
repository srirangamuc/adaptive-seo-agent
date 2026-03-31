from __future__ import annotations

import json

from tests.conftest import get_client


class _StubLLM:
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        if "strict JSON" in system_prompt:
            payload = {
                "seo": {
                    "title": "AI in healthcare",
                    "description": "AI improves healthcare workflows.",
                    "keywords": ["AI", "healthcare"],
                },
                "social": {
                    "twitter": "AI transforms healthcare.",
                    "linkedin": "AI adoption in healthcare is accelerating.",
                },
            }
            return json.dumps(payload)

        if "newsletter summaries" in system_prompt:
            payload = {
                "headline": "AI in healthcare",
                "summary": "AI supports better diagnostics and operations.",
            }
            return json.dumps(payload)

        return "Blog content about AI in healthcare."


def test_generate_fast_mode(monkeypatch) -> None:
    from core.graph.nodes import blog_node
    from core.graph.nodes import seo_social_node
    from core.graph.nodes import newsletter_node

    monkeypatch.setattr(blog_node, "get_llm_service", lambda: _StubLLM())
    monkeypatch.setattr(seo_social_node, "get_llm_service", lambda: _StubLLM())
    monkeypatch.setattr(newsletter_node, "get_llm_service", lambda: _StubLLM())

    client = get_client()
    response = client.post(
        "/generate",
        json={
            "topic": "AI in healthcare",
            "fast_mode": True,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    content = payload["content"]

    assert content["fast_mode"] is True
    assert isinstance(content["anchor"], str)
    assert "seo" in content and "social" in content and "newsletter" in content
    assert "title" in content["seo"]
    assert "twitter" in content["social"]
    assert "headline" in content["newsletter"]
