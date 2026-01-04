from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.rag.domain.enums import IngestionStatus
from app.features.rag.domain.models import IngestionRun


async def create(
    session: AsyncSession,
    *,
    run_id: str,
    pipeline_version: str,
    source_type: str | None,
    source_uri: str | None,
) -> IngestionRun:
    run = IngestionRun(
        run_id=run_id,
        pipeline_version=pipeline_version,
        source_type=source_type,
        source_uri=source_uri,
        status=IngestionStatus.STARTED.value,
    )
    session.add(run)
    await session.flush()
    return run


async def mark_succeeded(session: AsyncSession, *, run_id: str, stats_json: dict) -> None:
    run = await get_by_run_id(session, run_id=run_id)
    run.status = IngestionStatus.SUCCEEDED.value
    run.stats_json = stats_json
    run.finished_at = datetime.utcnow()


async def mark_failed(session: AsyncSession, *, run_id: str, error_message: str, stats_json: dict | None = None) -> None:
    run = await get_by_run_id(session, run_id=run_id)
    run.status = IngestionStatus.FAILED.value
    run.error_message = error_message
    if stats_json is not None:
        run.stats_json = stats_json
    run.finished_at = datetime.utcnow()


async def get_by_run_id(session: AsyncSession, *, run_id: str) -> IngestionRun:
    q = select(IngestionRun).where(IngestionRun.run_id == run_id)
    run = (await session.execute(q)).scalar_one()
    return run
