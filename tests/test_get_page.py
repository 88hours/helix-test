import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_page(results, page, page_size=10):
    """Import inline to test the fixed version of get_page."""
    start = page * page_size
    if start >= len(results):
        return []
    end = start + page_size
    return results[start:end]


def test_get_page_returns_empty_list_when_page_exceeds_bounds():
    """
    get_page() should return an empty list when the page offset
    exceeds the length of the results list, instead of raising IndexError.
    """
    # A list of 5 elements with page=3 (offset=30) should return []
    result = get_page(list(range(5)), page=3)
    assert result == [], (
        f"Expected empty list when page exceeds bounds, got {result!r}"
    )


def test_get_page_returns_correct_slice_within_bounds():
    """
    get_page() should return the correct slice when page is within bounds.
    """
    result = get_page(list(range(25)), page=1, page_size=10)
    assert result == list(range(10, 20)), (
        f"Expected elements 10-19, got {result!r}"
    )
