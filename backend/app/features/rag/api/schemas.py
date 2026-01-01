from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class DocumentDTO(BaseModel):
    doc_id: str = Field(..., max_length=128)
    source_type: str = Field(..., max_length=32)
    source_uri: str
    title: Optional[str] = None
    checksum: Optional[str] = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    ingestion_pipeline_version: str = Field(default="v0", max_length=64)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChunkDTO(BaseModel):
    chunk_id: str = Field(..., max_length=160)
    doc_id: str = Field(..., max_length=128)
    ordinal: int
    content: str
    start_ref: Optional[str] = None
    end_ref: Optional[str] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None


class IngestionRunDTO(BaseModel):
    run_id: str = Field(..., max_length=64)
    pipeline_version: str = Field(..., max_length=64)
    source_type: Optional[str] = Field(default=None, max_length=32)
    source_uri: Optional[str] = None
    status: str = Field(default="STARTED", max_length=16)
    stats_json: dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class RetrievalResultDTO(BaseModel):
    chunk_id: str
    doc_id: str
    score: float
    snippet: Optional[str] = None
    source_uri: Optional[str] = None
    deep_link: Optional[str] = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class AnswerResponseDTO(BaseModel):
    session_id: str = Field(..., max_length=64)
    query_text: str
    answer_text: Optional[str] = None
    embedding_model_version: str = Field(..., max_length=64)
    answer_model_version: Optional[str] = Field(default=None, max_length=64)
    citations: list[RetrievalResultDTO] = Field(default_factory=list)
    created_at: Optional[datetime] = None


class FeedbackCreateDTO(BaseModel):
    session_id: str = Field(..., max_length=64)
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    is_helpful: Optional[bool] = None
    comment: Optional[str] = None
