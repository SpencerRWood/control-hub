from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence

from app.features.approvals.domain.models import ApprovalItem, ApprovalStatus
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession


class ApprovalItemRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, item: ApprovalItem) -> ApprovalItem:
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def get(self, item_id: int) -> Optional[ApprovalItem]:
        res = await self.session.execute(select(ApprovalItem)\
                                         .where(ApprovalItem.id == item_id))
        return res.scalar_one_or_none()

    async def list(
        self,
        *,
        status: Optional[ApprovalStatus] = None,
        type: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[ApprovalItem]:
        stmt: Select[tuple[ApprovalItem]] = select(ApprovalItem)

        if status is not None:
            stmt = stmt.where(ApprovalItem.status == status)
        if type is not None:
            stmt = stmt.where(ApprovalItem.type == type)
        if created_after is not None:
            stmt = stmt.where(ApprovalItem.created_at >= created_after)
        if created_before is not None:
            stmt = stmt.where(ApprovalItem.created_at <= created_before)

        stmt = stmt.order_by(ApprovalItem.created_at.desc()).limit(limit).offset(offset)
        res = await self.session.execute(stmt)
        return res.scalars().all()
