from __future__ import annotations

from app.features.rag.domain.models import Document
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_by_doc_id(session: AsyncSession, *, doc_id: str) -> Document | None:
    q = select(Document).where(Document.doc_id == doc_id)
    return (await session.execute(q)).scalar_one_or_none()


async def create(
    session: AsyncSession,
    *,
    doc_id: str,
    source_type: str,
    source_uri: str,
    title: str | None,
    checksum: str | None,
    metadata_json: dict,
    ingestion_pipeline_version: str = "v0",
) -> Document:
    doc = Document(
        doc_id=doc_id,
        source_type=source_type,
        source_uri=source_uri,
        title=title,
        checksum=checksum,
        metadata_json=metadata_json,
        ingestion_pipeline_version=ingestion_pipeline_version,
    )
    session.add(doc)
    await session.flush()
    return doc
