# backend/app/features/chat/domain/enums.py
from __future__ import annotations

import enum


class ChatRole(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"