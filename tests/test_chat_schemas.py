
import pytest
from pydantic import ValidationError

from app.schemas.chat import ChatRequest, ChatResponse


VALID_CONVERSATION_ID = "12345678-1234-5678-1234-567812345678"


def test_valid_chat_request():
    request = ChatRequest(
        conversation_id=VALID_CONVERSATION_ID,
        message="  Hello Agent!  ",
    )

    assert request.message == "Hello Agent!"
    assert str(request.conversation_id) == VALID_CONVERSATION_ID


def test_empty_message_is_rejected():
    with pytest.raises(ValidationError):
        ChatRequest(
            conversation_id=VALID_CONVERSATION_ID,
            message="   ",
        )


def test_message_over_8000_characters_is_rejected():
    with pytest.raises(ValidationError):
        ChatRequest(
            conversation_id=VALID_CONVERSATION_ID,
            message="a" * 8001,
        )


def test_invalid_conversation_id_is_rejected():
    with pytest.raises(ValidationError):
        ChatRequest(
            conversation_id="not-a-uuid",
            message="Hello",
        )


def test_chat_response():
    response = ChatResponse(
        task_id="12345678-1234-5678-1234-567812345679",
        conversation_id=VALID_CONVERSATION_ID,
        status="completed",
        answer="Hello!",
        error=None,
    )

    assert response.status == "completed"
    assert response.answer == "Hello!"


def test_invalid_status_is_rejected():
    with pytest.raises(ValidationError):
        ChatResponse(
            task_id="12345678-1234-5678-1234-567812345679",
            conversation_id=VALID_CONVERSATION_ID,
            status="unknown",
        )
