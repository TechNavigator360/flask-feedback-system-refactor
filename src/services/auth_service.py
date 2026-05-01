
#future security improvement: replace plaintext passwords

def authenticate_user(users, username, password, role):
    for user in users:
        if (
            user["name"] == username
            and user["password"] == password
            and user["role"] == role
        ):
            return user

    return None