import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture providing a TestClient instance"""
    return TestClient(app)


@pytest.fixture
def mock_activities(monkeypatch):
    """Fixture providing clean test activity data"""
    test_activities = {
        "Chess Club": {
            "description": "Learn chess strategies",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["alice@test.edu", "bob@test.edu"]
        },
        "Programming Class": {
            "description": "Learn programming",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["charlie@test.edu"]
        }
    }
    monkeypatch.setattr("src.app.activities", test_activities)
    return test_activities
