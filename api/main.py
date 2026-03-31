from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.errors import unhandled_exception_handler
from api.middleware.request_logging import RequestLoggingMiddleware
from api.routes.generation import router as generation_router
from api.routes.health import router as health_router
from config.logging import setup_logging
from config.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    setup_logging(settings)
    yield


app = FastAPI(title="Adaptive Content DAG", lifespan=lifespan)
app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.include_router(health_router)
app.include_router(generation_router)
