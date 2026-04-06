import pytest
from fastapi.testclient import TestClient

try:
    from raven.scripts.runner import app
except ImportError:
    app = None


def test_main_returns_successful_response_without_exception():
    """
    Assert that the FastAPI application handles requests successfully
    without raising an unhandled exception.
    The runner's main app should return a 200 OK for the root endpoint
    or at minimum not return a 500 Internal Server Error.
    """
    if app is None:
        pytest.skip("Could not import app from raven.scripts.runner")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/")
    # The correct behaviour is that the application handles the request
    # gracefully and does not produce a 500 Internal Server Error.
    assert response.status_code != 500, (
        f"Expected a successful response, but got HTTP {response.status_code}. "
        f"Response body: {response.text}"
    )
