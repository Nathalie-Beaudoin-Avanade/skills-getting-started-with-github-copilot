from urllib.parse import quote


def signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/signup"


def unregister_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/participants"


def test_get_activities_returns_activity_map(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in payload
    assert isinstance(payload[expected_activity]["participants"], list)


def test_signup_success_adds_normalized_email(client):
    # Arrange
    activity_name = "Chess Club"
    raw_email = "  NewStudent@Mergington.edu  "

    # Act
    response = client.post(signup_path(activity_name), params={"email": raw_email})
    payload = response.json()
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert payload["message"] == "Signed up newstudent@mergington.edu for Chess Club"
    assert "newstudent@mergington.edu" in participants


def test_signup_rejects_duplicate_after_normalization(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email_variant = "  MICHAEL@MERGINGTON.EDU "

    # Act
    response = client.post(signup_path(activity_name), params={"email": duplicate_email_variant})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"

    # Act
    response = client.post(signup_path(activity_name), params={"email": "student@mergington.edu"})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_when_email_is_blank(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(signup_path(activity_name), params={"email": "   "})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Email is required"


def test_unregister_success_removes_matching_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email_variant = "  DANIEL@MERGINGTON.EDU "

    # Act
    response = client.delete(unregister_path(activity_name), params={"email": email_variant})
    payload = response.json()
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert payload["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in [p.strip().lower() for p in participants]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"

    # Act
    response = client.delete(unregister_path(activity_name), params={"email": "student@mergington.edu"})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_400_when_email_is_blank(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(unregister_path(activity_name), params={"email": "   "})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Email is required"


def test_unregister_returns_404_when_participant_not_found(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(unregister_path(activity_name), params={"email": "nobody@mergington.edu"})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"