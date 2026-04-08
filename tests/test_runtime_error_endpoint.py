import importlib
import sys
import pytest
from fastapi.testclient import TestClient

# Import the module
sys.path.insert(0, '.')
import fastapi_error
from fastapi_error import app


def test_get_db_connection_returns_none_when_pool_exhausted():
    """When the connection pool is exhausted, get_db_connection should return None
    (a safe fallback) instead of raising a RuntimeError."""
    from fastapi_error import get_db_connection

    pool_config = {"max": 10, "in_use": 10, "available": 0}
    result = get_db_connection(pool_config)
    assert result is None
