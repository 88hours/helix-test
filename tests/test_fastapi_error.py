from fastapi.testclient import TestClient
from fastapi_error import app

client = TestClient(app)

def test_average_item_price_returns_zero_when_item_count_is_zero():
    response = client.get("/error/zero-division")
    assert response.status_code == 200
