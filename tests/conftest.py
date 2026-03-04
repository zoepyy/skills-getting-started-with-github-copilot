import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Fixture that resets activities to initial state before each test."""
    app_module.activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the school soccer team and compete in interscholastic matches",
            "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": []
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Painting Workshop": {
            "description": "Explore various painting techniques and create art",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Drama Club": {
            "description": "Rehearse and perform plays and skits",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 30,
            "participants": []
        },
        "Math Olympiad": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Science Research": {
            "description": "Conduct experiments and discuss scientific topics",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        }
    }
    yield


@pytest.fixture
def client():
    """Fixture that provides a TestClient for the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture
def sample_email():
    """Fixture that provides a sample email for testing."""
    return "test@mergington.edu"


@pytest.fixture
def sample_activity():
    """Fixture that provides a sample activity name for testing."""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Fixture that provides a sample email for testing."""
    return "test@mergington.edu"


@pytest.fixture
def sample_activity():
    """Fixture that provides a sample activity name for testing."""
    return "Chess Club"
