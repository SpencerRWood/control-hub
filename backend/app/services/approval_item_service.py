from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.approval_item import ApprovalItem, ApprovalStatus
from app.repos.approval_item_repo import ApprovalItemRepo
from app.schemas.approval_item import ApprovalItemCreate


class ApprovalItemService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ApprovalItemRepo(session)

    async def create(self, payload: ApprovalItemCreate) -> ApprovalItem:
        item = ApprovalItem(
            title=payload.title,
            description=payload.description,
            type=payload.type,
            payload_json=payload.payload_json,
            status=ApprovalStatus.PENDING,
            requested_by=payload.requested_by,
            assigned_to=payload.assigned_to,
        )
        async with self.session.begin():
            return await self.repo.create(item)

    async def get(self, item_id: int) -> ApprovalItem:
        item = await self.repo.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="ApprovalItem not found")
        return item

    async def list(
        self,
        *,
        status: Optional[ApprovalStatus],
        type: Optional[str],
        created_after: Optional[datetime],
        created_before: Optional[datetime],
        limit: int,
        offset: int,
    ) -> Sequence[ApprovalItem]:
        return await self.repo.list(
            status=status,
            type=type,
            created_after=created_after,
            created_before=created_before,
            limit=limit,
            offset=offset,
        )

    async def approve(self, item_id: int, *, decision_by: str, decision_reason: Optional[str]) -> ApprovalItem:
        async with self.session.begin():
            item = await self.repo.get(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="ApprovalItem not found")
            if item.status != ApprovalStatus.PENDING:
                raise HTTPException(status_code=409, detail="Item is not PENDING")

            item.status = ApprovalStatus.APPROVED
            item.decision_by = decision_by
            item.decision_reason = decision_reason
            item.decision_at = datetime.now(timezone.utc)

        await self.session.refresh(item)
        return item

    async def reject(self, item_id: int, *, decision_by: str, decision_reason: str) -> ApprovalItem:
        async with self.session.begin():
            item = await self.repo.get(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="ApprovalItem not found")
            if item.status != ApprovalStatus.PENDING:
                raise HTTPException(status_code=409, detail="Item is not PENDING")

            item.status = ApprovalStatus.REJECTED
            item.decision_by = decision_by
            item.decision_reason = decision_reason
            item.decision_at = datetime.now(timezone.utc)

        await self.session.refresh(item)
        return item
