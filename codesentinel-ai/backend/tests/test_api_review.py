"""
Integration tests for the AI Review API endpoints.

Uses FastAPI dependency overrides to replace GitHubService and
GroqService with mocks, exercising the full HTTP -> service ->
repository -> database path without real network calls.
"""

from unittest.mock import AsyncMock

from app.core.dependencies import get_github_service, get_groq_service
from app.main import app
from app.schemas.github_schemas import ChangedFileSchema, PullRequestSchema


def _fake_pull_request() -> PullRequestSchema:
    return PullRequestSchema(
        pr_number=7,
        title="Fix pagination bug",
        description=None,
        author="octocat",
        base_branch="main",
        head_branch="fix-pagination",
        additions=10,
        deletions=2,
        changed_files_count=1,
        html_url="https://github.com/octocat/demo/pull/7",
        changed_files=[
            ChangedFileSchema(
                filename="app.py", status="modified", additions=10, deletions=2, changes=12, patch="diff"
            )
        ],
    )


def test_analyze_pull_request_success(client):
    mock_github = AsyncMock()
    mock_github.get_full_pull_request.return_value = _fake_pull_request()

    mock_groq = AsyncMock()
    mock_groq.generate_structured_review.return_value = {
        "summary": "Clean, well-structured fix.",
        "overall_score": 9.0,
        "risk_level": "LOW",
        "issues": [],
        "strengths": ["Good test coverage", "Clear commit message"],
    }

    app.dependency_overrides[get_github_service] = lambda: mock_github
    app.dependency_overrides[get_groq_service] = lambda: mock_groq

    response = client.post(
        "/api/v1/review/analyze",
        json={"repo_owner": "octocat", "repo_name": "demo", "pr_number": 7},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["review"]["overall_score"] == 9.0
    assert body["data"]["review"]["risk_level"] == "LOW"

    app.dependency_overrides.pop(get_github_service, None)
    app.dependency_overrides.pop(get_groq_service, None)


def test_analyze_pull_request_rejects_invalid_pr_number(client):
    response = client.post(
        "/api/v1/review/analyze",
        json={"repo_owner": "octocat", "repo_name": "demo", "pr_number": 0},
    )
    assert response.status_code == 422


def test_get_review_returns_404_when_not_found(client):
    response = client.get("/api/v1/review/999")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
