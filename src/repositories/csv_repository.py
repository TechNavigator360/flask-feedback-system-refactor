import csv
from datetime import datetime
import logging

def load_data(csv_path="data.csv"):

    """
    Loads user, feedback, and report data from a CSV file.

    - Parses rows based on the "type" field (user, feedback, or report).
    - Converts timestamps (`updated_at`) to datetime objects or skips malformed entries with a warning.
    - Returns three lists:
        - users: List of user dictionaries with name, password, and role.
        - feedback_data: List of feedback dictionaries with details and timestamps.
        - report_data: List of report dictionaries with agent-specific performance data.
    - Parameters:
        - csv_path: Path to the input CSV file (default: "data.csv").
    """

    users = []
    feedback_data = []
    report_data = []

    with open(csv_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_type = row.get("type")
            if row_type == "user":
                users.append({
                    "name": row["username"],
                    "password": row["password"],
                    "role": row["role"]
                })
            elif row_type == "feedback":
                updated_at = row["updated_at"]
                try:
                    if "-" in updated_at and ":" in updated_at:
                        updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
                    else:
                        updated_at = datetime.fromtimestamp(float(updated_at))
                except (ValueError, TypeError):
                    logging.warning(f"Skipped entry with malformed or missing updated_at: {row}")
                    continue

                feedback_data.append({
                    "feedback_id": row["feedback_id"],
                    "agent": row["agent"],
                    "feedback_text": row["feedback_text"],
                    "status": row["status"],
                    "updated_at": updated_at
                })
            elif row_type == "report":
                report_data.append({
                    "report_id": row["report_id"],
                    "date": row["date"],
                    "agent": row["agent"],
                    "feedback_applied": row["feedback_applied"]
                })

    return users, feedback_data, report_data

def save_data(users, feedback_data, report_data, csv_path="data.csv"):

    """
    Saves user, feedback, and report data to a CSV file.

    - Writes data for users, feedback, and reports into separate rows in a single CSV.
    - Converts `updated_at` timestamps to a standardized string format.
    - Ensures fields not relevant to a particular data type are left blank.
    - Parameters:
        - users: List of dictionaries representing user data.
        - feedback_data: List of dictionaries representing feedback data.
        - report_data: List of dictionaries representing report data.
        - csv_path: Filepath for the CSV file (default: "data.csv").
    """

    with open(csv_path, mode="w", newline="") as file:
        fieldnames = ["type", "username", "password", "role", "feedback_id", "agent", "feedback_text", "status", "report_id", "date", "feedback_applied", "updated_at"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Write users
        for user in users:
            writer.writerow({
                "type": "user",
                "username": user.get("name", ""),
                "password": user.get("password", ""),
                "role": user.get("role", ""),
                "feedback_id": "",
                "agent": "",
                "feedback_text": "",
                "status": "",
                "report_id": "",
                "date": "",
                "feedback_applied": "",
                "updated_at": ""
            })

        # Write feedback
        for feedback in feedback_data:
            # Convert `updated_at` to a string, whether it's a datetime or a float
            if isinstance(feedback["updated_at"], datetime):
                updated_at_str = feedback["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(feedback["updated_at"], float):
                updated_at_str = datetime.fromtimestamp(feedback["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
            else:
                updated_at_str = feedback["updated_at"]  # Fallback if it’s already a string

            feedback_entry = {
                "type": "feedback",
                "username": "",  # Blank fields not used for feedback entries
                "password": "",
                "role": "",
                "feedback_id": feedback.get("feedback_id", ""),
                "agent": feedback.get("agent", ""),
                "feedback_text": feedback.get("feedback_text", ""),
                "status": feedback.get("status", ""),
                "report_id": "",
                "date": "",
                "feedback_applied": "",
                "updated_at": updated_at_str
            }
            writer.writerow(feedback_entry)

        # Write reports
        for report in report_data:
            writer.writerow({
                "type": "report",
                "username": "",
                "password": "",
                "role": "",
                "feedback_id": "",
                "agent": report.get("agent", ""),
                "feedback_text": "",
                "status": "",
                "report_id": report.get("report_id", ""),
                "date": report.get("date", ""),
                "feedback_applied": report.get("feedback_applied", ""),
                "updated_at": ""
            })