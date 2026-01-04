# backend/app/api/rag.py
from __future__ import annotations

from app.db.session_async import get_session
from app.features.rag.api.deps import get_pdf_ingestion_service
from app.features.rag.domain.schemas import (
    AnswerResponseDTO,
    ChunkDTO,
    DocumentDTO,
    FeedbackCreateDTO,
    IngestionRunDTO,
)
from app.features.rag.services.ingestion.service import PdfIngestionService
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

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
async def create_ingestion_run(
    payload: IngestionRunDTO,
    session: AsyncSession = Depends(get_session),
    svc: PdfIngestionService = Depends(get_pdf_ingestion_service),
) -> IngestionRunDTO:
    run_id = await svc.ingest_pdf(
        session=session,
        source_uri=payload.source_uri,
        requested_by=payload.stats_json.get("requested_by", "unknown"),
    )

    # re-fetch to return canonical DB state
    from app.features.rag.repo.ingestion_runs import get_by_run_id

    run = await get_by_run_id(session, run_id=run_id)

    return IngestionRunDTO(
        run_id=run.run_id,
        pipeline_version=run.pipeline_version,
        source_type=run.source_type,
        source_uri=run.source_uri,
        status=run.status,
        stats_json=run.stats_json,
        error_message=run.error_message,
        started_at=run.started_at,
        finished_at=run.finished_at,
    )


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
