from src import app as app_module


def test_signup_successfully_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    before_count = len(app_module.activities[activity_name]["participants"])

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    after_count = len(app_module.activities[activity_name]["participants"])
    assert after_count == before_count + 1
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_when_activity_not_found(client):
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_when_student_already_signed_up(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_returns_400_when_activity_is_full(client):
    activity_name = "Chess Club"
    email = "overflow@mergington.edu"
    app_module.activities[activity_name]["participants"] = [
        f"student{index}@mergington.edu"
        for index in range(app_module.activities[activity_name]["max_participants"])
    ]

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}
