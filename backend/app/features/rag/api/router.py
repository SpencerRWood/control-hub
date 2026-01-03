# backend/app/api/rag.py
from __future__ import annotations

from app.features.rag.api.schemas import (
    AnswerResponseDTO,
    ChunkDTO,
    DocumentDTO,
    FeedbackCreateDTO,
    IngestionRunDTO,
)
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["rag"])

class DocumentCreate(DocumentDTO):
    pass


class ChunkCreate(ChunkDTO):
    pass


class EmbeddingCreate(BaseModel):
    chunk_id: str = Field(..., max_length=160)
    embedding_model_version: str = Field(..., max_length=64)
    embedding: list[float]  


class IngestionRunCreate(IngestionRunDTO):
    pass


@router.post(
    "/documents",
    response_model=DocumentDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_document(payload: DocumentCreate) -> DocumentDTO:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post(
    "/chunks",
    response_model=ChunkDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_chunk(payload: ChunkCreate) -> ChunkDTO:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post(
    "/embeddings",
    status_code=status.HTTP_201_CREATED,
)
def create_embedding(payload: EmbeddingCreate) -> dict:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post(
    "/ingestion-runs",
    response_model=IngestionRunDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_ingestion_run(payload: IngestionRunCreate) -> IngestionRunDTO:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


class RagQueryRequest(BaseModel):
    query_text: str
    embedding_model_version: str = Field(..., max_length=64)
    top_k: int = Field(default=8, ge=1, le=50)


@router.post(
    "/query",
    response_model=AnswerResponseDTO,
    status_code=status.HTTP_200_OK,
)
def rag_query(payload: RagQueryRequest) -> AnswerResponseDTO:
    # Contract-first: return a valid shape even before generation exists.
    return AnswerResponseDTO(
        session_id="stub",
        query_text=payload.query_text,
        answer_text=None,
        embedding_model_version=payload.embedding_model_version,
        answer_model_version=None,
        citations=[],
        created_at=None,
    )


@router.post(
    "/feedback",
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(payload: FeedbackCreateDTO) -> dict:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
