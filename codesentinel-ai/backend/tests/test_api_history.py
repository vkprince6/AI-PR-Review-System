"""
Integration tests for the History API endpoints (listing and deletion).
"""

from unittest.mock import AsyncMock

from app.core.dependencies import get_github_service, get_groq_service
from app.main import app
from app.schemas.github_schemas import ChangedFileSchema, PullRequestSchema


def _seed_one_review(client) -> dict:
    """Helper: analyze one mocked PR so history endpoints have data to return."""
    mock_github = AsyncMock()
    mock_github.get_full_pull_request.return_value = PullRequestSchema(
        pr_number=1,
        title="Seed PR",
        description=None,
        author="tester",
        base_branch="main",
        head_branch="feature",
        additions=5,
        deletions=1,
        changed_files_count=1,
        html_url="https://github.com/tester/repo/pull/1",
        changed_files=[
            ChangedFileSchema(filename="a.py", status="added", additions=5, deletions=1, changes=6, patch="diff")
        ],
    )
    mock_groq = AsyncMock()
    mock_groq.generate_structured_review.return_value = {
        "summary": "Looks fine.",
        "overall_score": 8.0,
        "risk_level": "LOW",
        "issues": [],
        "strengths": ["Simple change"],
    }

    app.dependency_overrides[get_github_service] = lambda: mock_github
    app.dependency_overrides[get_groq_service] = lambda: mock_groq

    response = client.post(
        "/api/v1/review/analyze",
        json={"repo_owner": "tester", "repo_name": "repo", "pr_number": 1},
    )
    app.dependency_overrides.pop(get_github_service, None)
    app.dependency_overrides.pop(get_groq_service, None)
    return response.json()["data"]


def test_list_pull_requests_returns_empty_initially(client):
    response = client.get("/api/v1/history/pull-requests")
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["items"] == []
    assert body["data"]["total"] == 0


def test_list_pull_requests_returns_seeded_record(client):
    _seed_one_review(client)
    response = client.get("/api/v1/history/pull-requests")
    body = response.json()
    assert body["data"]["total"] == 1
    assert body["data"]["items"][0]["repo_owner"] == "tester"
    assert body["data"]["items"][0]["latest_review_score"] == 8.0


def test_delete_pull_request_removes_record(client):
    _seed_one_review(client)
    list_response = client.get("/api/v1/history/pull-requests")
    pr_id = list_response.json()["data"]["items"][0]["id"]

    delete_response = client.delete(f"/api/v1/history/pull-requests/{pr_id}")
    assert delete_response.status_code == 204

    list_after = client.get("/api/v1/history/pull-requests")
    assert list_after.json()["data"]["total"] == 0


def test_delete_nonexistent_pull_request_returns_404(client):
    response = client.delete("/api/v1/history/pull-requests/999")
    assert response.status_code == 404
