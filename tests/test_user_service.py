from src.services.user_service import create_user

def test_create_user_adds_user_when_input_is_valid():
    users = []

    success, message, new_user = create_user(users, "agent1", " pass123", "Agent")

    assert success is True
    assert new_user == {"name": "agent1", "password": "pass123", "role": "Agent"}
    assert users == [new_user]

def test_create_user_fails_when_username_is_empty():
    users = []

    success, message, new_user = create_user(users, "", "pass123", "Agent")

    assert success is False
    assert new_user is None
    assert users == []

def test_create_user_fails_when_password_is_empty():
    users = []

    success, message, new_user = create_user(users, "agent1", "", "Agent")

    assert success is False
    assert new_user is None
    assert users == []

def test_create_user_fails_when_username_already_exists():
    users = [{"name": "agent1", "password": "pass123", "role": "Agent"}]

    success, message, new_user = create_user(users, "agent1", "otherpass", "Coach")

    assert success is False
    assert new_user is None
    assert len(users) == 1