import os
import sys

# Make the project root importable when running this script directly.
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from app import app
from src.database.db import db
from src.database.models import User
from src.repositories.csv_repository import load_data


def seed_users_from_csv():
    # Seed user records from existing CSV file into SQLite.
    # Migration helper only.
    users = load_data()[0]

    #print(type(data))
    #print(data[:2])
    #return

    created_count = 0
    skipped_count = 0

    for user_data in users: 

        username = user_data.get("name")
        password = user_data.get("password")
        role = user_data.get("role")

        if not username:
            skipped_count += 1
            continue

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            skipped_count += 1
            continue

        user = User(
            username=username,
            password=password,
            role=role,
        )

        db.session.add(user)
        created_count += 1

    db.session.commit()

    print(f"Seed complete: {created_count} users created, {skipped_count} users skipped")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_users_from_csv()

