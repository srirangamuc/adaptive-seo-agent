from __future__ import annotations

import asyncio
from time import perf_counter

from api.schemas.request import GenerateRequest
from config.constants import BLOG_PROMPT, NEWSLETTER_JSON_PROMPT, SEO_JSON_PROMPT, SOCIAL_JSON_PROMPT
from core.graph.engine import run_graph
from core.services.llm_service import get_llm_service


TOPICS = [
    "AI adoption in retail",
    "Sustainable packaging for ecommerce",
    "Customer retention in fintech",
    "Remote work productivity for managers",
    "Cybersecurity basics for small businesses",
]

RATE_LIMIT_SLEEP_SECONDS = 2.0


def _baseline_request(topic: str) -> GenerateRequest:
    return GenerateRequest(topic=topic)


async def baseline_generate(topic: str) -> dict:
    llm = get_llm_service()
    request = _baseline_request(topic)

    blog_prompt = BLOG_PROMPT.format(
        topic=request.topic,
        audience=request.audience or "general",
        constraints=request.constraints or "none",
        outline="",
        tone="neutral",
        keywords="",
        entities="",
    )

    anchor = await llm.generate(
        "You write high-quality marketing content.",
        blog_prompt,
    )

    seo_prompt = SEO_JSON_PROMPT.format(topic=request.topic)
    seo = await llm.generate("You create SEO metadata.", seo_prompt)

    social_prompt = SOCIAL_JSON_PROMPT.format(topic=request.topic, audience="general")
    social = await llm.generate("You write social media posts.", social_prompt)

    newsletter_prompt = NEWSLETTER_JSON_PROMPT.format(
        topic=request.topic,
        audience="general",
        anchor=anchor,
    )
    newsletter = await llm.generate("You write concise newsletter summaries.", newsletter_prompt)

    return {
        "anchor": anchor,
        "seo": seo,
        "social": social,
        "newsletter": newsletter,
        "timings": {},
        "fast_mode": False,
    }


async def run_baseline() -> float:
    start = perf_counter()
    for topic in TOPICS:
        await baseline_generate(topic)
        await asyncio.sleep(RATE_LIMIT_SLEEP_SECONDS)
    return perf_counter() - start


async def run_dag() -> float:
    start = perf_counter()
    for topic in TOPICS:
        await run_graph(GenerateRequest(topic=topic))
        await asyncio.sleep(RATE_LIMIT_SLEEP_SECONDS)
    return perf_counter() - start


async def main() -> None:
    baseline_time = await run_baseline()
    dag_time = await run_dag()

    print("Baseline total seconds:", round(baseline_time, 2))
    print("DAG total seconds:", round(dag_time, 2))


if __name__ == "__main__":
    asyncio.run(main())
