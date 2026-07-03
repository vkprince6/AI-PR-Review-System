"""
GitHub integration service.

Wraps the GitHub REST API via HTTPX, providing repository validation,
pull request retrieval, and changed-file diff extraction.
"""

from typing import Any, Dict, List

import httpx

from app.core.config import settings
from app.core.exceptions import GitHubAPIException
from app.core.logger import logger
from app.schemas.github_schemas import (
    ChangedFileSchema,
    PullRequestSchema,
    RepositoryValidateResponse,
)


class GitHubService:
    """
    Service for interacting with the GitHub REST API.

    Encapsulates authentication, error handling, and response
    mapping so callers never touch raw HTTP concerns.
    """

    def __init__(self) -> None:
        """Initialize the GitHub service with an authenticated HTTPX client."""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if settings.github_token:
            headers["Authorization"] = f"Bearer {settings.github_token}"

        self._client = httpx.AsyncClient(
            base_url=settings.github_api_base_url,
            headers=headers,
            timeout=settings.github_api_timeout,
        )

    async def close(self) -> None:
        """Close the underlying HTTPX client connection pool."""
        await self._client.aclose()

    async def _get(self, url: str) -> Any:
        """
        Perform an authenticated GET request against the GitHub API.

        Args:
            url: Relative API path (e.g. '/repos/owner/name').

        Returns:
            Any: Parsed JSON response body.

        Raises:
            GitHubAPIException: On network failure, timeout, or non-2xx response.
        """
        try:
            response = await self._client.get(url)
        except httpx.RequestError as exc:
            logger.error("GitHub API network error | url={url} | error={error}", url=url, error=str(exc))
            raise GitHubAPIException(
                message="Failed to reach GitHub API.", details={"url": url, "error": str(exc)}
            ) from exc

        if response.status_code == 404:
            raise GitHubAPIException(
                message="GitHub resource not found.", details={"url": url, "status": 404}
            )
        if response.status_code == 403:
            raise GitHubAPIException(
                message="GitHub API rate limit exceeded or access forbidden.",
                details={"url": url, "status": 403},
            )
        if response.status_code >= 400:
            raise GitHubAPIException(
                message="GitHub API returned an error.",
                details={"url": url, "status": response.status_code, "body": response.text[:500]},
            )

        return response.json()

    async def validate_repository(self, owner: str, repo: str) -> RepositoryValidateResponse:
        """
        Validate that a repository exists and retrieve its basic metadata.

        Args:
            owner: Repository owner/organization.
            repo: Repository name.

        Returns:
            RepositoryValidateResponse: Validation result with repo metadata.

        Raises:
            GitHubAPIException: If the repository cannot be found or accessed.
        """
        data = await self._get(f"/repos/{owner}/{repo}")
        logger.info("Validated GitHub repository | repo={owner}/{repo}", owner=owner, repo=repo)
        return RepositoryValidateResponse(
            is_valid=True,
            owner=data["owner"]["login"],
            name=data["name"],
            default_branch=data.get("default_branch"),
            is_private=data.get("private"),
            stars=data.get("stargazers_count"),
            description=data.get("description"),
        )

    async def get_pull_request(self, owner: str, repo: str, pr_number: int) -> Dict[str, Any]:
        """
        Fetch raw Pull Request metadata from GitHub.

        Args:
            owner: Repository owner/organization.
            repo: Repository name.
            pr_number: Pull request number.

        Returns:
            Dict[str, Any]: Raw GitHub API response for the PR.
        """
        data = await self._get(f"/repos/{owner}/{repo}/pulls/{pr_number}")
        logger.info(
            "Fetched pull request | repo={owner}/{repo} | pr={pr}", owner=owner, repo=repo, pr=pr_number
        )
        return data

    async def get_changed_files(
        self, owner: str, repo: str, pr_number: int
    ) -> List[ChangedFileSchema]:
        """
        Fetch the list of changed files (with diffs) for a Pull Request.

        Args:
            owner: Repository owner/organization.
            repo: Repository name.
            pr_number: Pull request number.

        Returns:
            List[ChangedFileSchema]: Structured changed-file records.
        """
        data = await self._get(f"/repos/{owner}/{repo}/pulls/{pr_number}/files")
        return [
            ChangedFileSchema(
                filename=item["filename"],
                status=item["status"],
                additions=item["additions"],
                deletions=item["deletions"],
                changes=item["changes"],
                patch=item.get("patch"),
            )
            for item in data
        ]

    async def get_full_pull_request(
        self, owner: str, repo: str, pr_number: int
    ) -> PullRequestSchema:
        """
        Fetch and assemble complete Pull Request data: metadata + changed files.

        Args:
            owner: Repository owner/organization.
            repo: Repository name.
            pr_number: Pull request number.

        Returns:
            PullRequestSchema: Fully assembled PR data ready for AI review.
        """
        pr_data = await self.get_pull_request(owner, repo, pr_number)
        changed_files = await self.get_changed_files(owner, repo, pr_number)

        return PullRequestSchema(
            pr_number=pr_data["number"],
            title=pr_data["title"],
            description=pr_data.get("body"),
            author=pr_data["user"]["login"],
            base_branch=pr_data["base"]["ref"],
            head_branch=pr_data["head"]["ref"],
            additions=pr_data.get("additions", 0),
            deletions=pr_data.get("deletions", 0),
            changed_files_count=pr_data.get("changed_files", len(changed_files)),
            html_url=pr_data["html_url"],
            changed_files=changed_files,
        )