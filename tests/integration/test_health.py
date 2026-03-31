from __future__ import annotations

from tests.conftest import get_client


def test_health_live() -> None:
    client = get_client()
    response = client.get("/health/live")
    assert response.status_code == 200


def test_health_ready() -> None:
    client = get_client()
    response = client.get("/health/ready")
    assert response.status_code == 200
