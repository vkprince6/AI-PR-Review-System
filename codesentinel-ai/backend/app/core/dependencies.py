"""
FastAPI dependency injection wiring.

Centralizes construction of services so route handlers remain thin
and dependencies can be swapped/mocked easily in tests.
"""

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.github_service import GitHubService
from app.services.groq_service import GroqService
from app.services.review_service import ReviewService


async def get_github_service() -> AsyncGenerator[GitHubService, None]:
    """
    Provide a GitHubService instance, ensuring its HTTPX client is closed after use.

    Yields:
        GitHubService: An initialized GitHub integration service.
    """
    service = GitHubService()
    try:
        yield service
    finally:
        await service.close()


def get_groq_service() -> GroqService:
    """
    Provide a GroqService instance.

    Returns:
        GroqService: An initialized Groq AI integration service.
    """
    return GroqService()


def get_review_service(
    db: Session = Depends(get_db),
    github_service: GitHubService = Depends(get_github_service),
    groq_service: GroqService = Depends(get_groq_service),
) -> ReviewService:
    """
    Provide a fully-wired ReviewService instance.

    Args:
        db: Request-scoped SQLAlchemy session.
        github_service: GitHub integration service.
        groq_service: Groq AI integration service.

    Returns:
        ReviewService: An initialized review orchestration service.
    """
    return ReviewService(github_service=github_service, groq_service=groq_service, db=db)