# backend/tests/test_rag_ingestion_service.py
from __future__ import annotations

import hashlib

import pytest
from app.features.rag.domain.models import ChunkEmbedding, Document, DocumentChunk
from app.features.rag.repo.ingestion_runs import get_by_run_id
from app.features.rag.services.ingestion.docling_parser import ParsedDoc
from app.features.rag.services.ingestion.service import PdfIngestionService
from sqlalchemy import func, select


class FakeParser:
    def parse(self, source_uri: str) -> ParsedDoc:
        md = "# Title\n\nHello world.\n\n## Table\n\nA | B\n---|---\n1 | 2\n"
        return ParsedDoc(markdown=md, title="Fake Title")


def fake_embed(texts: list[str]) -> list[list[float]]:
    # deterministic 1536-d vectors
    out = []
    for t in texts:
        h = int(hashlib.sha256(t.encode("utf-8")).hexdigest(), 16)
        val = (h % 997) / 997.0
        out.append([val] * 1536)
    return out


@pytest.mark.asyncio
async def test_ingest_creates_document_chunks_embeddings(db_session):
    svc = PdfIngestionService(
        parser=FakeParser(),
        embed_fn=fake_embed,
        embedding_model_version="stub-1536",
        pipeline_version="v0",
    )

    run_id = await svc.ingest_pdf(
        session=db_session,
        source_uri="/workspace/tests/fixtures/swagger.pdf",
        requested_by="spencer",
    )

    run = await get_by_run_id(db_session, run_id=run_id)
    assert run.status in ("SUCCEEDED", "FAILED")
    assert run.error_message is None
    assert run.stats_json.get("doc_id")

    doc_id = run.stats_json["doc_id"]

    # document exists
    doc = (await db_session.execute(select(Document).where(Document.doc_id == doc_id))).scalar_one()
    assert doc.source_type == "pdf"
    assert doc.checksum

    # chunks exist
    chunk_count = (await db_session.execute(
        select(func.count()).select_from(DocumentChunk).where(DocumentChunk.doc_id == doc_id)
    )).scalar_one()
    assert chunk_count >= 1

    # embeddings exist
    emb_count = (await db_session.execute(
        select(func.count()).select_from(ChunkEmbedding)
        .join(DocumentChunk, DocumentChunk.chunk_id == ChunkEmbedding.chunk_id)
        .where(DocumentChunk.doc_id == doc_id)
        .where(ChunkEmbedding.embedding_model_version == "stub-1536")
    )).scalar_one()
    assert emb_count == chunk_count
