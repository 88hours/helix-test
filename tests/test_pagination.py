import pytest
from send_error import get_page

def test_get_page_returns_empty_list_when_page_exceeds_bounds():
    """Test that get_page returns an empty list when requesting a page beyond available data."""
    data = list(range(5))
    result = get_page(data, page=3)
    assert result == []

def test_get_page_returns_valid_page_within_bounds():
    """Test that get_page correctly returns data for valid pages."""
    data = list(range(10))
    result = get_page(data, page=0)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
