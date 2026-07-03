"""
Input validators.

Standalone validation functions used across services to enforce
business rules that go beyond simple Pydantic field constraints.
"""

import re

from app.core.exceptions import ValidationException

_REPO_FULL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")


def validate_repo_full_name(repo_full_name: str) -> tuple[str, str]:
    """
    Validate and split a repository identifier into owner and name.

    Args:
        repo_full_name: Repository identifier in 'owner/repo' format.

    Returns:
        tuple[str, str]: A (owner, repo_name) tuple.

    Raises:
        ValidationException: If the format does not match 'owner/repo'.
    """
    if not _REPO_FULL_NAME_PATTERN.match(repo_full_name):
        raise ValidationException(
            message="Repository must be in 'owner/repo' format.",
            details={"repo_full_name": repo_full_name},
        )
    owner, name = repo_full_name.split("/", maxsplit=1)
    return owner, name


def validate_pr_number(pr_number: int) -> int:
    """
    Validate that a pull request number is a positive integer.

    Args:
        pr_number: The pull request number to validate.

    Returns:
        int: The validated pull request number.

    Raises:
        ValidationException: If pr_number is not a positive integer.
    """
    if pr_number <= 0:
        raise ValidationException(
            message="Pull request number must be a positive integer.",
            details={"pr_number": pr_number},
        )
    return pr_number