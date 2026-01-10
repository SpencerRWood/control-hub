# backend/app/features/chat/api/router.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session_async import get_session  # adjust if your project uses a different import
from app.features.chat.domain.schemas import (
    ChatMessageCreate,
    ChatPostMessageResponse,
    ChatThreadCreate,
    ChatThreadDetailResponse,
    ChatThreadRead,
)
from app.features.chat.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service(session: AsyncSession = Depends(get_session)) -> ChatService:
    return ChatService(session=session)


@router.post("/threads", response_model=ChatThreadRead)
async def create_thread(
    body: ChatThreadCreate,
    svc: ChatService = Depends(get_chat_service),
) -> ChatThreadRead:
    try:
        return await svc.create_thread(body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/threads/{thread_id}/messages", response_model=ChatPostMessageResponse)
async def post_message(
    thread_id: str,
    body: ChatMessageCreate,
    svc: ChatService = Depends(get_chat_service),
) -> ChatPostMessageResponse:
    try:
        return await svc.post_message(thread_id=thread_id, body=body)
    except ValueError as e:
        # thread not found or bad request
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/threads/{thread_id}", response_model=ChatThreadDetailResponse)
async def get_thread(
    thread_id: str,
    limit: int = 200,
    offset: int = 0,
    svc: ChatService = Depends(get_chat_service),
) -> ChatThreadDetailResponse:
    try:
        return await svc.get_thread_detail(thread_id=thread_id, limit=limit, offset=offset)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
