from src import app as app_module


def test_unregister_successfully_removes_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    before_count = len(app_module.activities[activity_name]["participants"])

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    after_count = len(app_module.activities[activity_name]["participants"])
    assert after_count == before_count - 1
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_when_activity_not_found(client):
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_when_participant_not_found(client):
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}
