def test_get_activities_returns_all_activities(client):
    expected_activity = "Chess Club"

    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert expected_activity in payload
    assert "participants" in payload[expected_activity]
