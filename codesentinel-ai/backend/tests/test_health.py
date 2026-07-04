"""Tests for the health check endpoint."""


def test_health_check_returns_ok(client):
    """The /health endpoint should always return a 200 OK status payload."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "app" in body
    assert "env" in body
