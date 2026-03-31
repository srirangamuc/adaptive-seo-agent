FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000
CMD ["gunicorn", "api.main:app", "-c", "config/gunicorn_conf.py"]
