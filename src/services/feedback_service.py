from datetime import datetime

DEFAULT_FEEDBACK_STATUS = "Not Integrated"
PLACEHOLDER_AGENT = "Select Agent"


def create_feedback(agent, feedback_text, timestamp):
    agent = agent.strip() if agent else ""
    feedback_text = feedback_text.strip() if feedback_text else ""

    if agent == "" or agent == PLACEHOLDER_AGENT:
        return False, "Please select an agent.", None

    if feedback_text == "":
        return False, "Feedback text cannot be empty.", None

    feedback = {
        "feedback_id": f"feedback_{int(timestamp)}",
        "agent": agent,
        "feedback_text": feedback_text,
        "status": DEFAULT_FEEDBACK_STATUS,
        "updated_at": datetime.now()
    }

    return True, "Feedback added successfully.", feedback