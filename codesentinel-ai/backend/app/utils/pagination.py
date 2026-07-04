"""
Pagination utilities.

Provides reusable pagination request/response helpers so every
list-style endpoint in the system behaves consistently.
"""

from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Query parameters controlling pagination for list endpoints."""

    page: int = Field(default=1, ge=1, description="1-indexed page number.")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page (max 100).")

    @property
    def offset(self) -> int:
        """Compute the SQL OFFSET value from page and page_size."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Compute the SQL LIMIT value (alias of page_size)."""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated list response envelope."""

    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def build(cls, items: List[T], total: int, params: PaginationParams) -> "PaginatedResponse[T]":
        """
        Construct a PaginatedResponse from raw items and pagination params.

        Args:
            items: The page of items retrieved from the database.
            total: Total number of matching records across all pages.
            params: The pagination parameters used for this query.

        Returns:
            PaginatedResponse[T]: A fully populated paginated envelope.
        """
        total_pages = (total + params.page_size - 1) // params.page_size if total > 0 else 0
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
        )
