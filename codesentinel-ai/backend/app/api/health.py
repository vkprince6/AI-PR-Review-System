"""
Health check API router.

Exposes a lightweight endpoint to verify service liveness,
used by load balancers, container orchestrators, and uptime monitors.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Schema for the health check response payload."""

    status: str
    app: str
    env: str
    version: str


@router.get("/health", response_model=HealthResponse, summary="Service health check")
async def health_check() -> HealthResponse:
    """
    Return the current health status of the service.

    Returns:
        HealthResponse: Service status, name, environment, and version.
    """
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        env=settings.app_env,
        version="1.0.0",
    )
