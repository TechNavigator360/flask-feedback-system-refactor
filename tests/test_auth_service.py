from src.services.auth_service import authenticate_user


def test_authenticate_user_returns_user_when_credentials_are_valid():
    users = [
        {"name": "agent1", "password": "pass123", "role": "Agent"},
        {"name": "coach1", "password": "pass456", "role": "Coach"},
    ]

    result = authenticate_user(users, "agent1", "pass123", "Agent")

    assert result == {"name": "agent1", "password": "pass123", "role": "Agent"}


def test_authenticate_user_returns_none_when_password_is_wrong():
    users = [
        {"name": "agent1", "password": "pass123", "role": "Agent"}
    ]

    result = authenticate_user(users, "agent1", "wrong", "Agent")

    assert result is None


def test_authenticate_user_returns_none_when_role_is_wrong():
    users = [
        {"name": "agent1", "password": "pass123", "role": "Agent"}
    ]

    result = authenticate_user(users, "agent1", "pass123", "Coach")

    assert result is None