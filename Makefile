PYTHON=python

.PHONY: help setup install dev prod test lint fmt eval ui

help:
	@echo "Targets:"
	@echo "  setup   - create venv with uv"
	@echo "  install - install dependencies"
	@echo "  dev     - run API with reload"
	@echo "  prod    - run API with gunicorn"
	@echo "  test    - run pytest"
	@echo "  eval    - run baseline vs DAG comparison"
	@echo "  ui      - run Gradio UI"

setup:
	uv venv --python 3.11

install:
	uv pip install -r requirements.txt

# Use explicit reload dirs to avoid watching .venv
dev:
	uvicorn api.main:app --reload --reload-dir api --reload-dir core --reload-dir config --reload-dir scripts --reload-dir tests

prod:
	gunicorn api.main:app -c config/gunicorn_conf.py

test:
	pytest -q

eval:
	python -m scripts.evaluate

ui:
	python gradio_app.py
