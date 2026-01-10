# backend/app/features/chat/repo/threads.py
from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.chat.domain.models import ChatThread


async def get_by_thread_id(session: AsyncSession, *, thread_id: str) -> ChatThread | None:
    q = select(ChatThread).where(ChatThread.thread_id == thread_id)
    return (await session.execute(q)).scalar_one_or_none()


async def create(
    session: AsyncSession,
    *,
    thread_id: str,
    created_by: str,
    title: str | None,
    metadata_json: dict,
) -> ChatThread:
    obj = ChatThread(
        thread_id=thread_id,
        created_by=created_by,
        title=title,
        metadata_json=metadata_json,
    )
    session.add(obj)
    await session.flush()
    return obj


async def list_by_created_by(
    session: AsyncSession,
    *,
    created_by: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> Sequence[ChatThread]:
    q = select(ChatThread)

    if created_by is not None:
        q = q.where(ChatThread.created_by == created_by)

    q = q.order_by(ChatThread.updated_at.desc()).limit(limit).offset(offset)
    return (await session.execute(q)).scalars().all()
