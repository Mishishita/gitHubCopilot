from fastapi.testclient import TestClient
from src.app import app, activities
import urllib.parse

client = TestClient(app)


def test_get_activities_returns_data():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "pytest-user@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    signup_url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    r = client.post(signup_url)
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    r2 = client.post(signup_url)
    assert r2.status_code == 400

    # Unregister
    unregister_url = f"/activities/{urllib.parse.quote(activity)}/unregister?email={urllib.parse.quote(email)}"
    r3 = client.delete(unregister_url)
    assert r3.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregister again should fail
    r4 = client.delete(unregister_url)
    assert r4.status_code == 400
