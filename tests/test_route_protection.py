import pytest

from app import app

@pytest.fixture
def client():
    # Enable Flask testing mode.
    # This gives better error reporting during tests.
    app.config["TESTING"] = True

    # Test secret key used for Flask sessions.
    app.config["SECRET_KEY"] = "test-secret-key"

    # Create Flask test client for route testing.
    with app.test_client() as client:
        yield client

def test_logged_out_user_is_redirected_from_coach_dashboard(client):
    # Simulate a logged-out user requesting a protected route.
    response = client.get("/coach")

    # Protected routes should redirect unauthenticated users.
    assert response.status_code == 302

    # User should be redirected to the login page.
    assert response.headers["Location"] == "/"

def test_agent_cannot_access_coach_dashboard(client):
    # Simulate logged-in Agent session.
    with client.session_transaction() as session:
        session["current_user"] = {
            "name": "Test Agent",
            "role": "Agent",
        }

    # Agent attempts to access coach-only route.
    response = client.get("/coach")

    # Access should be denied via redirect.
    assert response.status_code == 302

    # User should be redirected away from protected route.
    assert response.headers["Location"] == "/"

def test_coach_can_access_coach_dashboard(client):
    # Simulate logged-in Coach session.
    with client.session_transaction() as session:
        session["current_user"] = {
            "name": "Test Coach",
            "role": "Coach",
        }

    # Coach accesses coach-only route.
    response = client.get("/coach")

    # Coach should be allowed to view the dashboard.
    assert response.status_code == 200

def test_coach_cannot_access_agent_dashboard(client):
    # Simulate logged-in Caoch session.
    with client.session_transaction() as session:
        session["current_user"] = {
            "name": "Test Coach",
            "role": "Coach", 
        }

    # Coach attemts to access agent-only route.
    response = client.get("/agent")

    # Coach should be redirected away from protected route.
    assert response.status_code == 302

    # Unauthorized users are redirected to the login/home route.
    assert response.headers["Location"] == "/"

def test_logged_out_user_is_redirected_from_agent_dashboard(client):
    # Simulate logged-out user requesting protected route.
    response = client.get("/agent")

    # Protected routes should redirect unauthorized users.
    assert response.status_code == 302

    # User should be redirected to login/home page.
    assert response.headers["Location"] == "/"