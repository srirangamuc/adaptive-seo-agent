from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


def get_client() -> TestClient:
    return TestClient(app)
