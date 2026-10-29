from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

class ChatRequest(BaseModel):
    """validate incoming chat request"""

    model_config = ConfigDict(str_strip_whitespace=True)

    conversation_id: UUID = Field(
        ...,
        description="the id of the existing conversation",
    )

    message:str = Field(
        ...,
        min_length=1,
        max_length=8000,
        description="the user's message",
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        """reject messages that are empty after trimming whitespace"""
        if not value:
            raise ValueError("message cannot be empty")
        return value

class ChatResponse(BaseModel):
    """standard response structure for a chat task"""
    model_config = ConfigDict(extra="forbid")

    task_id: UUID
    conversation_id: UUID
    status: Literal[
        "pending",
        "running",
        "completed",
        "failed",
    ]
    answer: str | None = None
    error: str | None = None