"""
Logging configuration module.

Sets up Loguru with console and file sinks, structured formatting,
and log rotation suitable for enterprise/production use.
"""

import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings


def configure_logging() -> None:
    """
    Configure Loguru logging sinks for the application.

    Removes the default handler and installs:
        - A colorized console sink for local development readability.
        - A rotating file sink for persistent, production-grade logs.

    Returns:
        None
    """
    logger.remove()

    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        format=console_format,
        level=settings.log_level,
        colorize=True,
        backtrace=settings.debug,
        diagnose=settings.debug,
    )

    log_file = Path(settings.log_file_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        backtrace=True,
        diagnose=False,
        enqueue=True,
    )

    logger.info(
        "Logging configured | env={env} | level={level}",
        env=settings.app_env,
        level=settings.log_level,
    )


__all__ = ["logger", "configure_logging"]
