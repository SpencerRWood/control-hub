# backend/app/features/chat/domain/schemas.py
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.features.chat.domain.enums import ChatRole


class ChatThreadCreate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    created_by: str = Field(min_length=1, max_length=128)
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class ChatThreadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    thread_id: str  
    title: Optional[str]
    created_by: str
    metadata_json: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=20_000)

    # orchestration options (kept in request, optionally persisted in metadata_json)
    use_rag: bool = True
    max_citations: int = Field(default=5, ge=0, le=20)

    metadata_json: dict[str, Any] = Field(default_factory=dict)


class ChatCitationDTO(BaseModel):
    source_id: str = Field(min_length=1, max_length=256)
    title: Optional[str] = None
    source_uri: Optional[str] = None
    deep_link: Optional[str] = None
    loc: Optional[str] = None
    score: Optional[float] = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class ChatToolCallDTO(BaseModel):
    tool_call_id: str = Field(min_length=1, max_length=128)
    name: str = Field(min_length=1, max_length=64)
    args_json: dict[str, Any] = Field(default_factory=dict)


class ChatToolResultDTO(BaseModel):
    tool_call_id: str = Field(min_length=1, max_length=128)
    name: str = Field(min_length=1, max_length=64)
    output_json: dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None


class ChatMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    message_id: str
    thread_id: str
    role: ChatRole
    content: str

    citations_json: list[dict[str, Any]] = Field(default_factory=list)
    tool_calls_json: list[dict[str, Any]] = Field(default_factory=list)
    tool_results_json: list[dict[str, Any]] = Field(default_factory=list)

    metadata_json: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class ChatPostMessageResponse(BaseModel):
    user_message: ChatMessageRead
    assistant_message: ChatMessageRead

    # if your chat can propose an approval item in the same turn
    proposed_approval_item_id: Optional[int] = None


class ChatThreadDetailResponse(BaseModel):
    thread: ChatThreadRead
    messages: list[ChatMessageRead]
