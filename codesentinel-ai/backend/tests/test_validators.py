"""Unit tests for standalone input validators."""

import pytest

from app.core.exceptions import ValidationException
from app.utils.validators import validate_pr_number, validate_repo_full_name


def test_validate_repo_full_name_accepts_valid_format():
    owner, name = validate_repo_full_name("facebook/react")
    assert owner == "facebook"
    assert name == "react"


def test_validate_repo_full_name_rejects_invalid_format():
    with pytest.raises(ValidationException):
        validate_repo_full_name("not-a-valid-repo")


def test_validate_pr_number_accepts_positive_integer():
    assert validate_pr_number(5) == 5


@pytest.mark.parametrize("invalid_value", [0, -1, -100])
def test_validate_pr_number_rejects_non_positive_values(invalid_value):
    with pytest.raises(ValidationException):
        validate_pr_number(invalid_value)
