# backend/app/features/chat/domain/models.py
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from app.db.base import Base
from sqlalchemy import (
    JSON,
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ChatThread(Base):
    __tablename__ = "chat_threads"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Public/stable identifier (ULID/UUID7/string). Keep this even if you later expose it in URLs.
    thread_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    title: Mapped[Optional[str]] = mapped_column(String(200))
    created_by: Mapped[str] = mapped_column(String(128), nullable=False)

    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, server_default="{}")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="thread",
        cascade="all, delete-orphan",
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Public/stable identifier (optional but useful for tracing/tool-calls)
    message_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    thread_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("chat_threads.thread_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Keep as String for now; you can switch to SAEnum(ChatRole) later without changing API DTOs.
    role: Mapped[str] = mapped_column(String(16), nullable=False)  # system|user|assistant|tool

    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Stored as JSON arrays for UI rendering / audit / replay
    citations_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, server_default="[]")
    tool_calls_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, server_default="[]")
    tool_results_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, server_default="[]")

    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, server_default="{}")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    thread: Mapped["ChatThread"] = relationship(back_populates="messages")

    __table_args__ = (
        UniqueConstraint("thread_id", "message_id", name="uq_chat_messages_thread_id_message_id"),
    )


Index("ix_chat_threads_created_at", ChatThread.created_at)
Index("ix_chat_messages_thread_created_at", ChatMessage.thread_id, ChatMessage.created_at)
Index("ix_chat_messages_role_created_at", ChatMessage.role, ChatMessage.created_at)
