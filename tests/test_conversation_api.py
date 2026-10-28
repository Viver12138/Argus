
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_conversation():
    response = client.post("/conversations")

    assert response.status_code == 201

    data = response.json()
    assert data["conversation_id"]
    assert data["status"] == "active"
    assert data["created_at"]


def test_create_two_independent_conversations():
    first = client.post("/conversations").json()
    second = client.post("/conversations").json()

    assert first["conversation_id"] != second["conversation_id"]


def test_delete_conversation():
    created = client.post("/conversations").json()
    conversation_id = created["conversation_id"]

    response = client.delete(
        f"/conversations/{conversation_id}"
    )

    assert response.status_code == 204


def test_delete_nonexistent_conversation():
    response = client.delete(
        "/conversations/not-a-real-conversation"
    )

    assert response.status_code == 404
