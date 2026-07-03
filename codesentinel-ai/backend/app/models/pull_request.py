"""
Pull Request ORM model.

Represents a snapshot of a GitHub Pull Request at the time
it was submitted for AI review.
"""

from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class PullRequestModel(Base, TimestampMixin):
    """
    Represents a GitHub Pull Request tracked by CodeSentinel AI.

    Attributes:
        id: Primary key.
        repo_owner: GitHub organization/user owning the repository.
        repo_name: Repository name.
        pr_number: Pull request number within the repository.
        title: Pull request title.
        description: Pull request body/description.
        author: GitHub username of the PR author.
        base_branch: Target branch of the PR.
        head_branch: Source branch of the PR.
        additions: Total lines added across the PR.
        deletions: Total lines deleted across the PR.
        changed_files_count: Number of files changed.
        html_url: Public GitHub URL of the PR.
        reviews: Related AI review records.
    """

    __tablename__ = "pull_requests"
    __table_args__ = (
        UniqueConstraint("repo_owner", "repo_name", "pr_number", name="uq_pull_request_identity"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repo_owner: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    repo_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pr_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    base_branch: Mapped[str] = mapped_column(String(255), nullable=False)
    head_branch: Mapped[str] = mapped_column(String(255), nullable=False)
    additions: Mapped[int] = mapped_column(Integer, default=0)
    deletions: Mapped[int] = mapped_column(Integer, default=0)
    changed_files_count: Mapped[int] = mapped_column(Integer, default=0)
    html_url: Mapped[str] = mapped_column(String(500), nullable=False)

    reviews: Mapped[list["ReviewModel"]] = relationship(
        back_populates="pull_request", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<PullRequestModel {self.repo_owner}/{self.repo_name}#{self.pr_number}>"