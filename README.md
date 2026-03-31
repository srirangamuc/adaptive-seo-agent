# Adaptive Content DAG

Adaptive Content DAG is a LangGraph-powered content system that generates a coordinated suite of outputs from a single topic or source document. It produces a canonical blog post, SEO metadata, social posts, and a newsletter summary while maintaining consistency across formats. The system supports fast mode for low-latency use cases and full mode for quality gates and adaptive retries.

## Highlights

- Stateful LangGraph DAG with conditional routing and adaptive retries.
- Parallelized transformation nodes for derived content.
- Embedding-based relevance and consistency checks.
- Document ingestion from plain text, URL, or PDF.
- Gradio UI for quick testing.
- JSON logging + optional LangSmith tracing.

## Quickstart

1) Create a UV environment:

```bash
uv venv --python 3.11
```

2) Install dependencies:

```bash
uv pip install -r requirements.txt
```

3) Configure environment:

```bash
copy .env.example .env
```

Set `GROQ_API_KEY` in `.env`.

4) Run the API:

```bash
uvicorn api.main:app --reload
```

## Production Run

Use Gunicorn with Uvicorn workers for production:

```bash
gunicorn api.main:app -c config/gunicorn_conf.py
```

Tune workers, threads, and timeouts via `config/gunicorn_conf.py` or environment values in `.env`.

## Usage

### API Request

```json
{
	"topic": "AI in healthcare",
	"audience": "Students",
	"constraints": "Keep the language technical and precise",
	"fast_mode": false,
	"source_text": "Optional: paste a document here",
	"source_url": "Optional: https://example.com/doc.pdf",
	"source_type": "pdf"
}
```

### API Response (shape)

```json
{
	"request_id": "...",
	"status": "ok",
	"content": {
		"anchor": "...",
		"seo": {"title": "...", "description": "...", "keywords": []},
		"social": {"twitter": "...", "linkedin": "..."},
		"newsletter": {"headline": "...", "summary": "..."},
		"metadata": {"scores": {}},
		"timings": {},
		"fast_mode": false,
		"retries": 0,
		"relevance_ok": true,
		"derivatives_ok": true,
		"failure_reasons": {},
		"node_retries": {}
	}
}
```

## DAG Overview

Full mode path:

1) Ingest document (optional)
2) Planning node builds content spec
3) Blog node generates the canonical anchor
4) Validation checks relevance
5) Derived outputs run in parallel: SEO+Social and Newsletter
6) Validation gates + adaptive retries

Fast mode path:

- Blog -> SEO+Social + Newsletter
- Skips planning, validation, and retries

## Document Ingestion

Document ingestion supports:

- Plain text (`source_text`)
- URL (`source_url`)
- PDF (`source_type: pdf`)

Ingestion extracts text, chunks it, and uses an excerpt for planning and generation.

## Profiling

Each node reports timings in milliseconds under `content.timings`.

Example (fast mode):

```json
{
	"blog_ms": 1363.18,
	"seo_social_ms": 437.12,
	"newsletter_ms": 368.39
}
```

## Performance Evaluation

Run baseline vs DAG comparison:

```bash
python -m scripts.evaluate
```

Sample run (5 topics, 2s rate-limit sleep between topics):

- Baseline total seconds: 18.54
- DAG total seconds: 80.76

Note: Full DAG includes planning, validation, embeddings, and retry logic. Use `fast_mode` for low-latency calls.

## Fast Mode

Set in `.env`:

```
FAST_MODE=true
```

Or override per request:

```json
{ "fast_mode": true }
```

## Logging and Tracing

- Structured JSON logs to console and `logs/app.log`
- Request ID propagated via `x-request-id`
- Optional LangSmith tracing via `LANGSMITH_ENABLED=true`

## Gradio UI

```bash
python gradio_app.py
```

## Tests

```bash
pytest -q
```
