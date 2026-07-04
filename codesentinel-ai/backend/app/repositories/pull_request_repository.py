"""
Pull Request repository.

Provides data access methods specific to PullRequestModel, including
lookups by GitHub identity (owner/repo/pr_number) and paginated history.
"""

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.pull_request import PullRequestModel
from app.repositories.base_repository import BaseRepository


class PullRequestRepository(BaseRepository[PullRequestModel]):
    """Repository for CRUD and lookup operations on PullRequestModel."""

    def __init__(self, db: Session) -> None:
        """
        Initialize the repository bound to PullRequestModel.

        Args:
            db: Active SQLAlchemy session.
        """
        super().__init__(model=PullRequestModel, db=db)

    def get_by_identity(
        self, repo_owner: str, repo_name: str, pr_number: int
    ) -> Optional[PullRequestModel]:
        """
        Fetch a Pull Request record by its unique GitHub identity.

        Args:
            repo_owner: Repository owner/organization.
            repo_name: Repository name.
            pr_number: Pull request number.

        Returns:
            Optional[PullRequestModel]: The matching record, if it exists.
        """
        statement = select(PullRequestModel).where(
            PullRequestModel.repo_owner == repo_owner,
            PullRequestModel.repo_name == repo_name,
            PullRequestModel.pr_number == pr_number,
        )
        return self.db.execute(statement).scalar_one_or_none()

    def get_with_reviews(self, record_id: int) -> Optional[PullRequestModel]:
        """
        Fetch a Pull Request along with its full review history, eagerly loaded.

        Args:
            record_id: Primary key of the Pull Request.

        Returns:
            Optional[PullRequestModel]: The record with reviews loaded, or None.
        """
        statement = (
            select(PullRequestModel)
            .where(PullRequestModel.id == record_id)
            .options(selectinload(PullRequestModel.reviews))
        )
        return self.db.execute(statement).scalar_one_or_none()

    def list_paginated_with_reviews(
        self, offset: int, limit: int
    ) -> Sequence[PullRequestModel]:
        """
        Retrieve a page of Pull Requests with their reviews eagerly loaded.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            Sequence[PullRequestModel]: The requested page, newest first.
        """
        statement = (
            select(PullRequestModel)
            .options(selectinload(PullRequestModel.reviews))
            .order_by(PullRequestModel.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return self.db.execute(statement).scalars().all()

    def upsert(self, pull_request: PullRequestModel) -> PullRequestModel:
        """
        Insert a new Pull Request record, or update it if one already exists.

        Args:
            pull_request: A transient PullRequestModel instance with fresh data.

        Returns:
            PullRequestModel: The persisted, up-to-date record.
        """
        existing = self.get_by_identity(
            pull_request.repo_owner, pull_request.repo_name, pull_request.pr_number
        )
        if existing:
            existing.title = pull_request.title
            existing.description = pull_request.description
            existing.author = pull_request.author
            existing.base_branch = pull_request.base_branch
            existing.head_branch = pull_request.head_branch
            existing.additions = pull_request.additions
            existing.deletions = pull_request.deletions
            existing.changed_files_count = pull_request.changed_files_count
            existing.html_url = pull_request.html_url
            self.db.commit()
            self.db.refresh(existing)
            return existing

        return self.create(pull_request)
