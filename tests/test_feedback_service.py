from src.services.feedback_service import create_feedback

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