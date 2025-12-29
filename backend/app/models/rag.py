from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# If you're using pgvector-python:
# pip install pgvector
from pgvector.sqlalchemy import Vector


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    doc_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)

    source_type: Mapped[str] = mapped_column(String(32), nullable=False)  # e.g., "markdown"|"pdf"
    source_uri: Mapped[str] = mapped_column(Text, nullable=False)

    title: Mapped[Optional[str]] = mapped_column(String(512))
    checksum: Mapped[Optional[str]] = mapped_column(String(128))  # stable content hash if you want

    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, server_default="{}")

    ingestion_pipeline_version: Mapped[str] = mapped_column(String(64), nullable=False, default="v0")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chunk_id: Mapped[str] = mapped_column(String(160), nullable=False, unique=True, index=True)

    doc_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("documents.doc_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)  # stable per-doc ordering
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # chunk metadata for deterministic deeplinks
    start_ref: Mapped[Optional[str]] = mapped_column(String(128))  # e.g., heading id, or page anchor
    end_ref: Mapped[Optional[str]] = mapped_column(String(128))
    page_start: Mapped[Optional[int]] = mapped_column(Integer)
    page_end: Mapped[Optional[int]] = mapped_column(Integer)

    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, server_default="{}")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    document: Mapped["Document"] = relationship(back_populates="chunks")
    embeddings: Mapped[list["ChunkEmbedding"]] = relationship(back_populates="chunk", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("doc_id", "ordinal", name="uq_document_chunks_doc_id_ordinal"),
    )


class ChunkEmbedding(Base):
    __tablename__ = "chunk_embeddings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    chunk_id: Mapped[str] = mapped_column(
        String(160),
        ForeignKey("document_chunks.chunk_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    embedding_model_version: Mapped[str] = mapped_column(String(64), nullable=False)

    # Decide a single dimension for MVP (make it config-driven later)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    chunk: Mapped["DocumentChunk"] = relationship(back_populates="embeddings")

    __table_args__ = (
        UniqueConstraint("chunk_id", "embedding_model_version", name="uq_chunk_embeddings_chunk_model"),
    )


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    pipeline_version: Mapped[str] = mapped_column(String(64), nullable=False)
    source_type: Mapped[Optional[str]] = mapped_column(String(32))
    source_uri: Mapped[Optional[str]] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(16), nullable=False, default="STARTED")  # STARTED|SUCCEEDED|FAILED

    stats_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, server_default="{}")
    error_message: Mapped[Optional[str]] = mapped_column(Text)

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    retrieval_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    doc_id: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    query_text: Mapped[str] = mapped_column(Text, nullable=False)

    embedding_model_version: Mapped[str] = mapped_column(String(64), nullable=False)
    top_k: Mapped[int] = mapped_column(Integer, nullable=False, default=8)

    results_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, server_default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class RagQuerySession(Base):
    __tablename__ = "rag_queries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    session_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    answer_text: Mapped[Optional[str]] = mapped_column(Text)

    answer_model_version: Mapped[Optional[str]] = mapped_column(String(64))
    embedding_model_version: Mapped[str] = mapped_column(String(64), nullable=False)

    citations_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, server_default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    feedback_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    session_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("rag_queries.session_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    rating: Mapped[Optional[int]] = mapped_column(Integer)  # 1..5
    is_helpful: Mapped[Optional[bool]] = mapped_column(Boolean)
    comment: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


# Optional: explicit metadata indexes beyond column indexes
Index("ix_documents_source_type_created_at", Document.source_type, Document.created_at)
Index("ix_documents_created_at", Document.created_at)
