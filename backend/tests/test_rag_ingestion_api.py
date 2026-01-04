import hashlib
import uuid
from dataclasses import dataclass
from typing import Any

import pytest
from app.features.rag.api.deps import get_pdf_ingestion_service
from app.features.rag.services.ingestion.service import PdfIngestionService
from app.main import app


@dataclass
class FakeParsedChunk:
    ordinal: int
    content: str
    page_start: int | None = None
    page_end: int | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class FakeParsedDocument:
    title: str | None
    checksum: str
    metadata: dict[str, Any]
    chunks: list[FakeParsedChunk]


class FakeParser:
    async def parse(self, source_uri: str) -> FakeParsedDocument:
        checksum = hashlib.sha256(source_uri.encode("utf-8")).hexdigest()

        chunks = [
            FakeParsedChunk(ordinal=0, content="Hello world"),
            FakeParsedChunk(ordinal=1, content="More test content"),
            FakeParsedChunk(ordinal=2, content="Final chunk"),
        ]

        return FakeParsedDocument(
            title="Fake PDF",
            checksum=checksum,
            metadata={"source_uri": source_uri},
            chunks=chunks,
        )

async def fake_embed(texts: list[str]) -> list[list[float]]:
    """
    Deterministic 1536-dim embeddings (matches VECTOR(1536)).
    """
    vectors: list[list[float]] = []
    for i, _ in enumerate(texts):
        v = [0.0] * 1536
        v[i % 1536] = 1.0
        vectors.append(v)
    return vectors

@pytest.mark.asyncio
async def test_post_ingestion_runs_returns_run(async_client):
    def override():
        return PdfIngestionService(
            parser=FakeParser(),
            embed_fn=fake_embed,
            embedding_model_version="stub-1536",
            pipeline_version="v0",
        )

    app.dependency_overrides[get_pdf_ingestion_service] = override

    resp = await async_client.post(
        "/rag/ingestion-runs",
        json={
            "run_id": uuid.uuid4().hex,  # or any deterministic string
            "source_uri": "/workspace/tests/fixtures/swagger.pdf",
            "pipeline_version": "v0",
            "requested_by": "spencer",
        },
    )

    assert resp.status_code == 201, resp.text

    data = resp.json()
    assert data["run_id"]
    assert data["status"] in ("SUCCEEDED", "FAILED")

    app.dependency_overrides.clear()
