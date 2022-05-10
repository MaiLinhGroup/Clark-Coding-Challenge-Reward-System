from fastapi.testclient import TestClient
from pathlib import Path

from main import app

test_client = TestClient(app)

curdir = Path.cwd()

def test_read_root():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_calculate_score():
    response = test_client.post(
        "/confirmed-invitations/scores",
        files={
            "file": ("filename", open(f"{curdir}/test/input.txt", "rb"), "text/plain"),
        }
    )
    assert response.status_code == 200
    assert response.json() == {"A": 1.75, "B": 1.5, "C": 1.0}

def test_calculate_score_with_empty_input():
    response = test_client.post(
        "/confirmed-invitations/scores",
        files={
            "file": ("filename", open(f"{curdir}/test/empty_input.txt", "rb"), "text/plain"),
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Input file is empty"}

def test_calculate_score_only_first_invitation_counts():
    response = test_client.post(
        "/confirmed-invitations/scores",
        files={
            "file": ("filename", open(f"{curdir}/test/only_first_invite_input.txt", "rb"), "text/plain"),
        }
    )
    assert response.status_code == 200
    assert response.json() == {"A": 1.75, "B": 1.5, "C": 1.0}

def test_calculate_score_with_multiple_invitees():
    response = test_client.post(
        "/confirmed-invitations/scores",
        files={
            "file": ("filename", open(f"{curdir}/test/multiple_invitees_input.txt", "rb"), "text/plain"),
        }
    )
    assert response.status_code == 200
    assert response.json() == {"A": 2.25, "B": 2.5, "C": 1.0}

def test_calculate_score_input_out_of_order():
    response = test_client.post(
        "/confirmed-invitations/scores",
        files={
            "file": ("filename", open(f"{curdir}/test/out_of_order_input.txt", "rb"), "text/plain"),
        }
    )
    assert response.status_code == 200
    assert response.json() == {"A": 2.25, "B": 2.5, "C": 1.0}