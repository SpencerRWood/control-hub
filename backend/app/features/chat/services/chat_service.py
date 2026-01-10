# backend/app/features/chat/services/chat_service.py
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.chat.domain.enums import ChatRole
from app.features.chat.domain.schemas import (
    ChatMessageCreate,
    ChatMessageRead,
    ChatPostMessageResponse,
    ChatThreadCreate,
    ChatThreadDetailResponse,
    ChatThreadRead,
)
from app.features.chat.repo import messages as message_repo
from app.features.chat.repo import threads as thread_repo


class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _new_id(self) -> str:
        # Match your existing "string public id" pattern; swap to ULID/UUID7 later if desired.
        return uuid.uuid4().hex

    async def create_thread(self, body: ChatThreadCreate) -> ChatThreadRead:
        thread_id = self._new_id()

        obj = await thread_repo.create(
            self.session,
            thread_id=thread_id,
            created_by=body.created_by,
            title=body.title,
            metadata_json=body.metadata_json,
        )

        await self.session.commit()
        await self.session.refresh(obj)
        return ChatThreadRead.model_validate(obj)

    async def post_message(self, *, thread_id: str, body: ChatMessageCreate) -> ChatPostMessageResponse:
        thread = await thread_repo.get_by_thread_id(self.session, thread_id=thread_id)
        if thread is None:
            raise ValueError(f"ChatThread not found: thread_id={thread_id}")

        user_msg = await message_repo.create(
            self.session,
            message_id=self._new_id(),
            thread_id=thread_id,
            role=ChatRole.USER.value,
            content=body.content,
            metadata_json=body.metadata_json,
        )

        # MVP stub: replace with LLM + (optional) RAG/approvals integration later
        assistant_content = "Acknowledged."
        assistant_metadata: dict[str, Any] = {"stubbed": True}

        assistant_msg = await message_repo.create(
            self.session,
            message_id=self._new_id(),
            thread_id=thread_id,
            role=ChatRole.ASSISTANT.value,
            content=assistant_content,
            citations_json=[],
            tool_calls_json=[],
            tool_results_json=[],
            metadata_json=assistant_metadata,
        )

        # One commit for both messages
        await self.session.commit()
        await self.session.refresh(user_msg)
        await self.session.refresh(assistant_msg)

        return ChatPostMessageResponse(
            user_message=ChatMessageRead.model_validate(user_msg),
            assistant_message=ChatMessageRead.model_validate(assistant_msg),
            proposed_approval_item_id=None,
        )

    async def get_thread_detail(self, *, thread_id: str, limit: int = 200, offset: int = 0) -> ChatThreadDetailResponse:
        thread = await thread_repo.get_by_thread_id(self.session, thread_id=thread_id)
        if thread is None:
            raise ValueError(f"ChatThread not found: thread_id={thread_id}")

        msgs = await message_repo.list_by_thread_id(
            self.session,
            thread_id=thread_id,
            limit=limit,
            offset=offset,
            newest_first=False,
        )

        return ChatThreadDetailResponse(
            thread=ChatThreadRead.model_validate(thread),
            messages=[ChatMessageRead.model_validate(m) for m in msgs],
        )
