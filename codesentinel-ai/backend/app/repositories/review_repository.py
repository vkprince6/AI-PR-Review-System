"""
Review repository.

Provides data access methods specific to ReviewModel, including
fetching the most recent AI review for a given Pull Request and
paginated review history joined with Pull Request context.
"""

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.review import ReviewModel
from app.repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository[ReviewModel]):
    """Repository for CRUD and lookup operations on ReviewModel."""

    def __init__(self, db: Session) -> None:
        """
        Initialize the repository bound to ReviewModel.

        Args:
            db: Active SQLAlchemy session.
        """
        super().__init__(model=ReviewModel, db=db)

    def get_latest_by_pull_request_id(self, pull_request_id: int) -> Optional[ReviewModel]:
        """
        Fetch the most recently created review for a given Pull Request.

        Args:
            pull_request_id: Foreign key to the PullRequestModel.

        Returns:
            Optional[ReviewModel]: The latest review, or None if none exist.
        """
        statement = (
            select(ReviewModel)
            .where(ReviewModel.pull_request_id == pull_request_id)
            .order_by(ReviewModel.created_at.desc())
        )
        return self.db.execute(statement).scalars().first()

    def get_with_pull_request(self, record_id: int) -> Optional[ReviewModel]:
        """
        Fetch a Review along with its parent Pull Request eagerly loaded.

        Args:
            record_id: Primary key of the Review.

        Returns:
            Optional[ReviewModel]: The record with pull_request loaded, or None.
        """
        statement = (
            select(ReviewModel)
            .where(ReviewModel.id == record_id)
            .options(selectinload(ReviewModel.pull_request))
        )
        return self.db.execute(statement).scalar_one_or_none()

    def list_paginated_with_pull_request(self, offset: int, limit: int) -> Sequence[ReviewModel]:
        """
        Retrieve a page of Reviews with their parent Pull Request eagerly loaded.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            Sequence[ReviewModel]: The requested page, newest first.
        """
        statement = (
            select(ReviewModel)
            .options(selectinload(ReviewModel.pull_request))
            .order_by(ReviewModel.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return self.db.execute(statement).scalars().all()
