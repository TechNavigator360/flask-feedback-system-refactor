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

VALID_FEEDBACK_STATUSES = [
    "Not Integrated", 
    "Integrated"
]

def update_feedback_status(feedback_list, feedback_id, new_status):
    if new_status not in VALID_FEEDBACK_STATUSES:
        return False, "Invalid feedback status."
    
    for feedback in feedback_list:
        if feedback["feedback_id"] == feedback_id:
            feedback["status"] = new_status
            feedback["updated_at"] = datetime.now()

            return True, "Feedback status updated successfully."
        
    return False, "Feedback item not found."