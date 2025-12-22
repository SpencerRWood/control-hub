from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.approval_item import ApprovalStatus


class ApprovalItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    type: str = Field(min_length=1, max_length=64)
    payload_json: dict[str, Any] = Field(default_factory=dict)
    requested_by: str = Field(min_length=1, max_length=128)
    assigned_to: Optional[str] = Field(default=None, max_length=128)


class ApprovalItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str]
    type: str
    payload_json: dict[str, Any]
    status: ApprovalStatus
    requested_by: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    decision_at: Optional[datetime]
    decision_by: Optional[str]
    decision_reason: Optional[str]


class ApprovalItemApprove(BaseModel):
    decision_by: str = Field(min_length=1, max_length=128)
    decision_reason: Optional[str] = None


class ApprovalItemReject(BaseModel):
    decision_by: str = Field(min_length=1, max_length=128)
    decision_reason: str = Field(min_length=1)
