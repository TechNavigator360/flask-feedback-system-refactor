from src.services.feedback_service import create_feedback
from src.services.feedback_service import (
    create_feedback,
    update_feedback_status
)

def test_create_feedback_returns_feedback_when_feedback_is_valid():
    success, message, feedback = create_feedback("agent1", "Use more empathy", 1234567890)

    assert success is True
    assert feedback["feedback_id"] == "feedback_1234567890"
    assert feedback["agent"] == "agent1"
    assert feedback["feedback_text"] == "Use more empathy"
    assert feedback["status"] == "Not Integrated"

def test_create_feedback_fails_when_agent_is_not_selected():
    success, message, feedback = create_feedback("Select Agent", "Use more empathy", 1234567890)

    assert success is False
    assert feedback is None

def test_create_feedback_fails_when_feedback_test_is_empty():
    success, message, feedback = create_feedback("agent1", "", 1234567890)

    assert success is False
    assert feedback is None

def test_update_feedback_status_updates_feedback_when_status_is_valid():
    feedback_data = [
        {
            "feedback_id": "feedback_1",
            "agent": "agent1",
            "feedback_text": "Use more empathy",
            "status": "Not Integrated",
            "updated_at": "old_timestamp"
        }
    ]
        
    success, message = update_feedback_status(
        feedback_data, 
        "feedback_1",
        "Integrated"
    )

    assert success is True
    assert message == "Feedback status updated successfully."
    assert feedback_data[0]["status"] == "Integrated"
    assert feedback_data[0]["updated_at"] != "old_timestamp"

    def test_update_feedback_status_fails_when_status_is_invalid():
        feedback_data = [
            {
                "feedback_id": "feedback_1",
                "agent": "agent1",
                "feedback_text": "Use more empathy",
                "status": "Not Integrated",
                "updated_at": "old_timestamp"
            }
        ]

        success, message = update_feedback_status(
            feedback_data,
            "feedback_1",
            "Done"
        )

        assert success is False
        assert message == "Invalid feedback status."
        assert feedback_data[0]["status"] == "Not Integrated"