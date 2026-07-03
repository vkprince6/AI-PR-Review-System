"""
Review repository.

Provides data access methods specific to ReviewModel, including
fetching the most recent AI review for a given Pull Request.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

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