"""
Unit tests for ReviewService orchestration logic.

GitHub and Groq services are fully mocked so these tests run
deterministically, offline, and without consuming any API quota.
"""

from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import ValidationException
from app.schemas.github_schemas import ChangedFileSchema, PullRequestSchema
from app.schemas.review_schemas import ReviewRequestSchema
from app.services.review_service import ReviewService


def _fake_pull_request() -> PullRequestSchema:
    return PullRequestSchema(
        pr_number=1,
        title="Add login feature",
        description="Adds basic auth",
        author="testuser",
        base_branch="main",
        head_branch="add-login-feature",
        additions=23,
        deletions=0,
        changed_files_count=1,
        html_url="https://github.com/testuser/testrepo/pull/1",
        changed_files=[
            ChangedFileSchema(
                filename="auth.py",
                status="added",
                additions=23,
                deletions=0,
                changes=23,
                patch="+def login(username, password): ...",
            )
        ],
    )


def _fake_groq_result() -> dict:
    return {
        "summary": "Contains a SQL injection vulnerability.",
        "overall_score": 4.5,
        "risk_level": "HIGH",
        "issues": [
            {
                "file_path": "auth.py",
                "line_number": 6,
                "severity": "HIGH",
                "category": "SECURITY",
                "description": "SQL injection via string concatenation.",
                "suggestion": "Use parameterized queries.",
            }
        ],
        "strengths": ["Readable function names."],
    }


@pytest.mark.asyncio
async def test_review_pull_request_success(db_session):
    """A successful review orchestrates GitHub fetch, AI inference, and persistence."""
    mock_github = AsyncMock()
    mock_github.get_full_pull_request.return_value = _fake_pull_request()

    mock_groq = AsyncMock()
    mock_groq.generate_structured_review.return_value = _fake_groq_result()

    service = ReviewService(github_service=mock_github, groq_service=mock_groq, db=db_session)
    request = ReviewRequestSchema(repo_owner="testuser", repo_name="testrepo", pr_number=1)

    result = await service.review_pull_request(request)

    assert result.review.overall_score == 4.5
    assert result.review.risk_level == "HIGH"
    assert len(result.review.issues) == 1
    assert result.review.issues[0].category == "SECURITY"
    mock_github.get_full_pull_request.assert_awaited_once_with("testuser", "testrepo", 1)
    mock_groq.generate_structured_review.assert_awaited_once()


@pytest.mark.asyncio
async def test_review_pull_request_persists_to_database(db_session):
    """Reviewing a PR should create retrievable PullRequest and Review records."""
    mock_github = AsyncMock()
    mock_github.get_full_pull_request.return_value = _fake_pull_request()

    mock_groq = AsyncMock()
    mock_groq.generate_structured_review.return_value = _fake_groq_result()

    service = ReviewService(github_service=mock_github, groq_service=mock_groq, db=db_session)
    request = ReviewRequestSchema(repo_owner="testuser", repo_name="testrepo", pr_number=1)

    await service.review_pull_request(request)

    saved_pr = service.pull_request_repository.get_by_identity("testuser", "testrepo", 1)
    assert saved_pr is not None
    assert saved_pr.title == "Add login feature"

    saved_review = service.review_repository.get_latest_by_pull_request_id(saved_pr.id)
    assert saved_review is not None
    assert saved_review.risk_level == "HIGH"


@pytest.mark.asyncio
async def test_review_pull_request_raises_on_invalid_ai_output(db_session):
    """Malformed AI output failing schema validation should raise ValidationException."""
    mock_github = AsyncMock()
    mock_github.get_full_pull_request.return_value = _fake_pull_request()

    mock_groq = AsyncMock()
    mock_groq.generate_structured_review.return_value = {"summary": "incomplete output"}

    service = ReviewService(github_service=mock_github, groq_service=mock_groq, db=db_session)
    request = ReviewRequestSchema(repo_owner="testuser", repo_name="testrepo", pr_number=1)

    with pytest.raises(ValidationException):
        await service.review_pull_request(request)
