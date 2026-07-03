"""
CodeSentinel AI — Application Entrypoint.

Bootstraps the FastAPI application: configures logging, database,
middleware, global exception handlers, and mounts versioned API routers.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.database import init_db
from app.core.exceptions import CodeSentinelException
from app.core.logger import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application startup and shutdown lifecycle events.

    Args:
        app: The FastAPI application instance.

    Yields:
        None
    """
    configure_logging()
    logger.info("Starting {app_name} in {env} mode", app_name=settings.app_name, env=settings.app_env)
    init_db()
    logger.info("Database initialized.")
    yield
    logger.info("Shutting down {app_name}", app_name=settings.app_name)


def create_application() -> FastAPI:
    """
    Application factory that constructs and configures the FastAPI instance.

    Returns:
        FastAPI: The fully configured application instance.
    """
    app = FastAPI(
        title=settings.app_name,
        description="Enterprise AI Pull Request Review Assistant",
        version="1.0.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    register_routers(app)

    return app


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers on the FastAPI application.

    Args:
        app: The FastAPI application instance.

    Returns:
        None
    """

    @app.exception_handler(CodeSentinelException)
    async def codesentinel_exception_handler(
        request: Request, exc: CodeSentinelException
    ) -> JSONResponse:
        """Handle all custom application exceptions with structured JSON responses."""
        logger.error(
            "Handled exception | path={path} | message={message} | details={details}",
            path=request.url.path,
            message=exc.message,
            details=exc.details,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch-all handler for unexpected exceptions."""
        logger.exception("Unhandled exception at path={path}", path=request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "An unexpected internal error occurred.",
                "details": {},
            },
        )


def register_routers(app: FastAPI) -> None:
    """
    Mount all API routers onto the application.

    Args:
        app: The FastAPI application instance.

    Returns:
        None
    """
    app.include_router(health_router)
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


app = create_application()