import os

bind = "0.0.0.0:8000"
workers = int(os.getenv("WORKERS", "2"))
worker_class = "uvicorn.workers.UvicornWorker"
threads = int(os.getenv("THREADS", "4"))
timeout = int(os.getenv("TIMEOUT", "120"))
graceful_timeout = 30
keepalive = int(os.getenv("KEEPALIVE", "5"))
max_requests = int(os.getenv("MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", "100"))
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info").lower()
