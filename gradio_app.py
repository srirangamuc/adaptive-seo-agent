from __future__ import annotations

import json

import gradio as gr
import requests


def _build_payload(
    topic: str,
    audience: str,
    constraints: str,
    fast_mode: bool,
    source_text: str,
    source_url: str,
    source_type: str,
) -> dict:
    payload = {
        "topic": topic.strip(),
        "fast_mode": fast_mode,
    }
    if audience.strip():
        payload["audience"] = audience.strip()
    if constraints.strip():
        payload["constraints"] = constraints.strip()
    if source_text.strip():
        payload["source_text"] = source_text.strip()
    if source_url.strip():
        payload["source_url"] = source_url.strip()
    if source_type.strip():
        payload["source_type"] = source_type.strip().lower()
    return payload


def generate(
    api_url: str,
    topic: str,
    audience: str,
    constraints: str,
    fast_mode: bool,
    source_text: str,
    source_url: str,
    source_type: str,
) -> tuple[str, str]:
    payload = _build_payload(topic, audience, constraints, fast_mode, source_text, source_url, source_type)
    response = requests.post(f"{api_url.rstrip('/')}/generate", json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    content = data.get("content", {})

    formatted = json.dumps(content, indent=2, ensure_ascii=True)
    timings = json.dumps(content.get("timings", {}), indent=2, ensure_ascii=True)
    return formatted, timings


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Adaptive Content DAG") as demo:
        gr.Markdown("# Adaptive Content DAG\nGenerate blog + SEO + social + newsletter content.")

        with gr.Row():
            api_url = gr.Textbox(value="http://127.0.0.1:8000", label="API URL")
            fast_mode = gr.Checkbox(value=False, label="Fast mode")

        topic = gr.Textbox(label="Topic", placeholder="AI adoption in retail")
        audience = gr.Textbox(label="Audience (optional)", placeholder="Store managers")
        constraints = gr.Textbox(label="Constraints (optional)", placeholder="Keep it concise")
        source_text = gr.Textbox(label="Source text (optional)", lines=6)
        source_url = gr.Textbox(label="Source URL (optional)", placeholder="https://example.com/doc.pdf")
        source_type = gr.Dropdown(
            label="Source type (optional)",
            choices=["", "pdf", "html", "text"],
            value="",
        )

        submit = gr.Button("Generate")

        with gr.Row():
            output = gr.JSON(label="Content")
            timings = gr.JSON(label="Timings (ms)")

        submit.click(
            fn=generate,
            inputs=[api_url, topic, audience, constraints, fast_mode, source_text, source_url, source_type],
            outputs=[output, timings],
        )

    return demo


if __name__ == "__main__":
    build_app().launch()
