"""
API v1 router aggregator.

Combines all version-1 domain routers (GitHub, Review, History) into
a single router mounted under the application's API version prefix.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import github, history, review

api_v1_router = APIRouter()
api_v1_router.include_router(github.router)
api_v1_router.include_router(review.router)
api_v1_router.include_router(history.router)
