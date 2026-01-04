from __future__ import annotations

from app.features.rag.domain.models import ChunkEmbedding
from sqlalchemy.ext.asyncio import AsyncSession


async def bulk_create(
    session: AsyncSession,
    *,
    rows: list[dict],
) -> None:
    session.add_all([ChunkEmbedding(**r) for r in rows])
    await session.flush()
