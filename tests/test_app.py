import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client, mock_activities):
        # Arrange
        expected_count = 2

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success_adds_participant(self, client, mock_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "diana@test.edu"
        initial_count = len(mock_activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in mock_activities[activity_name]["participants"]
        assert len(mock_activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_duplicate_returns_400(self, client, mock_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "alice@test.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client, mock_activities):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "eve@test.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success_removes_participant(self, client, mock_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "alice@test.edu"
        initial_count = len(mock_activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email not in mock_activities[activity_name]["participants"]
        assert len(mock_activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_nonexistent_participant_returns_404(self, client, mock_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "frank@test.edu"  # Not signed up

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_unregister_nonexistent_activity_returns_404(self, client, mock_activities):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "grace@test.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestRedirect:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_index_html(self, client):
        # Arrange
        expected_redirect = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert expected_redirect in response.headers["location"]
