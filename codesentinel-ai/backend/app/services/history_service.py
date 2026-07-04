"""
History service.

Provides business logic for listing, retrieving, and deleting
historical Pull Request and Review records — the CRUD/history
surface of the application.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.core.exceptions import RepositoryNotFoundException
from app.repositories.pull_request_repository import PullRequestRepository
from app.repositories.review_repository import ReviewRepository
from app.schemas.history_schemas import PullRequestHistoryItemSchema, ReviewHistoryItemSchema
from app.utils.pagination import PaginatedResponse, PaginationParams


class HistoryService:
    """
    Orchestrates read/delete operations over stored Pull Requests and Reviews.

    Attributes:
        pull_request_repository: Data access for PullRequestModel.
        review_repository: Data access for ReviewModel.
    """

    def __init__(self, db: Session) -> None:
        """
        Initialize the history service with a database session.

        Args:
            db: Active SQLAlchemy session.
        """
        self.pull_request_repository = PullRequestRepository(db)
        self.review_repository = ReviewRepository(db)

    def list_pull_requests(
        self, params: PaginationParams, storage_key: Optional[str] = None
    ) -> PaginatedResponse[PullRequestHistoryItemSchema]:
        """
        List Pull Requests with pagination, including their latest review summary.

        Args:
            params: Pagination parameters (page, page_size).

        Returns:
            PaginatedResponse[PullRequestHistoryItemSchema]: Paginated PR history.
        """
        total = self.pull_request_repository.count()
        records = self.pull_request_repository.list_paginated_with_reviews(
            offset=params.offset, limit=params.limit
        )

        items = []
        for record in records:
            latest_review = max(record.reviews, key=lambda r: r.created_at, default=None)
            items.append(
                PullRequestHistoryItemSchema(
                    id=record.id,
                    repo_owner=record.repo_owner,
                    repo_name=record.repo_name,
                    pr_number=record.pr_number,
                    title=record.title,
                    author=record.author,
                    additions=record.additions,
                    deletions=record.deletions,
                    changed_files_count=record.changed_files_count,
                    html_url=record.html_url,
                    created_at=record.created_at,
                    latest_review_score=latest_review.overall_score if latest_review else None,
                    latest_review_risk=latest_review.risk_level if latest_review else None,
                )
            )

        return PaginatedResponse.build(items=items, total=total, params=params)

    def get_pull_request_detail(self, pull_request_id: int):
        """
        Fetch a single Pull Request with its full review history.

        Args:
            pull_request_id: Primary key of the Pull Request.

        Returns:
            PullRequestModel: The record with reviews eagerly loaded.

        Raises:
            RepositoryNotFoundException: If no matching record exists.
        """
        record = self.pull_request_repository.get_with_reviews(pull_request_id)
        if record is None:
            raise RepositoryNotFoundException(
                message=f"Pull request with id {pull_request_id} not found.",
                details={"pull_request_id": pull_request_id},
            )
        return record

    def delete_pull_request(self, pull_request_id: int) -> None:
        """
        Delete a Pull Request and all its associated reviews (cascade).

        Args:
            pull_request_id: Primary key of the Pull Request to delete.

        Returns:
            None

        Raises:
            RepositoryNotFoundException: If no matching record exists.
        """
        record = self.pull_request_repository.get_by_id(pull_request_id)
        if record is None:
            raise RepositoryNotFoundException(
                message=f"Pull request with id {pull_request_id} not found.",
                details={"pull_request_id": pull_request_id},
            )
        self.pull_request_repository.delete(record)

    def list_reviews(
        self, params: PaginationParams, storage_key: Optional[str] = None
    ) -> PaginatedResponse[ReviewHistoryItemSchema]:
        """
        List Reviews with pagination, including parent Pull Request context.

        Args:
            params: Pagination parameters (page, page_size).

        Returns:
            PaginatedResponse[ReviewHistoryItemSchema]: Paginated review history.
        """
        total = self.review_repository.count()
        records = self.review_repository.list_paginated_with_pull_request(
            offset=params.offset, limit=params.limit
        )

        items = [
            ReviewHistoryItemSchema(
                id=record.id,
                pull_request_id=record.pull_request_id,
                repo_full_name=f"{record.pull_request.repo_owner}/{record.pull_request.repo_name}",
                pr_number=record.pull_request.pr_number,
                pr_title=record.pull_request.title,
                overall_score=record.overall_score,
                risk_level=record.risk_level,
                model_used=record.model_used,
                created_at=record.created_at,
            )
            for record in records
        ]

        return PaginatedResponse.build(items=items, total=total, params=params)

    def delete_review(self, review_id: int) -> None:
        """
        Delete a single Review record.

        Args:
            review_id: Primary key of the Review to delete.

        Returns:
            None

        Raises:
            RepositoryNotFoundException: If no matching record exists.
        """
        record = self.review_repository.get_by_id(review_id)
        if record is None:
            raise RepositoryNotFoundException(
                message=f"Review with id {review_id} not found.", details={"review_id": review_id}
            )
        self.review_repository.delete(record)
