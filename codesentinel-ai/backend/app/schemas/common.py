"""
Common, reusable API schemas.

Provides a generic response envelope so every endpoint in the
system returns a predictable, consistent JSON shape.
"""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Generic API response envelope.

    Attributes:
        success: Whether the request completed successfully.
        message: Optional human-readable status message.
        data: Optional payload of type T.
    """

    success: bool
    message: Optional[str] = None
    data: Optional[T] = None