"""
AI Review API router.

Exposes endpoints for triggering an AI-powered Pull Request review
and retrieving previously generated review results.
"""

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_review_service
from app.core.exceptions import RepositoryNotFoundException
from app.schemas.common import APIResponse
from app.schemas.review_schemas import ReviewRequestSchema, ReviewResponseSchema, ReviewResultSchema
from app.services.review_service import ReviewService
from app.services.storage_service import StorageService

router = APIRouter(prefix="/review", tags=["AI Review"])


@router.post(
    "/analyze",
    response_model=APIResponse[ReviewResponseSchema],
    summary="Trigger an AI-powered code review for a Pull Request",
)
async def analyze_pull_request(
    payload: ReviewRequestSchema,
    review_service: ReviewService = Depends(get_review_service),
    x_storage_key: str | None = Header(default=None, alias="x-storage-key"),
) -> APIResponse[ReviewResponseSchema]:
    """
    Run the full AI review pipeline against a GitHub Pull Request.

    Args:
        payload: Repository owner, name, and PR number to review.
        review_service: Injected review orchestration service.

    Returns:
        APIResponse[ReviewResponseSchema]: The structured AI review result.
    """
    try:
        result = await review_service.review_pull_request(payload, storage_key=x_storage_key)
    except Exception as exc:
        error_message = str(exc)
        return JSONResponse(
            status_code=502,
            content={
                "success": False,
                "error": error_message,
                "details": {
                    "repo": f"{payload.repo_owner}/{payload.repo_name}",
                    "pr_number": payload.pr_number,
                    "exception_type": exc.__class__.__name__,
                },
            },
        )

    return APIResponse(success=True, message="Review completed successfully.", data=result)


@router.get(
    "/{review_id}",
    response_model=APIResponse[ReviewResponseSchema],
    summary="Retrieve a previously generated review by its ID",
)
async def get_review(
    review_id: int,
    db: Session = Depends(get_db),
) -> APIResponse[ReviewResponseSchema]:
    """
    Fetch a stored AI review by its database ID.

    Args:
        review_id: Primary key of the review record.
        db: Injected database session.

    Returns:
        APIResponse[ReviewResponseSchema]: The stored review result.

    Raises:
        RepositoryNotFoundException: If no review exists with the given ID.
    """
    storage_service = StorageService(storage_key="default")
    review = storage_service.get_review(review_id)

    if review is None:
        raise RepositoryNotFoundException(
            message=f"Review with id {review_id} not found.", details={"review_id": review_id}
        )

    review_result = ReviewResultSchema(
        summary=review["summary"],
        overall_score=review["overall_score"],
        risk_level=review["risk_level"],
        issues=review["issues"],
        strengths=review["strengths"],
    )

    response_data = ReviewResponseSchema(
        id=review["id"],
        repo_full_name=f"{review['repo_owner']}/{review['repo_name']}",
        pr_number=review["pr_number"],
        pr_title=review["pr_title"],
        review=review_result,
        model_used=review["model_used"],
        created_at=review["created_at"],
    )
    return APIResponse(success=True, data=response_data)