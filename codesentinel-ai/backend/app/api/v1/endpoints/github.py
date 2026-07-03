"""
GitHub API router.

Exposes endpoints for validating repositories and inspecting
Pull Request metadata/changed files directly from GitHub.
"""

from fastapi import APIRouter, Depends

from app.core.dependencies import get_github_service
from app.schemas.common import APIResponse
from app.schemas.github_schemas import (
    PullRequestSchema,
    RepositoryValidateRequest,
    RepositoryValidateResponse,
)
from app.services.github_service import GitHubService
from app.utils.validators import validate_repo_full_name

router = APIRouter(prefix="/github", tags=["GitHub"])


@router.post(
    "/validate-repository",
    response_model=APIResponse[RepositoryValidateResponse],
    summary="Validate that a GitHub repository exists and is accessible",
)
async def validate_repository(
    payload: RepositoryValidateRequest,
    github_service: GitHubService = Depends(get_github_service),
) -> APIResponse[RepositoryValidateResponse]:
    """
    Validate a GitHub repository by its full name ('owner/repo').

    Args:
        payload: Request body containing the repository full name.
        github_service: Injected GitHub integration service.

    Returns:
        APIResponse[RepositoryValidateResponse]: Validation result and metadata.
    """
    owner, name = validate_repo_full_name(payload.repo_full_name)
    result = await github_service.validate_repository(owner, name)
    return APIResponse(success=True, message="Repository is valid.", data=result)


@router.get(
    "/{owner}/{repo}/pulls/{pr_number}",
    response_model=APIResponse[PullRequestSchema],
    summary="Retrieve full Pull Request metadata and changed files",
)
async def get_pull_request(
    owner: str,
    repo: str,
    pr_number: int,
    github_service: GitHubService = Depends(get_github_service),
) -> APIResponse[PullRequestSchema]:
    """
    Fetch complete Pull Request data (metadata + changed files) from GitHub.

    Args:
        owner: Repository owner/organization.
        repo: Repository name.
        pr_number: Pull request number.
        github_service: Injected GitHub integration service.

    Returns:
        APIResponse[PullRequestSchema]: Full Pull Request data.
    """
    pr_data = await github_service.get_full_pull_request(owner, repo, pr_number)
    return APIResponse(success=True, data=pr_data)