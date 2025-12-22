from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ApprovalItem(Base):
    __tablename__ = "approval_items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[str] = mapped_column(String, default="PENDING", index=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
