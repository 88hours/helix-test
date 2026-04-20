from fastapi.testclient import TestClient
from fastapi_error import app

client = TestClient(app)


def test_get_page_returns_empty_or_safe_when_page_out_of_bounds():
    """
    When get_page() is called with a page index that goes beyond the list bounds,
    it should return a safe result (empty list or empty result) rather than raising
    an IndexError. The /error/index endpoint should return a 200 response.
    """
    response = client.get("/error/index")
    assert response.status_code == 200
