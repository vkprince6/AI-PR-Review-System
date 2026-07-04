"""
Unit tests for GitHubService.

The underlying HTTPX client is mocked so these tests run fully
offline with no real GitHub API calls or token required.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.exceptions import GitHubAPIException
from app.services.github_service import GitHubService


def _mock_response(status_code: int, json_data):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = json_data
    response.text = str(json_data)
    return response


@pytest.mark.asyncio
async def test_validate_repository_success():
    service = GitHubService()
    service._client.get = AsyncMock(
        return_value=_mock_response(
            200,
            {
                "owner": {"login": "facebook"},
                "name": "react",
                "default_branch": "main",
                "private": False,
                "stargazers_count": 200000,
                "description": "A JS library",
            },
        )
    )

    result = await service.validate_repository("facebook", "react")

    assert result.is_valid is True
    assert result.owner == "facebook"
    assert result.stars == 200000
    await service.close()


@pytest.mark.asyncio
async def test_validate_repository_not_found_raises_exception():
    service = GitHubService()
    service._client.get = AsyncMock(return_value=_mock_response(404, {}))

    with pytest.raises(GitHubAPIException):
        await service.validate_repository("nonexistent", "repo")
    await service.close()


@pytest.mark.asyncio
async def test_get_changed_files_maps_response_correctly():
    service = GitHubService()
    service._client.get = AsyncMock(
        return_value=_mock_response(
            200,
            [
                {
                    "filename": "auth.py",
                    "status": "added",
                    "additions": 23,
                    "deletions": 0,
                    "changes": 23,
                    "patch": "+def login(): ...",
                }
            ],
        )
    )

    files = await service.get_changed_files("owner", "repo", 1)

    assert len(files) == 1
    assert files[0].filename == "auth.py"
    assert files[0].status == "added"
    await service.close()
