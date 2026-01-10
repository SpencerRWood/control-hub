# backend/app/features/chat/repo/messages.py
from __future__ import annotations

from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.chat.domain.models import ChatMessage


async def get_by_message_id(session: AsyncSession, *, message_id: str) -> ChatMessage | None:
    q = select(ChatMessage).where(ChatMessage.message_id == message_id)
    return (await session.execute(q)).scalar_one_or_none()


async def create(
    session: AsyncSession,
    *,
    message_id: str,
    thread_id: str,
    role: str,
    content: str,
    citations_json: list[dict[str, Any]] | None = None,
    tool_calls_json: list[dict[str, Any]] | None = None,
    tool_results_json: list[dict[str, Any]] | None = None,
    metadata_json: dict[str, Any] | None = None,
) -> ChatMessage:
    obj = ChatMessage(
        message_id=message_id,
        thread_id=thread_id,
        role=role,
        content=content,
        citations_json=citations_json or [],
        tool_calls_json=tool_calls_json or [],
        tool_results_json=tool_results_json or [],
        metadata_json=metadata_json or {},
    )
    session.add(obj)
    await session.flush()
    return obj


async def list_by_thread_id(
    session: AsyncSession,
    *,
    thread_id: str,
    limit: int = 50,
    offset: int = 0,
    newest_first: bool = False,
) -> Sequence[ChatMessage]:
    q = select(ChatMessage).where(ChatMessage.thread_id == thread_id)

    if newest_first:
        q = q.order_by(ChatMessage.created_at.desc())
    else:
        q = q.order_by(ChatMessage.created_at.asc())

    q = q.limit(limit).offset(offset)
    return (await session.execute(q)).scalars().all()


async def get_latest_by_thread_id(session: AsyncSession, *, thread_id: str) -> ChatMessage | None:
    q = (
        select(ChatMessage)
        .where(ChatMessage.thread_id == thread_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(1)
    )
    return (await session.execute(q)).scalar_one_or_none()
