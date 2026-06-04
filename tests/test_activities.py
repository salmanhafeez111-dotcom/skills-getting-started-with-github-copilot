"""Unit tests for activities endpoints using AAA (Arrange-Act-Assert) pattern"""


def test_get_activities_returns_all_activities(client):
    """Test GET /activities returns all available activities"""
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Club", "Drama Club", "Debate Team", "Science Club"
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity in expected_activities:
        assert activity in data


def test_get_activities_returns_activity_with_required_fields(client):
    """Test GET /activities returns activities with all required fields"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act
    response = client.get("/activities")
    data = response.json()
    first_activity = data["Chess Club"]

    # Assert
    for field in required_fields:
        assert field in first_activity
    assert isinstance(first_activity["participants"], list)
    assert isinstance(first_activity["max_participants"], int)


def test_signup_for_activity_succeeds_with_valid_email(client):
    """Test POST /activities/{activity}/signup successfully signs up a student"""
    # Arrange
    activity_name = "Chess Club"
    email = "test_student@mergington.edu"
    
    # Get initial participant count
    response_before = client.get("/activities")
    participants_before = len(response_before.json()[activity_name]["participants"])

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert signup_response.status_code == 200
    assert "message" in signup_response.json()
    
    # Verify participant was added
    response_after = client.get("/activities")
    participants_after = len(response_after.json()[activity_name]["participants"])
    assert participants_after == participants_before + 1
    assert email in response_after.json()[activity_name]["participants"]


def test_signup_returns_success_message(client):
    """Test POST /activities/{activity}/signup returns appropriate success message"""
    # Arrange
    activity_name = "Art Club"
    email = "artist@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
