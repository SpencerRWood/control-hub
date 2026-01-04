# app/features/rag/domain/enums.py
from enum import StrEnum


class IngestionStatus(StrEnum):
    STARTED = "STARTED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
