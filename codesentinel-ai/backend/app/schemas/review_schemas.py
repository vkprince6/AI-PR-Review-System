"""
AI Review-related Pydantic schemas.

Defines the request contract for triggering a review and the
strict structured-output contract the Groq model must return.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class IssueSeverity(str, Enum):
    """Severity levels for a code review issue."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class IssueCategory(str, Enum):
    """Categorical classification of a code review issue."""

    BUG = "BUG"
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    STYLE = "STYLE"
    BEST_PRACTICE = "BEST_PRACTICE"
    MAINTAINABILITY = "MAINTAINABILITY"


class RiskLevel(str, Enum):
    """Overall risk classification for a Pull Request."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ReviewRequestSchema(BaseModel):
    """Request payload for triggering an AI review of a Pull Request."""

    repo_owner: str = Field(..., min_length=1, examples=["facebook"])
    repo_name: str = Field(..., min_length=1, examples=["react"])
    pr_number: int = Field(..., gt=0, examples=[1])
    storage_key: Optional[str] = Field(default=None, examples=["user-123"])
    github_token: Optional[str] = Field(default=None, examples=["ghp_123"])
    groq_api_key: Optional[str] = Field(default=None, examples=["gsk_123"])

    @field_validator("repo_owner", "repo_name")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        """Trim accidental whitespace from repo identifiers."""
        return value.strip()


class ReviewIssueSchema(BaseModel):
    """A single issue identified by the AI reviewer within the diff."""

    file_path: str
    line_number: Optional[int] = None
    severity: IssueSeverity
    category: IssueCategory
    description: str
    suggestion: str


class ReviewResultSchema(BaseModel):
    """Structured output contract that the Groq model must produce."""

    summary: str = Field(..., description="High-level natural language review summary.")
    overall_score: float = Field(..., ge=0, le=10, description="Code quality score, 0-10.")
    risk_level: RiskLevel
    issues: List[ReviewIssueSchema] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)


class ReviewResponseSchema(BaseModel):
    """Final API response returned after a Pull Request review completes."""

    id: int
    repo_full_name: str
    pr_number: int
    pr_title: str
    review: ReviewResultSchema
    model_used: str
    created_at: datetime

    model_config = {"from_attributes": True}