from __future__ import annotations

from app.features.rag.domain.models import DocumentChunk
from sqlalchemy.ext.asyncio import AsyncSession


async def bulk_create(
    session: AsyncSession,
    *,
    doc_id: str,
    rows: list[dict],
) -> list[DocumentChunk]:
    objs = [DocumentChunk(doc_id=doc_id, **r) for r in rows]
    session.add_all(objs)
    await session.flush()
    return objs
