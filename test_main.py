from urllib import response
from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)

def test_read_root():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_calculate_score():
    response = test_client.post(
        "/scoring",
        files={
            "file": ("filename", open("input.txt", "rb"), "text/plain"),
        }
    )
    assert response.status_code == 200