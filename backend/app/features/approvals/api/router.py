from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.db.session_async import get_session
from app.features.approvals.api.schemas import (
    ApprovalItemApprove,
    ApprovalItemCreate,
    ApprovalItemRead,
    ApprovalItemReject,
)
from app.features.approvals.domain.models import ApprovalStatus
from app.features.approvals.services.approval_item_service import ApprovalItemService
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["approvals"])


def get_service(session: AsyncSession = Depends(get_session)) -> ApprovalItemService:
    return ApprovalItemService(session)


@router.post("", response_model=ApprovalItemRead, status_code=201)
async def create_approval_item(payload: ApprovalItemCreate, 
                               svc: ApprovalItemService = Depends(get_service)):
    return await svc.create(payload)

@router.get("", response_model=list[ApprovalItemRead])
async def list_approval_items(
    status: Optional[ApprovalStatus] = Query(default=None),
    type: Optional[str] = Query(default=None),
    created_after: Optional[datetime] = Query(default=None),
    created_before: Optional[datetime] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    svc: ApprovalItemService = Depends(get_service),
):
    items = await svc.list(
        status=status,
        type=type,
        created_after=created_after,
        created_before=created_before,
        limit=limit,
        offset=offset,
    )
    return list(items)


@router.get("/{item_id}", response_model=ApprovalItemRead)
async def get_approval_item(item_id: int, svc: ApprovalItemService = Depends(get_service)):
    return await svc.get(item_id)


@router.post("/{item_id}/approve", response_model=ApprovalItemRead)
async def approve_approval_item(item_id: int, payload: ApprovalItemApprove, svc: ApprovalItemService = Depends(get_service)):
    return await svc.approve(item_id, decision_by=payload.decision_by, decision_reason=payload.decision_reason)


@router.post("/{item_id}/reject", response_model=ApprovalItemRead)
async def reject_approval_item(item_id: int, payload: ApprovalItemReject, svc: ApprovalItemService = Depends(get_service)):
    return await svc.reject(item_id, decision_by=payload.decision_by, decision_reason=payload.decision_reason)
