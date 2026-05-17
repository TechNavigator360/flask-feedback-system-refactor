from app import app

# Tests the real login flow through the Flask route.
# This is an integration-style route thet using Flask's test client.
def test_successful_coach_login_redirects_to_coach_dashboard():
    app.config["TESTING"] = True

    with app.test_client() as client:

        # Simulate submitting the login form.
        response = client.post(
            "/",
            data={
                "username": "coach1",
                "password": "pass456",
                "role": "Coach",
            },
            follow_redirects=False,
        )

        # Successful login should redirect to the coach dashboard.
        assert response.status_code == 302
        assert response.headers["Location"] == "/coach"

        # Varify that the session was created correctly.
        with client.session_transaction() as sess:
            assert sess["current_user"]["role"] == "Coach"

# Verifies that an Agent can log in successfully
# and is redirected to the agent dashboard.
def test_successful_agent_login_redirects_to_agent_dashboard():
    app.config["TESTING"] = True

    with app.test_client() as client:

        response = client.post(
            "/",
            data={
                "username": "agent1",
                "password": "pass123",
                "role": "Agent",
            },
            follow_redirects=False,
        )

        assert response.status_code == 302
        assert response.headers["Location"] == "/agent"

        with client.session_transaction() as sess:
            assert sess["current_user"]["role"] == "Agent"

# Verifies that invalid credentials do not create a session
# and redirects the user back to the login page.
def test_invalid_login_redirects_back_to_login():
    app.config["TESTING"] = True

    with app.test_client() as client:

        response = client.post(
            "/",
            data={
                "username": "invalid-user",
                "password": "wrong-password",
                "role": "Coach",
            },
            follow_redirects=False,
        )

        # Invalid login should redirect back to login.
        assert response.status_code == 302
        assert response.headers["Location"] == "/"

        # Session should not contain authenticated user.
        with client.session_transaction() as sess:
            assert "current_user" not in sess

# Verifies that logout clears the authenticated session
# and redirects the user back to the login page. 
def test_logout_clears_session_and_redirects_to_login():
    app.config["TESTING"] = True

    with app.test_client() as client:

        # Create authenticated session
        with client.session_transaction() as sess:
            sess["current_user"] = {
                "name": "Test Coach",
                "role": "Coach",
            }

        response = client.get(
            "/logout",
            follow_redirects=False,
        )    

        # Logout should redirect back to login.
        assert response.status_code == 302
        assert response.headers["Location"] == "/"

        # Session should be cleared.
        with client.session_transaction() as sess:
            assert "current_user" not in sess