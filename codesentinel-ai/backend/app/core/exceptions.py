"""
Custom exception hierarchy for CodeSentinel AI.

All application-specific exceptions inherit from CodeSentinelException,
enabling centralized exception handling in the FastAPI exception handlers.
"""

from typing import Any, Optional


class CodeSentinelException(Exception):
    """Base exception for all CodeSentinel AI application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the base application exception.

        Args:
            message: Human-readable error message.
            status_code: HTTP status code to associate with this error.
            details: Optional structured metadata about the error.
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class GitHubAPIException(CodeSentinelException):
    """Raised when a GitHub REST API call fails or returns an error."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message=message, status_code=502, details=details)


class GroqAPIException(CodeSentinelException):
    """Raised when the Groq AI inference call fails or returns malformed output."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message=message, status_code=502, details=details)


class RepositoryNotFoundException(CodeSentinelException):
    """Raised when a database record cannot be located."""

    def __init__(self, message: str = "Resource not found", details: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message=message, status_code=404, details=details)


class ValidationException(CodeSentinelException):
    """Raised when input validation fails outside of Pydantic's automatic validation."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message=message, status_code=422, details=details)


class ConfigurationException(CodeSentinelException):
    """Raised when required configuration/environment variables are missing or invalid."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message=message, status_code=500, details=details)
