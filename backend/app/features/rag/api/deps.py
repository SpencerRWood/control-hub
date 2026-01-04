from __future__ import annotations

from app.features.rag.services.ingestion.docling_parser import DoclingPdfParser
from app.features.rag.services.ingestion.service import PdfIngestionService


def get_pdf_ingestion_service() -> PdfIngestionService:
    # TEMP embedding stub — replace with OpenAI/OpenRouter later
    def fake_embed(texts: list[str]) -> list[list[float]]:
        # deterministic, schema-valid vectors (1536)
        out = []
        for t in texts:
            h = hash(t)
            out.append([(h % 997) / 997.0] * 1536)
        return out

    return PdfIngestionService(
        parser=DoclingPdfParser(),
        embed_fn=fake_embed,
        embedding_model_version="stub-1536",
        pipeline_version="v0",
    )
