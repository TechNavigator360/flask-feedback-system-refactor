from src.database.db import db
from src.database.models import User

def find_user_by_user_name(username):
    # Find a user by username in database.
    return User.query.filter_by(username=username).first()

def create_user(username, password, role):
    # Create a user in the database.
    # Repository handles persistence.
    user = User(
        username=username,
        password=password,
        role=role,
    )

    db.session.add(user)
    db.session.commit()

    return user