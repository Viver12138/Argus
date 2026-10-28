import threading
import uuid

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

def utc_now() -> datetime:
    """返回当前的UTC"""
    return datetime.now(timezone.utc)

@dataclass
class Conversation:
    """为同一对话存储数据和执行锁"""
    conversation_id: str
    messages: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=utc_now)
    last_available: datetime = field(default_factory=utc_now)

    # prevent concurrent Agent tasks in the same conversation
    lock: threading.Lock = field(
        default_factory=threading.Lock,
        repr=False,
        compare=False,
    )

    def touch(self) -> None:
        """refresh the last activity time"""
        self.last_available = utc_now()


class ConversationStore:
    """manage all con4sations in process memory"""

    def __init__(self, idle_timeout_minutes: int = 30):
        self._conversations: dict[str, Conversation] = {}

        # protect the shared con4sation dict
        self._lock = threading.Lock()
        self._idle_timeout = timedelta(minutes=idle_timeout_minutes)

    def cleanup_expired(self) -> int:
        """remove expired conversations that no active task"""
        now = utc_now()
        remove_count = 0

        with self._lock:
            expired_ids = [
                conversation_id
                for conversation_id, conversation
                in self._conversations.items()
                if(
                    now - conversation.last_available > self._idle_timeout
                    and not conversation.lock.locked()
                )
            ]

            for conversation_id, conversation in expired_ids:
                self._conversations.pop(conversation_id)
                remove_count += 1

        return remove_count

    def create(self) -> Conversation:
        """ca and store a con4sation with a unique id """
        conversation = Conversation(
            conversation_id= str(uuid.uuid4())
        )

        with self._lock:
            self._conversations[conversation.conversation_id] = conversation

        return conversation

    def get(self, conversation_id: str) -> Conversation | None:
        """return a con4sation or none if it dose not exist"""
        self.cleanup_expired()

        with self._lock:
            return self._conversations.get(conversation_id, None)

    def delete(self, conversation_id: str) -> bool:
        """del a con4sation return F or T"""
        with self._lock:
            conversation = self._conversations.get(conversation_id)

            if conversation is None:
                return False

            if conversation.lock.locked():
                return False

            del self._conversations[conversation_id]
            return True

#shared store instance for the application
store = ConversationStore()