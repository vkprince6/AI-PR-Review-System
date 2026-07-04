"""
History-related Pydantic schemas.

Represents summarized Pull Request and Review records returned
by the history/listing API endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PullRequestHistoryItemSchema(BaseModel):
    """Summarized Pull Request record for history listings."""

    id: int
    repo_owner: str
    repo_name: str
    pr_number: int
    title: str
    author: str
    additions: int
    deletions: int
    changed_files_count: int
    html_url: str
    created_at: datetime
    latest_review_score: Optional[float] = None
    latest_review_risk: Optional[str] = None

    model_config = {"from_attributes": True}


class ReviewHistoryItemSchema(BaseModel):
    """Summarized Review record for history listings."""

    id: int
    pull_request_id: int
    repo_full_name: str
    pr_number: int
    pr_title: str
    overall_score: float
    risk_level: str
    model_used: str
    created_at: datetime

    model_config = {"from_attributes": True}
