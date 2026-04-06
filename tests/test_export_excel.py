from fastapi.testclient import TestClient
from fastapi_error import app

client = TestClient(app, raise_server_exceptions=False)

def test_import_error_endpoint_returns_safe_response():
    response = client.get("/error/import")
    # The endpoint should handle the missing openpyxl dependency gracefully
    # and return a proper HTTP response (not crash with a 500 internal server error)
    assert response.status_code != 500
    assert response.status_code in (200, 400, 422, 503)
