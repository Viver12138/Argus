
from app.services.conversation import ConversationStore


def test_create_and_get_conversation():
    store = ConversationStore()

    conversation = store.create()

    assert conversation.conversation_id
    assert store.get(conversation.conversation_id) is conversation


def test_conversations_have_independent_messages():
    store = ConversationStore()

    first = store.create()
    second = store.create()

    first.messages.append({"role": "user", "content": "Hello"})

    assert first.messages != second.messages
    assert second.messages == []


def test_cannot_delete_busy_conversation():
    store = ConversationStore()
    conversation = store.create()

    conversation.lock.acquire()
    try:
        assert store.delete(conversation.conversation_id) is False
    finally:
        conversation.lock.release()

    assert store.delete(conversation.conversation_id) is True
