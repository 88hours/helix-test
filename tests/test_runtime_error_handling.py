from fastapi.testclient import TestClient
from fastapi_error import app, get_db_connection

client = TestClient(app, raise_server_exceptions=False)


def test_runtime_error_endpoint_returns_graceful_error_response():
    """The /error/runtime endpoint should handle pool exhaustion gracefully
    and return a proper HTTP error response, not crash with an unhandled RuntimeError."""
    response = client.get("/error/runtime")
    # The endpoint should return a structured error response (e.g., 503 or 200 with error info)
    # rather than an unhandled 500 crash. A graceful handler returns non-500 status
    # OR returns a JSON body describing the error condition safely.
    assert response.status_code != 500, (
        f"Expected a graceful error response, but got 500 Internal Server Error. "
        f"The pool exhaustion should be handled gracefully."
    )


def test_get_db_connection_returns_none_when_pool_exhausted():
    """get_db_connection should return None (or a safe fallback) when the pool is exhausted,
    instead of raising a RuntimeError."""
    exhausted_pool = {"max": 10, "in_use": 10, "available": 0}
    result = get_db_connection(exhausted_pool)
    assert result is None, (
        f"Expected None when connection pool is exhausted, but got: {result}"
    )
