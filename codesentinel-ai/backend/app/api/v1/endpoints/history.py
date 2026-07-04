"""
History API router.

Exposes CRUD/listing endpoints over previously stored Pull Requests
and AI Review records, with pagination support.
"""

import json

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.core.dependencies import get_history_service
from app.schemas.common import APIResponse
from app.schemas.history_schemas import PullRequestHistoryItemSchema, ReviewHistoryItemSchema
from app.schemas.review_schemas import ReviewResponseSchema, ReviewResultSchema
from app.services.history_service import HistoryService
from app.utils.pagination import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/history", tags=["History"])


@router.get(
    "/pull-requests",
    response_model=APIResponse[PaginatedResponse[PullRequestHistoryItemSchema]],
    summary="List reviewed Pull Requests with pagination",
)
async def list_pull_requests(
    params: PaginationParams = Depends(),
    history_service: HistoryService = Depends(get_history_service),
) -> APIResponse[PaginatedResponse[PullRequestHistoryItemSchema]]:
    """
    Retrieve a paginated list of Pull Requests that have been reviewed.

    Args:
        params: Pagination query parameters (page, page_size).
        history_service: Injected history service.

    Returns:
        APIResponse[PaginatedResponse[PullRequestHistoryItemSchema]]: Paginated PR history.
    """
    result = history_service.list_pull_requests(params)
    return APIResponse(success=True, data=result)


@router.get(
    "/pull-requests/{pull_request_id}",
    response_model=APIResponse[ReviewResponseSchema],
    summary="Get a single Pull Request's latest review detail",
)
async def get_pull_request_detail(
    pull_request_id: int,
    history_service: HistoryService = Depends(get_history_service),
) -> APIResponse[ReviewResponseSchema]:
    """
    Fetch a Pull Request's stored data along with its most recent review.

    Args:
        pull_request_id: Primary key of the Pull Request.
        history_service: Injected history service.

    Returns:
        APIResponse[ReviewResponseSchema]: The PR's latest review, structured.
    """
    record = history_service.get_pull_request_detail(pull_request_id)
    latest_review = max(record.reviews, key=lambda r: r.created_at)

    review_result = ReviewResultSchema(
        summary=latest_review.summary,
        overall_score=latest_review.overall_score,
        risk_level=latest_review.risk_level,
        issues=json.loads(latest_review.issues_json),
        strengths=json.loads(latest_review.strengths_json),
    )

    response_data = ReviewResponseSchema(
        id=latest_review.id,
        repo_full_name=f"{record.repo_owner}/{record.repo_name}",
        pr_number=record.pr_number,
        pr_title=record.title,
        review=review_result,
        model_used=latest_review.model_used,
        created_at=latest_review.created_at,
    )
    return APIResponse(success=True, data=response_data)


@router.delete(
    "/pull-requests/{pull_request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Pull Request and all its associated reviews",
)
async def delete_pull_request(
    pull_request_id: int,
    history_service: HistoryService = Depends(get_history_service),
) -> Response:
    """
    Delete a stored Pull Request record (cascades to its reviews).

    Args:
        pull_request_id: Primary key of the Pull Request to delete.
        history_service: Injected history service.

    Returns:
        Response: An empty 204 No Content response.
    """
    history_service.delete_pull_request(pull_request_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/reviews",
    response_model=APIResponse[PaginatedResponse[ReviewHistoryItemSchema]],
    summary="List all AI reviews with pagination",
)
async def list_reviews(
    params: PaginationParams = Depends(),
    history_service: HistoryService = Depends(get_history_service),
) -> APIResponse[PaginatedResponse[ReviewHistoryItemSchema]]:
    """
    Retrieve a paginated list of all AI-generated reviews.

    Args:
        params: Pagination query parameters (page, page_size).
        history_service: Injected history service.

    Returns:
        APIResponse[PaginatedResponse[ReviewHistoryItemSchema]]: Paginated review history.
    """
    result = history_service.list_reviews(params)
    return APIResponse(success=True, data=result)


@router.delete(
    "/reviews/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single review record",
)
async def delete_review(
    review_id: int,
    history_service: HistoryService = Depends(get_history_service),
) -> Response:
    """
    Delete a single stored review record.

    Args:
        review_id: Primary key of the Review to delete.
        history_service: Injected history service.

    Returns:
        Response: An empty 204 No Content response.
    """
    history_service.delete_review(review_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
