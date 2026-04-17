import pytest


def get_page(results, page, page_size=10):
    start = page * page_size
    if start >= len(results):
        return []
    return results[start:start + page_size]


def test_get_page_returns_empty_list_when_page_out_of_bounds():
    """
    When the page offset is beyond the list bounds, get_page should return
    an empty list (or some safe fallback) rather than raising an IndexError.
    """
    result = get_page(list(range(5)), page=3)
    assert result == []
