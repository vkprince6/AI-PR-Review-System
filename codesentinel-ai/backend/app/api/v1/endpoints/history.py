"""
History API router.

Exposes CRUD/listing endpoints over previously stored Pull Requests
and AI Review records, with pagination support.
"""

from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse, Response

from app.core.dependencies import get_history_service
from app.schemas.common import APIResponse
from app.schemas.history_schemas import PullRequestHistoryItemSchema, ReviewHistoryItemSchema
from app.schemas.review_schemas import ReviewResponseSchema, ReviewResultSchema
from app.services.history_service import HistoryService
from app.services.storage_service import StorageService
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
    x_storage_key: str | None = Header(default=None, alias="x-storage-key"),
) -> APIResponse[PaginatedResponse[PullRequestHistoryItemSchema]]:
    """
    Retrieve a paginated list of Pull Requests that have been reviewed.

    Args:
        params: Pagination query parameters (page, page_size).
        history_service: Injected history service.

    Returns:
        APIResponse[PaginatedResponse[PullRequestHistoryItemSchema]]: Paginated PR history.
    """
    effective_storage_key = (x_storage_key or "default").strip() or "default"
    storage_service = StorageService(storage_key=effective_storage_key)
    items = storage_service.list_pull_requests()
    return APIResponse(
        success=True,
        data=PaginatedResponse.build(items=items, total=len(items), params=params),
    )


@router.get(
    "/pull-requests/{pull_request_id}",
    response_model=APIResponse[ReviewResponseSchema],
    summary="Get a single Pull Request's latest review detail",
)
async def get_pull_request_detail(
    pull_request_id: int,
    history_service: HistoryService = Depends(get_history_service),
    x_storage_key: str | None = Header(default=None, alias="x-storage-key"),
) -> APIResponse[ReviewResponseSchema]:
    """
    Fetch a Pull Request's stored data along with its most recent review.

    Args:
        pull_request_id: Primary key of the Pull Request.
        history_service: Injected history service.

    Returns:
        APIResponse[ReviewResponseSchema]: The PR's latest review, structured.
    """
    effective_storage_key = (x_storage_key or "default").strip() or "default"
    storage_service = StorageService(storage_key=effective_storage_key)
    record = storage_service.get_pull_request_detail(pull_request_id)
    if record is None:
        return JSONResponse(status_code=404, content={"success": False, "error": "Pull request not found."})
    review_result = ReviewResultSchema(
        summary=record["summary"],
        overall_score=record["overall_score"],
        risk_level=record["risk_level"],
        issues=record["issues"],
        strengths=record["strengths"],
    )
    response_data = ReviewResponseSchema(
        id=record["id"],
        repo_full_name=f"{record['repo_owner']}/{record['repo_name']}",
        pr_number=record["pr_number"],
        pr_title=record["pr_title"],
        review=review_result,
        model_used=record["model_used"],
        created_at=record["created_at"],
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
    x_storage_key: str | None = Header(default=None, alias="x-storage-key"),
) -> Response:
    """
    Delete a stored Pull Request record (cascades to its reviews).

    Args:
        pull_request_id: Primary key of the Pull Request to delete.
        history_service: Injected history service.

    Returns:
        Response: An empty 204 No Content response.
    """
    effective_storage_key = (x_storage_key or "default").strip() or "default"
    storage_service = StorageService(storage_key=effective_storage_key)
    deleted = storage_service.delete_pull_request(pull_request_id)
    if not deleted:
        return JSONResponse(status_code=404, content={"success": False, "error": "Pull request not found."})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/reviews",
    response_model=APIResponse[PaginatedResponse[ReviewHistoryItemSchema]],
    summary="List all AI reviews with pagination",
)
async def list_reviews(
    params: PaginationParams = Depends(),
    history_service: HistoryService = Depends(get_history_service),
    x_storage_key: str | None = Header(default=None, alias="x-storage-key"),
) -> APIResponse[PaginatedResponse[ReviewHistoryItemSchema]]:
    """
    Retrieve a paginated list of all AI-generated reviews.

    Args:
        params: Pagination query parameters (page, page_size).
        history_service: Injected history service.

    Returns:
        APIResponse[PaginatedResponse[ReviewHistoryItemSchema]]: Paginated review history.
    """
    effective_storage_key = (x_storage_key or "default").strip() or "default"
    storage_service = StorageService(storage_key=effective_storage_key)
    items = storage_service.list_reviews()
    return APIResponse(
        success=True,
        data=PaginatedResponse.build(items=items, total=len(items), params=params),
    )


@router.delete(
    "/reviews/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single review record",
)
async def delete_review(
    review_id: int,
    history_service: HistoryService = Depends(get_history_service),
    x_storage_key: str | None = Header(default=None, alias="x-storage-key"),
) -> Response:
    """
    Delete a single stored review record.

    Args:
        review_id: Primary key of the Review to delete.
        history_service: Injected history service.

    Returns:
        Response: An empty 204 No Content response.
    """
    effective_storage_key = (x_storage_key or "default").strip() or "default"
    storage_service = StorageService(storage_key=effective_storage_key)
    deleted = storage_service.delete_review(review_id)
    if not deleted:
        return JSONResponse(status_code=404, content={"success": False, "error": "Review not found."})
    return Response(status_code=status.HTTP_204_NO_CONTENT)
