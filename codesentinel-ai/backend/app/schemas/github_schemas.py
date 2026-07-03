"""
GitHub-related Pydantic schemas.

Represents repository validation results, pull request metadata,
and changed-file diffs retrieved from the GitHub REST API.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class RepositoryValidateRequest(BaseModel):
    """Request payload for validating a GitHub repository."""

    repo_full_name: str = Field(
        ..., description="Repository in 'owner/repo' format.", examples=["facebook/react"]
    )


class RepositoryValidateResponse(BaseModel):
    """Response payload confirming repository existence and metadata."""

    is_valid: bool
    owner: str
    name: str
    default_branch: Optional[str] = None
    is_private: Optional[bool] = None
    stars: Optional[int] = None
    description: Optional[str] = None


class ChangedFileSchema(BaseModel):
    """Represents a single file changed within a Pull Request."""

    filename: str
    status: str = Field(..., description="added | modified | removed | renamed")
    additions: int
    deletions: int
    changes: int
    patch: Optional[str] = Field(default=None, description="Unified diff patch, if available.")


class PullRequestSchema(BaseModel):
    """Represents Pull Request metadata retrieved from GitHub."""

    pr_number: int
    title: str
    description: Optional[str] = None
    author: str
    base_branch: str
    head_branch: str
    additions: int
    deletions: int
    changed_files_count: int
    html_url: str
    changed_files: List[ChangedFileSchema] = Field(default_factory=list)