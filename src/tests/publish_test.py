from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_publish_item():
    payload = {
        "name": "Test Name",
        "description": "Test Description"
    }
    response = client.post("/publish/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["name"] == payload["name"]
    assert data["item"]["description"] == payload["description"]
    assert data["status"] == "published"