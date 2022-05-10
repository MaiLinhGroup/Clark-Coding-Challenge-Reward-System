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
    assert response.json() == {"A": 1.75, "B": 1.5, "C": 1.0}

def test_calculate_score_with_empty_input():
    response = test_client.post(
        "/scoring",
        files={
            "file": ("filename", open("empty_input.txt", "rb"), "text/plain"),
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Input file is empty"}

def test_calculate_score_only_first_invitation_counts():
    response = test_client.post(
        "/scoring",
        files={
            "file": ("filename", open("only_first_invite_input.txt", "rb"), "text/plain"),
        }
    )
    assert response.status_code == 200
    assert response.json() == {"A": 1.75, "B": 1.5, "C": 1.0}