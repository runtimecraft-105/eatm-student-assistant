import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app import create_app


@pytest.fixture
def client():
    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["service"] == "EATM Student Assistant"


def test_empty_message(client):
    response = client.post(
        "/api/chat",
        json={
            "message": ""
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "message cannot be empty"


def test_invalid_json(client):
    response = client.post(
        "/api/chat",
        data="this is not json",
        content_type="application/json"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == (
        "Request body must be valid JSON"
    )


def test_message_too_long(client):
    response = client.post(
        "/api/chat",
        json={
            "message": "a" * 4001
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "must not exceed" in data["error"]


def test_admin_ingestion_requires_token(client):
    response = client.post(
        "/api/admin/ingest"
    )

    assert response.status_code == 401

    data = response.get_json()

    assert data["error"] == "Unauthorized"