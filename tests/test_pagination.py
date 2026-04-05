import pytest
from send_error import get_page


def test_get_page_returns_empty_list_for_out_of_range_page():
    """Test that get_page returns an empty list when page index is out of range."""
    items = list(range(5))
    result = get_page(items, page=3)
    assert result == []


def test_get_page_returns_correct_page_within_range():
    """Test that get_page returns correct results for valid page numbers."""
    items = list(range(5))
    result = get_page(items, page=0)
    assert isinstance(result, list)
    assert len(result) > 0
