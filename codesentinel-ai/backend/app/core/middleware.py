"""
Custom ASGI middleware.

Provides request correlation IDs and structured request/response
logging for every HTTP call handled by the application.
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs every request/response cycle with timing.

    Attaches a unique X-Request-ID header to each response for
    traceability across logs, and logs method, path, status, and
    latency for observability.
    """

    def __init__(self, app: ASGIApp) -> None:
        """
        Initialize the middleware.

        Args:
            app: The wrapped ASGI application.
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process an incoming request, logging timing and outcome.

        Args:
            request: The incoming Starlette request.
            call_next: The next handler in the middleware chain.

        Returns:
            Response: The outgoing HTTP response with a request ID header.
        """
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        logger.info(
            "Request started | id={id} | method={method} | path={path}",
            id=request_id,
            method=request.method,
            path=request.url.path,
        )

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "Request failed | id={id} | method={method} | path={path} | duration_ms={duration:.2f}",
                id=request_id,
                method=request.method,
                path=request.url.path,
                duration=duration_ms,
            )
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed | id={id} | method={method} | path={path} | status={status} | duration_ms={duration:.2f}",
            id=request_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration=duration_ms,
        )
        return response
