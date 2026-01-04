from __future__ import annotations

import hashlib
import uuid
from typing import Callable

from app.features.rag.repo import chunks, documents, embeddings, ingestion_runs
from sqlalchemy.ext.asyncio import AsyncSession

from .chunking import chunk_markdown
from .docling_parser import DoclingPdfParser

EmbedFn = Callable[[list[str]], list[list[float]]]


class PdfIngestionService:
    def __init__(
        self,
        *,
        parser: DoclingPdfParser,
        embed_fn: EmbedFn,
        embedding_model_version: str,
        pipeline_version: str = "v0",
    ) -> None:
        self._parser = parser
        self._embed_fn = embed_fn
        self._embedding_model_version = embedding_model_version
        self._pipeline_version = pipeline_version

    async def ingest_pdf(
        self,
        *,
        session: AsyncSession,
        source_uri: str,
        requested_by: str,
    ) -> str:
        run_id = uuid.uuid4().hex
        await ingestion_runs.create(
            session,
            run_id=run_id,
            pipeline_version=self._pipeline_version,
            source_type="pdf",
            source_uri=source_uri,
        )

        stats: dict = {"requested_by": requested_by, "source_uri": source_uri, "pipeline_version": self._pipeline_version}

        try:
            parsed = self._parser.parse(source_uri)
            checksum = hashlib.sha256(parsed.markdown.encode("utf-8")).hexdigest()
            doc_id = checksum[:32]  # stable, compact

            stats["doc_id"] = doc_id

            existing = await documents.get_by_doc_id(session, doc_id=doc_id)
            if existing is None:
                await documents.create(
                    session,
                    doc_id=doc_id,
                    source_type="pdf",
                    source_uri=source_uri,
                    title=parsed.title,
                    checksum=checksum,
                    metadata_json={"parser": "docling"},
                    ingestion_pipeline_version=self._pipeline_version,
                )

            chunk_texts = chunk_markdown(parsed.markdown)
            stats["chunk_count"] = len(chunk_texts)

            chunk_rows = []
            for ordinal, text in enumerate(chunk_texts):
                chunk_rows.append(
                    {
                        "chunk_id": f"{doc_id}:{ordinal}",
                        "ordinal": ordinal,
                        "content": text,
                        "metadata_json": {},
                    }
                )

            created_chunks = await chunks.bulk_create(session, doc_id=doc_id, rows=chunk_rows)

            # embed (MVP: batch all)
            vectors = self._embed_fn([c.content for c in created_chunks])
            if len(vectors) != len(created_chunks):
                raise ValueError("embed_fn returned wrong number of vectors")
            if any(len(v) != 1536 for v in vectors):
                raise ValueError("embed_fn vectors must be length 1536")

            emb_rows = []
            for c, v in zip(created_chunks, vectors, strict=True):
                emb_rows.append(
                    {
                        "chunk_id": c.chunk_id,
                        "embedding_model_version": self._embedding_model_version,
                        "embedding": v,
                    }
                )

            await embeddings.bulk_create(session, rows=emb_rows)

            await ingestion_runs.mark_succeeded(session, run_id=run_id, stats_json=stats)
            await session.commit()
            return run_id

        except Exception as e:
            await ingestion_runs.mark_failed(session, run_id=run_id, error_message=str(e), stats_json=stats)
            await session.commit()
            return run_id
