import uuid

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_unregister_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = f"student-{uuid.uuid4().hex}@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )
    activities = client.get("/activities").json()

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]
