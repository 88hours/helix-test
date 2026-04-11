import pytest
from fastapi.testclient import TestClient
from fastapi_error import app, get_db_connection


def test_get_db_connection_returns_fallback_when_pool_exhausted():
    """get_db_connection should handle an exhausted pool gracefully,
    returning a safe fallback (e.g. None or a dict) instead of raising RuntimeError."""
    pool_state = {"max": 10, "in_use": 10, "available": 0}
    result = get_db_connection(pool_state)
    # The function should return a safe value instead of raising RuntimeError
    assert result is None or isinstance(result, dict)
