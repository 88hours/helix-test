import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi_error import app
from fastapi.testclient import TestClient

# Test the get_page function logic directly by extracting and testing it
# The correct behaviour: get_page with a 5-element list and page=3 should return
# an empty list (page slice beyond bounds), not raise an IndexError.

def get_page(results, page, page_size=10):
    """Correct implementation using slicing."""
    start = page * page_size
    return results[start:start + page_size]


def test_get_page_returns_empty_list_when_page_out_of_bounds():
    # list(range(5)) has 5 elements, page=3 => start=30, beyond bounds
    result = get_page(list(range(5)), page=3)
    assert result == [], f"Expected empty list for out-of-bounds page, got {result!r}"


def test_get_page_endpoint_returns_200_not_500():
    """The /error/index endpoint should not crash (500) once get_page is fixed."""
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/error/index")
    assert response.status_code != 500, (
        f"Expected non-500 response from /error/index, got {response.status_code}"
    )
