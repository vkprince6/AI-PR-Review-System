"""Unit tests for pagination utility classes."""

from app.utils.pagination import PaginatedResponse, PaginationParams


def test_pagination_params_computes_offset_and_limit():
    params = PaginationParams(page=3, page_size=10)
    assert params.offset == 20
    assert params.limit == 10


def test_paginated_response_build_computes_total_pages_correctly():
    params = PaginationParams(page=1, page_size=10)
    response = PaginatedResponse.build(items=[1, 2, 3], total=25, params=params)
    assert response.total_pages == 3
    assert response.total == 25
    assert response.page == 1


def test_paginated_response_build_handles_zero_total():
    params = PaginationParams(page=1, page_size=10)
    response = PaginatedResponse.build(items=[], total=0, params=params)
    assert response.total_pages == 0
